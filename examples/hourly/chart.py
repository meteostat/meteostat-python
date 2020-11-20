from meteostat import Stations, Hourly
from datetime import datetime
import matplotlib.pyplot as plt

# Get a weather station
stations = Stations(lat = 50, lon = 8)
station = stations.fetch(1)

# Get hourly data
data = Hourly(station, start = datetime(2010, 1, 1), end = datetime(2020, 1, 1, 23, 59))
data = data.fetch()

# Plot chart
data.plot(y = 'temp', kind = 'line')
plt.show()
