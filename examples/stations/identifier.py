from meteostat import Stations

# Get weather station with Meteostat ID 10637
stations = Stations(id = '10637', icao = 'EDDF')
station = stations.fetch(1).to_dict('records')[0]

# Print name
print(station["name"]["en"])
