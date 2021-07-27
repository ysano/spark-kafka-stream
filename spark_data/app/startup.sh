#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

# Load libraries
. /opt/bitnami/scripts/libspark.sh
. /opt/bitnami/scripts/libos.sh

# default cmd
# sh -c /opt/bitnami/scripts/spark/run.sh &
# exit
# sleep 60

# Load Spark environment variables
eval "$(spark_env)"

EXEC=$(command -v spark-submit)
apps=(
    "joined-sensor-data.py"
    "kafka2cassandra.py"
    "window_average.py"
)
for APP in "${apps[@]}" ; do
    info "** spark-submit $APP **"
    ARGS="/opt/bitnami/spark/app/$APP </dev/null >/opt/bitnami/spark/logs/${APP##*/}.log 2>&1 &"
    if am_i_root; then
        sh -c "gosu nohup $EXEC ${ARGS[*]}"
    else
        sh -c "nohup $EXEC ${ARGS[*]}"
    fi
    sleep 20
done
