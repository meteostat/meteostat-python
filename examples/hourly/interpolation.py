from meteostat import Stations, Hourly
from datetime import datetime
import matplotlib.pyplot as plt

# Hourly
station = ['10637']

data = Hourly(station, start = datetime(2020, 8, 1), end = datetime(2020, 8, 4, 23, 59))
data = data.normalize()
data = data.interpolate().fetch()
data.plot(x = 'time', y = ['temp'], kind = 'line')
plt.show()
