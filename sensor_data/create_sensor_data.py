#! python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import generators
from __future__ import nested_scopes
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import argparse
import json
import random

from datetime import datetime

LON = 143.19
LAT = 42.92


def main():
    """センサデータ生成用スクリプト
    """
    args = get_arguments()

    sensor_id = args.sensor_id
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    humidity = round(random.uniform(max(0.0, args.min_humidity), min(100.0, args.max_humidity)))
    temperature = round(random.uniform(args.min_temperature, args.max_temperature), 1)
    ph = round(random.uniform(max(1.0, args.min_ph), min(13.0, args.max_ph)), 1)
    whc = round(humidity * random.uniform(0.2, 0.8), 1)

    coord_result = {"lon": LON, "lat": LAT}
    main_result = {"humidity": humidity, "temperature": temperature, "ph": ph, "whc": whc}
    result = {"id": sensor_id, "date": time, "coord": coord_result, "main": main_result}

    print(json.dumps(result))


def get_arguments():
    """センサデータ生成用の引数を取得する。
    デフォルトでは広尾の気象データを基にデータが生成される。
    :return: 引数パース結果
    """
    parser = argparse.ArgumentParser(
        description="Random create sensor data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--sensor_id",
        type=int,
        default=1851632,
        help="Sensor id")

    parser.add_argument(
        "--min_humidity",
        type=float,
        default=25,
        help="Min humidity.")

    parser.add_argument(
        "--max_humidity",
        type=float,
        default=100,
        help="Max humidity.")

    parser.add_argument(
        "--min_temperature",
        type=float,
        default=-12.8,
        help="Min temperature.")

    parser.add_argument(
        "--max_temperature",
        type=float,
        default=30.4,
        help="Max temperature.")

    parser.add_argument(
        "--min_ph",
        type=float,
        default=4.5,
        help="Min pH.")

    parser.add_argument(
        "--max_ph",
        type=float,
        default=7.0,
        help="Max pH.")

    return parser.parse_args()


if __name__ == "__main__":
    main()
