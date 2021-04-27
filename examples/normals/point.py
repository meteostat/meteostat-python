"""
Example: Climate normals by geo point

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

# Create Point for Vancouver, BC
vancouver = Point(49.2497, -123.1193, 70)

# Get normals
data = Normals(vancouver, start, end)
data = data.fetch()

# Plot chart
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
