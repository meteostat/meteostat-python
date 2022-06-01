"""
Example: Simple data access

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Stations, Hourly
from meteostat.units import fahrenheit, direction, condition

# Time period
start = datetime(2018, 1, 1)
end = datetime(2018, 1, 1, 23, 59)

# Get nearby weather station
stations = Stations()
stations = stations.nearby(50, 8)
station = stations.fetch(1)

# Get hourly data
data = Hourly(station, start, end, timezone="Europe/Berlin")

# Convert data units
data = data.convert({"temp": fahrenheit, "wdir": direction, "coco": condition})

# Print to console
data = data.fetch()
print(data)
