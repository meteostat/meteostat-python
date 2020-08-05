from meteostat import Stations

# Get number of Stations in Ontario
stations = Stations()
stations.country('CA')
stations.region('ON')

print('Stations in Ontario:')
print(stations.count())

# Closest weather station for position
stations = Stations().nearby(50, 8).fetch(1)[0]

print('Closest weather station at coordinates 50, 8:')
print(stations["name"]["en"])

# Get number of stations in northern hemisphere
stations = Stations()
stations.area(90, -180, 0, 180)

print('Stations in northern hemisphere:')
print(stations.count())

# Get number of stations in southern hemisphere
stations = Stations()
stations.area(0, -180, -90, 180)

print('Stations in southern hemisphere:')
print(stations.count())
