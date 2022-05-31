"""
Compare Interpolation Methods

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Hourly

# Start & end datetime
start = datetime(2022, 3, 6, 0)
end = datetime(2022, 3, 13, 23)

# Schmitten (465m)
p1 = Point(50.2667, 8.45, 465)
# Neu-Anspach (320m)
p2 = Point(50.3167, 8.5, 320)
# Bad Homburg (186m)
p3 = Point(50.2268, 8.6182, 186)

# Fetch data
df1 = Hourly(p1, start, end).normalize().fetch()
df2 = Hourly(p2, start, end).fetch()
df3 = Hourly(p3, start, end).fetch()
df4 = Hourly("10635", start, end).fetch()
df5 = Hourly("D1424", start, end).fetch()

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
df1.plot(y=["temp"], ax=ax)
df2.plot(y=["temp"], ax=ax)
df3.plot(y=["temp"], ax=ax)
df4.plot(y=["temp"], ax=ax)
df5.plot(y=["temp"], ax=ax)

# Show plot
plt.legend(
    [
        f'Schmitten ({df1["temp"].mean()})',
        f'Neu-Anspach ({df2["temp"].mean()})',
        f'Bad Homburg ({df3["temp"].mean()})',
        f'Kleiner Feldberg ({df4["temp"].mean()})',
        f'Frankfurt Westend ({df5["temp"].mean()})',
    ]
)
plt.show()
