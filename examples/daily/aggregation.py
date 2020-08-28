from meteostat import Stations
from meteostat import Daily
from datetime import datetime
import matplotlib.pyplot as plt

data = Daily(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
data = data.normalize().aggregate(freq = '1W').fetch()

data.plot(x = 'time', y = ['tavg', 'tmin', 'tmax'], kind = 'line')
plt.show()
