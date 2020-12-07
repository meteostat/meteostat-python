"""
Example: Get weather stations by identifier

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get weather station with ICAO ID EDDF
stations = Stations()
station = stations.id('icao', 'EDDF').fetch()

# Print station
print(station)
