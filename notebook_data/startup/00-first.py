# coding: UTF-8
import os
import sys

spark_home = os.environ.get('SPARK_HOME', None)
sys.path.insert(0, spark_home + "/python")
sys.path.insert(0, os.path.join(spark_home, "python/lib/py4j-0.10.9-src.zip"))
exec(open(os.path.join(spark_home, "python/pyspark/shell.py")).read())
