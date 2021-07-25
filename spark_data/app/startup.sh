#!/bin/bash
sh -c '/opt/bitnami/scripts/spark/run.sh > /opt/bitnami/spark/logs/run.log' &
sleep 10
sh -c 'spark-submit /opt/bitnami/spark/app/join_sensor2kafka.py > /opt/bitnami/spark/logs/join_sensor2kafka.log'
sleep 20
sh -c 'spark-submit /opt/bitnami/spark/app/kafka2cassandra.py > /opt/bitnami/spark/logs/kafka2cassandra.log'
sleep 20
sh -c 'spark-submit /opt/bitnami/spark/app/window_average.py > /opt/bitnami/spark/logs/window_average.log'

