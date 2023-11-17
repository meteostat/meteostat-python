import logging
import meteostat as ms

logging.basicConfig(level=logging.INFO)

nearby = ms.stations.nearby(50, 8, 10000, 4)

print(nearby)

# ts = ms.hourly(
#   '10637',
#   '2020-01-01',
#   '2020-01-01',
#   parameters=[ms.Parameter.TEMP],
#   providers=[ms.Provider.NOAA_GHCND]
# )

# print(ts.fetch())