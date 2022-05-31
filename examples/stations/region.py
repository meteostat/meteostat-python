"""
Example: Select weather stations by country & state

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Stations

# Get stations in Ontario
stations = Stations()
stations = stations.region("CA", "ON")

# Print count to console
print("Stations in Ontario:", stations.count())
