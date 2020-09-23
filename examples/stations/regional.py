from meteostat import Stations

# Get number of Stations in Ontario
stations = Stations(country = 'CA', region = 'ON')

print('Stations in Ontario:')
print(stations.count())
