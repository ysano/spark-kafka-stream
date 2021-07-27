# coding: UTF-8
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == "__main__":

    # 1. "JoinSensortoKafka"というアプリケーション名称を持つSparkSessionを作成
    spark = SparkSession.builder.appName("JoinSensortoKafka").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # 2. kafka:9092でアクセス可能なKafkaの、`sensor-data` Topicからデータを取得する。
    kafkaDataFrame = spark.readStream.format("kafka").option(
        "kafka.bootstrap.servers",
        "kafka:9092").option("subscribe", "sensor-data").load()

    # 3. Valueカラムを文字列に変換
    stringFormattedDataFrame = kafkaDataFrame.selectExpr(
        "CAST(value AS STRING) as value")

    # 4. JSONとして読み込むスキーマを指定
    coordSchema = StructType().add("lat",
                                   DoubleType()).add("lon", DoubleType())
    mainSchema = StructType().add("temperature", DoubleType()).add(
        "humidity", DoubleType()).add("ph",
                                      DoubleType()).add("whc", DoubleType())
    schema = StructType().add("id", LongType()).add("date", StringType()).add(
        "coord", coordSchema).add("main", mainSchema)
    # 5. スキーマを指定し、JSONとしてデータをパース
    jsonParsedDataFrame = stringFormattedDataFrame.select(
        from_json(stringFormattedDataFrame.value, schema).alias("sensor_data"))
    formattedDataFrame = jsonParsedDataFrame.select(
        col("sensor_data.id").alias("id"),
        col("sensor_data.date").alias("date"),
        col("sensor_data.coord.lat").alias("lat"),
        col("sensor_data.coord.lon").alias("lon"),
        col("sensor_data.main.temperature").alias("temperature"),
        col("sensor_data.main.humidity").alias("humidity"),
        col("sensor_data.main.ph").alias("ph"),
        col("sensor_data.main.whc").alias("whc"))

    # 6. センサIdのカラム名称を "id" > "sensor_id"に変更
    columnRenamedDataFrame = formattedDataFrame.withColumnRenamed(
        "id", "sensor_id")

    # 7. CSVとして読み込むスキーマを指定
    masterSchema = StructType().add("sensor_id",
                                    LongType()).add("field_id", StringType())

    # 8. センサ配置マスタの初めの行をヘッダとして扱い、CSVをスキーマを指定してDataFrameとして読込
    sensorMasterDataFrame = spark.read.format(
        "com.databricks.spark.csv").schema(masterSchema).option(
            "header", "true").load("/opt/bitnami/spark/app/sensor_field.csv")

    # 9. "sensor_id"カラムでセンサデータとセンサ配置マスタをLeft outer join
    joinedDataFrame = columnRenamedDataFrame.join(sensorMasterDataFrame,
                                                  "sensor_id", "leftouter")

    # 10. JoinしたDataFrameをKafkaに投入
    query = joinedDataFrame.selectExpr(
        "to_json(struct(*)) AS value").writeStream.format("kafka").option(
            "kafka.bootstrap.servers",
            "kafka:9092").option("topic", "joined-sensor-data").option(
                "checkpointLocation",
                "/opt/data/state/JoinSensortoKafka").start()

    # 11. 終了されるまで継続的に読み込みと出力を実行
    query.awaitTermination()
