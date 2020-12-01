"""
Example: Simple chart

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

# Time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Inventory filter
inventory = { 'daily': [start, end] }

# Get a weather station
stations = Stations(lat=49.2497, lon=-123.1193, inventory=inventory)
station = stations.fetch(1)

# Get daily data
data = Daily(station, start=start, end=end)
data = data.fetch()

# Plot chart
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
