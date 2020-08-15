from meteostat import Stations
from meteostat import Daily
from datetime import datetime
import matplotlib.pyplot as plt

# Hourly
stations = Stations()
stations.sort_distance(50, 8)
station = stations.fetch(1)
# station = ['10637']

data = Daily(station, start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
data = data.fetch()

data.plot(x = 'time', y = ['tavg', 'tmin', 'tmax'], kind = 'line')
plt.show()
