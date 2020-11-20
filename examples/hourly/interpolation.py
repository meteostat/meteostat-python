from meteostat import Stations, Hourly
from datetime import datetime
import matplotlib.pyplot as plt

# Hourly

data = Hourly('10730', start = datetime(2020, 8, 1), end = datetime(2020, 8, 4, 23, 59))
data = data.normalize()
data = data.interpolate(limit = 6).fetch()
data.plot(y = 'temp', kind = 'line')
plt.show()
