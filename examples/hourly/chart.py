"""
Example: Simple chart

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Hourly

# Get closest weather station
stations = Stations()
stations = stations.nearby(50, 8)
station = stations.fetch(1)

# Time period
start = datetime(2017, 1, 1)
end = datetime(2017, 1, 1, 23, 59)

# Get hourly data
data = Hourly(station, start, end)
data = data.fetch()

# Plot chart
data.plot(y="temp")
plt.show()
