"""
Example: Get weather stations by geographical area

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get number of stations in northern hemisphere
stations = Stations(bounds=[90, -180, 0, 180])

print('Stations in northern hemisphere:')
print(stations.count())

# Get number of stations in southern hemisphere
stations = Stations(bounds=[0, -180, -90, 180])

print('Stations in southern hemisphere:')
print(stations.count())
