"""
Example: Climate normals by geo point

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import matplotlib.pyplot as plt
from meteostat import Normals, Point

# Create Point for Vancouver, BC
vancouver = Point(49.2497, -123.1193, 70)

# Get normals
data = Normals(vancouver, 1961, 1990)
data = data.normalize().fetch()

# Plot chart
data.plot(y=["tavg", "tmin", "tmax"])
plt.show()
