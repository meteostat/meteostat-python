"""
Example: Comparing multiple weather stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

# Get weather stations by WMO ID
stations = Stations()
stations = stations.id('wmo', ('71624', '72295', '68816', '94767'))
stations = stations.fetch()

# Get names of weather stations
names = stations['name'].to_list()

# Time period
start = datetime(2019, 1, 1)
end = datetime(2019, 12, 31)

# Get daily data
data = Daily(stations, start, end)
data = data.fetch()

# Plot chart
data.unstack('station')['tavg'].plot(
    legend=True,
    ylabel='Avg. Daily Temperature °C',
    title='Average Temperature Report for 2019')
plt.legend(names)
plt.show()
