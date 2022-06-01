"""
Example: Simple climate data access

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import matplotlib.pyplot as plt
from meteostat import Normals

# Get normals
data = Normals("10637")
data = data.normalize().fetch()

# Plot chart
data.plot(y=["tavg", "tmin", "tmax"])
plt.show()
