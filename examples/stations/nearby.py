from meteostat import Stations

# Closest weather station for position
stations = Stations()
stations.sort_distance(50, 8)
station = stations.fetch(1)[0]

print('Closest weather station at coordinates 50, 8:')
print(station["name"]["en"])
