from meteostat import Stations, Hourly
from meteostat.units import fahrenheit, direction, condition
from datetime import datetime

# Hourly
stations = Stations(lat = 50, lon = 8)
station = stations.fetch(1)

data = Hourly(station, start = datetime(2020, 1, 1), end = datetime(2020, 1, 1, 23, 59))
data = data.convert({ 'temp': fahrenheit, 'wdir': direction, 'coco': condition })
data = data.fetch()
print(data)
