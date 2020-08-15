from meteostat import Stations
from meteostat import Hourly
from datetime import datetime
import matplotlib.pyplot as plt

# Hourly
stations = Stations()
stations.sort_distance(50, 8)
station = stations.limit(1)

data = Hourly(station, start = datetime(2010, 1, 1), end = datetime(2020, 1, 1, 23, 59))
data = data.fetch()

data.plot(x = 'time', y = ['temp'], kind = 'line')
plt.show()
