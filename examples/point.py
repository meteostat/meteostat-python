from datetime import datetime
import meteostat as ms

point = ms.Point(50, 8)

ts = ms.hourly(point, datetime(2020, 1, 1, 6), datetime(2020, 1, 1, 18))
df = ms.interpolate(ts, point, method="nearets")

print(df)