"""
Example: Hourly point data access

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Point, Hourly

# Time period
start = datetime(2021, 1, 1)
end = datetime(2021, 1, 1, 23, 59)

# The point
point = Point(50.3167, 8.5, 320)

# Get hourly data
data = Hourly(point, start, end, timezone="Europe/Berlin")

# Print to console
data = data.fetch()
print(data)
