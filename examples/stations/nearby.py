"""
Example: Closest weather station by coordinates

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get weather station
stations = Stations(lat=50, lon=8, having_hourly=True)
station = stations.fetch(1).to_dict('records')[0]

# Print name
print('Closest weather station at coordinates 50, 8:')
print(station["name"])
