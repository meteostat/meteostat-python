from meteostat import Stations
from meteostat import Hourly
from datetime import datetime

# Get number of Stations in Ontario
stations = Stations()
stations.filter_country('CA')
stations.filter_region('ON')

# data = Hourly(stations, start = datetime(2020, 1, 1), end = datetime(2020, 1, 1))

print('Stations in Ontario:')
print(stations.count())

# Closest weather station for position
stations = Stations()
stations.sort_distance(50, 8)
station = stations.fetch(1)[0]

print('Closest weather station at coordinates 50, 8:')
print(station["name"]["en"])

# Hourly
stations = Stations()
stations.sort_distance(50, 8)
station = stations.limit(1)

data = Hourly(station, start = datetime(1890, 1, 1), end = datetime(1890, 1, 1, 23, 59))
print(data.fetch())

# Get number of stations in northern hemisphere
stations = Stations()
stations.filter_area(90, -180, 0, 180)

print('Stations in northern hemisphere:')
print(stations.count())

# Get number of stations in southern hemisphere
stations = Stations()
stations.filter_area(0, -180, -90, 180)

print('Stations in southern hemisphere:')
print(stations.count())
