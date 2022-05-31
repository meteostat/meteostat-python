"""
Example: Get weather stations by geographical area

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get all stations
stations = Stations()

# Get number of stations in northern hemisphere
northern = stations.bounds((90, -180), (0, 180))
print("Stations in northern hemisphere:", northern.count())

# Get number of stations in southern hemisphere
southern = stations.bounds((0, -180), (-90, 180))
print("Stations in southern hemisphere:", southern.count())
