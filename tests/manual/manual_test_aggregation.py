"""
Compare hourly aggregations with daily data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""


from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Hourly, Stations, Daily

start = datetime(2007, 12, 30)
end = datetime(2021, 12, 31)
lat, lon = 6.25, -75.5

stations = Stations()
station = stations.nearby(lat, lon).fetch(1)
data_daily = Daily(station, start, end, model=True).fetch()
data_agg = Hourly(station, start, end, timezone="America/Bogota", model=True)
data_agg = data_agg.normalize().aggregate("1D").fetch()

fig = plt.figure()
plt.plot(
    data_daily.index.date, data_daily["tavg"].values, label="Daily mean by Meteostat"
)
plt.plot(
    data_agg.index.date,
    data_agg["temp"].values,
    color="black",
    label="Daily mean calculated with aggregate",
    linewidth=0.25,
)


plt.legend()
plt.show()
