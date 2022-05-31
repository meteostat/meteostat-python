"""
Example: Aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Daily

# Time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Get daily data
data = Daily("10637", start, end)

# Group & aggregate weekly
data = data.normalize().aggregate(freq="1W").fetch()

# Plot chart
data.plot(y=["tavg", "tmin", "tmax"])
plt.show()
