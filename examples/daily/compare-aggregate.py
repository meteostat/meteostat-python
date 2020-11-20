from meteostat import Stations, Daily
from datetime import datetime
import matplotlib.pyplot as plt

# Get weather stations by WMO ID
stations = Stations(id = ['D1424', '10729', '10803', '10513']).fetch()

# Get names of weather stations
names = stations['name'].to_list()

# Get daily data for 2019
data = Daily(stations, start = datetime(2000, 1, 1), end = datetime(2019, 12, 31))
data = data.aggregate(freq = '1Y').fetch()

# Plot data
fig, ax = plt.subplots(figsize = (8, 6))
data.unstack('station')['tmax'].plot(kind = 'line', legend = True, ax = ax, style='.-', ylabel = 'Max. Annual Temperature (°C)', title = 'Max. Temperature Report')
plt.legend(names)

# Show plot
plt.show()
