"""
Example: Spatial aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

# Time period
start = datetime(1980, 1, 1)
end = datetime(2019, 12, 31)

# Get random weather stations in the US
stations = Stations(country='US', having_daily=datetime(2005, 1, 1))
stations = stations.fetch(limit=5, sample=True)

# Get daily data
data = Daily(stations, start=start, end=end, max_threads=5)

# Normalize & aggregate
data = data.normalize().aggregate(freq='1Y', spatial=True).fetch()

# Chart title
TITLE = 'Average US Annual Temperature from 1980 to 2019'

# Plot chart
data.plot(y=['tavg'], title=TITLE)
plt.show()
