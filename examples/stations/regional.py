from meteostat import Stations

# Get number of Stations in Ontario
stations = Stations()
stations.filter_country('CA')
stations.filter_region('ON')

print('Stations in Ontario:')
print(stations.count())
