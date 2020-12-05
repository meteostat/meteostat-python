"""
Example: Interpolation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Hourly

# Time period
start = datetime(2020, 8, 1)
end = datetime(2020, 8, 4, 23, 59)

# Get hourly data
data = Hourly('10730', start, end)
data = data.normalize()
data = data.interpolate(6)
data = data.fetch()

# Plot chart
data.plot(y='temp')
plt.show()
