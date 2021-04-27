"""
Example: Simple climate data access

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Normals

# Time period
start = datetime(1961, 1, 1)
end = datetime(1990, 12, 31)

# Get normals
data = Normals('10637', start, end)
data = data.fetch()

# Plot chart
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
