from meteostat import Stations, Daily
from datetime import datetime
import matplotlib.pyplot as plt

# Get weather stations by WMO ID
stations = Stations(wmo = ['71624', '72295', '68816', '94767']).fetch()

# Get names of weather stations
names = stations['name'].to_list()

# Get daily data for 2019
data = Daily(stations, start = datetime(2019, 1, 1), end = datetime(2019, 12, 31))
data = data.fetch()

# Plot data
ax = data.set_index('time').groupby(['station'])['tavg'].plot(kind = 'line', legend = True, ylabel = 'Avg. Daily Temperature °C', title = 'Average Temperature Report for 2019')
plt.legend(names)

# Show plot
plt.show()
