from meteostat import Stations, Hourly
from datetime import datetime

# Hourly
stations = Stations(wmo = '10637')
station = stations.fetch(1)

data = Hourly(station, start = datetime(2020, 1, 1), end = datetime(2020, 1, 1, 23, 59)).aggregate(freq = '1D')
print(data.fetch())
