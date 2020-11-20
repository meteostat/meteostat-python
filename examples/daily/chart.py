from meteostat import Stations, Daily
from datetime import datetime
import matplotlib.pyplot as plt

# Get a weather station
stations = Stations(lat = 49.2497, lon = -123.1193)
station = stations.fetch(1)

# Get daily data
data = Daily(station, start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
data = data.fetch()

# Plot chart
data.plot(y = ['tavg', 'tmin', 'tmax'], kind = 'line')
plt.show()
