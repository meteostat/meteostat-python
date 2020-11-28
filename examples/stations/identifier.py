"""
Example: Get weather stations by identifier

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get weather station with ICAO ID EDDF
stations = Stations(icao='EDDF')
station = stations.fetch(1).to_dict('records')[0]

# Print name
print(station["name"])
