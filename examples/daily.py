from datetime import date
import meteostat as ms
import logging

from meteostat.enumerations import Provider

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

ts = ms.hourly("10637", date(2024, 1, 1), date(2024, 1, 1))
print(ts.fetch(sources=True))
exit()


# Specify location and time range
POINT = ms.Point(50.1155, 8.6842, 113)
START = date(2024, 1, 1)
END = date(2024, 1, 1)

# Get nearby weather stations
stations = ms.nearby(POINT, limit=4)

# Get daily data & perform interpolation
ts = ms.hourly(stations, START, END)
print(ts.fetch())
df = ms.interpolate(ts, POINT)

print(df)
