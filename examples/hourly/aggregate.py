"""
Example: Aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Hourly

# Time period
start = datetime(2018, 1, 1)
end = datetime(2018, 1, 1, 23, 59)

# Get hourly data & aggregate daily
data = Hourly("10637", start, end)
data = data.aggregate("1D")
data = data.fetch()

# Print
print(data)
