"""
Example: Aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Stations, Hourly

# Hourly
stations = Stations(wmo='10637')
station = stations.fetch(1)

# Time period
start = datetime(2020, 1, 1)
end = datetime(2020, 1, 1, 23, 59)

# Get hourly data & aggregate
data = Hourly(station, start=start, end=end)
data = data.aggregate(freq='1D')
data = data.fetch()

# Print
print(data)
