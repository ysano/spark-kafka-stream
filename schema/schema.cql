CREATE KEYSPACE imai_farm WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE imai_farm ;

CREATE TYPE IF NOT EXISTS coords (
       lon float,
       lat float
);

-- select i, coord, ts, temperature from sensor_raw where id=? and date=?;
CREATE TABLE IF NOT EXISTS sensor_raw(
  id int,
  coord coords static,
  date text, /* yyyyMMdd 形式*/
  ts timestamp,
  temperature float,
  humidity float,
  ph float,
  whc float,
  PRIMARY KEY ((id, date), ts)
) WITH CLUSTERING ORDER BY (ts ASC);
