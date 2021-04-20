"""
Example: Simple

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Normals, Point

# Time period
start = datetime(1961, 1, 1)
end = datetime(1990, 12, 31)

# The point
point = Point(50.3167, 8.5, 320)

# Get normals
data = Normals(point, start, end)
data = data.fetch()

# Plot chart
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
