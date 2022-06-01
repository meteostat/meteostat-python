"""
Example: Comparing aggregated data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

# Get weather stations by Meteostat ID
stations = Stations()
stations = stations.fetch()
stations = stations[stations.index.isin(("D1424", "10729", "10803", "10513"))]

# Get names of weather stations
names = stations["name"].to_list()

# Time period
start = datetime(2000, 1, 1)
end = datetime(2019, 12, 31)

# Get daily data
data = Daily(stations, start, end)

# Aggregate annually
data = data.aggregate(freq="1Y").fetch()

# Plot chart
fig, ax = plt.subplots(figsize=(8, 6))
data.unstack("station")["tmax"].plot(
    legend=True,
    ax=ax,
    style=".-",
    ylabel="Max. Annual Temperature (°C)",
    title="Max. Temperature Report",
)
plt.legend(names)
plt.show()
