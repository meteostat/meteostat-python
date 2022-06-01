"""
Example: Aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Monthly

# Time period
start = datetime(2000, 1, 1)
end = datetime(2018, 12, 31)

# Get monthly data
# Then, aggregate annually
data = Monthly("72202", start, end)
data = data.normalize().aggregate(freq="1Y").fetch()

# Plot chart
data.plot(y="tavg")
plt.show()
