from meteostat import Stations, Daily
from datetime import datetime
import matplotlib.pyplot as plt

stations = Stations(country = 'US', daily = datetime(2005, 1, 1)).sample(50).fetch()

data = Daily(stations, start = datetime(1980, 1, 1), end = datetime(2019, 12, 31))
data = data.normalize().aggregate(freq = '1Y', spatial = True).fetch()

data.plot(y = ['tavg'], kind = 'line', title = 'Average US Annual Temperature from 1980 to 2019')
plt.show()
