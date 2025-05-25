from datetime import date
import meteostat as ms

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

point = ms.Point(50.3167, 8.5, 320)
stations = ms.stations.nearby(point, limit=5)

ts = ms.hourly(
    stations,
    start=date(2021, 1, 1),
    end=date(2021, 1, 2),
)

df = ms.interpolate(ts, point)

print(df)
