# Structure

## Vision

```py
from meteostat import stations, hourly, settings, Provider, Parameter

settings.meteostat_dir = '/root/meteostat'

s = stations.nearby(50, 8, limit=4)
ts = hourly(s, '2020-01-01')
df = ts.fetch()

print(df)
```

## Project Structure

- meteostat
  - core
    - cache
    - logger
    - exceptions
    - loader
    - settings
  - api
    - hourly
    - daily
    - monthly
    - normals
    - latest
  - providers
    - dwd
      - climate_hourly
      - climate_daily
      - climate_monthly
      - normals_global
    - noaa
      - isd_lite
  - utils
    - units
    - metar