#!/usr/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)

# Create hiroo sensor data
python $SCRIPT_DIR/create_sensor_data.py --sensor_id 1851632 --min_humidity 25 --max_humidity 100 --min_temperature -12.8 --max_temperature 30.4

# Create muroran sensor data
python $SCRIPT_DIR/create_sensor_data.py --sensor_id 1851633 --min_humidity 37 --max_humidity 100 --min_temperature -5.8 --max_temperature 29

# Create obihiro sensor data
python $SCRIPT_DIR/create_sensor_data.py --sensor_id 1851634 --min_humidity 27 --max_humidity 100 --min_temperature -17.8 --max_temperature 31.9

# Create tomakomai sensor data
python $SCRIPT_DIR/create_sensor_data.py --sensor_id 1851635 --min_humidity 23 --max_humidity 100 --min_temperature -13.2 --max_temperature 27.8

# Create urakawa sensor data
python $SCRIPT_DIR/create_sensor_data.py --sensor_id 1851636 --min_humidity 30 --max_humidity 100 --min_temperature -8.2 --max_temperature 28.9
