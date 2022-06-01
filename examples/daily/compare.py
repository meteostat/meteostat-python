"""
Example: Comparing multiple weather stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Daily

# Time period
start = datetime(2019, 1, 1)
end = datetime(2019, 12, 31)

# Get daily data
data = Daily(["71624", "72295", "68816", "94767"], start, end)
data = data.fetch()

# Plot chart
data.unstack("station")["tavg"].plot(
    legend=True,
    ylabel="Avg. Daily Temperature °C",
    title="Average Temperature Report for 2019",
)
plt.show()
