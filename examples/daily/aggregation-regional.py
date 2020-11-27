from meteostat import Stations, Daily
from datetime import datetime
import matplotlib.pyplot as plt

# Time period
start = datetime(1980, 1, 1)
end = datetime(2019, 12, 31)

# Get random weather stations in the US
stations = Stations(country = 'US', having_daily = datetime(2005, 1, 1))
stations = stations.fetch(limit = 5, sample = True)

# Get daily data
data = Daily(stations, start = start, end = end, max_threads = 5)

# Normalize & aggregate
data = data.normalize().aggregate(freq = '1Y', spatial = True).fetch()

# Chart title
title = 'Average US Annual Temperature from 1980 to 2019'

data.plot(y = ['tavg'], title = title)
plt.show()
