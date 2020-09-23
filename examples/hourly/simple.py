from meteostat import Stations
from meteostat import Hourly
from datetime import datetime

# Hourly
stations = Stations(lat = 50, lon = 8)
station = stations.fetch(1)

data = Hourly(station, start = datetime(2020, 1, 1), end = datetime(2020, 1, 1, 23, 59))
print(data.fetch())
