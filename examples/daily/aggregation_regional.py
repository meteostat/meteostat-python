from meteostat import Stations
from meteostat import Daily
from datetime import datetime
import matplotlib.pyplot as plt

stations = Stations().country('US').inventory(daily = datetime(2005, 1, 1)).sample(100).fetch()

data = Daily(stations, start = datetime(2000, 1, 1), end = datetime(2019, 12, 31))
data = data.normalize().aggregate(freq = '1Y', overall = True).fetch()

data.plot(y = ['tavg'], kind = 'line', title = 'Average US Annual Temperature from 2000 to 2019')
plt.show()
