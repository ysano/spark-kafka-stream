# coding: UTF-8
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":

    # 1. "KafkaToCassandra"というアプリケーション名称を持つSparkSessionを作成
    spark = SparkSession.builder.appName("KafkaToCassandra").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # 2. 10秒ごとにストリーム処理を実行するStreamingContextを作成
    ssc = StreamingContext(spark.sparkContext, 10)

    # 3. kafka:9092でアクセス可能なKafkaの、`sensor-data` Topicからデータを取得する。
    kafka = KafkaUtils.createDirectStream(
        ssc, ["sensor-data"], {"metadata.broker.list": "kafka:9092"})

    # 4. JSONとして読み込むスキーマを指定
    coordSchema = StructType().add("lat",
                                   DoubleType()).add("lon", DoubleType())
    mainSchema = StructType().add("temperature", DoubleType()).add(
        "humidity", IntegerType()).add("ph",
                                       DoubleType()).add("whc", DoubleType())
    schema = StructType().add("id", LongType()).add("date", StringType()).add(
        "coord", coordSchema).add("main", mainSchema)

    def saveToCassandra(rdd):
        """
        RDDをDataFrameへ変換し、Cassandraへ登録
        """
        if not rdd.isEmpty():
            # JSONで構成されたRDDをスキーマ定義をもとにDataFrameへ変換
            df = rdd.toDF(schema)
            # Cassandraのテーブルレイアウトへ変換
            cassandraDf = df.withColumn("ts", from_unixtime(unix_timestamp(df.date, "yyyy/MM/dd HH:mm:ss"))) \
                            .select("id", "coord",
                                    date_format("ts", "yyyyMMdd").alias("date"),
                                    "ts", "main.temperature", "main.humidity",
                                    "main.ph", "main.whc")
            # imai_farm.sensor_rawテーブルへ書き出す
            cassandraDf.write \
                       .format("org.apache.spark.sql.cassandra") \
                       .mode("append") \
                       .options(table="sensor_raw", keyspace="imai_farm") \
                       .save()

    # 5. KafkaのメッセージをJSON形式に変換したRDDをCassandraへ保存するための関数へ渡す
    kafka.map(lambda k_v: json.loads(k_v[1])).foreachRDD(saveToCassandra)

    # 6. ストリーミング処理を開始し、終了されるまで継続的に読み込みと出力を実行
    ssc.start()
    ssc.awaitTermination()
