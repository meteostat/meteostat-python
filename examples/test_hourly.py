from datetime import datetime, date
import logging
import meteostat as ms

ts = ms.hourly(
    ("10637"),
    datetime(2022, 1, 1, 11),
    datetime(2022, 1, 1, 12),
    parameters=(ms.Parameter.TEMP,),
    providers=(ms.Provider.SYNOP, ms.Provider.METAR),
    lite=False
)

print(ts.sourcemap)
exit()

# logging.basicConfig(level=logging.INFO)

# ms.purge_cache(0)

start = date(2020, 1, 1)
end = date(2020, 1, 1)

ts = ms.hourly(
    ("10637", "10635"),
    start,
    end,
    parameters=(ms.Parameter.TEMP,),
    providers=(ms.Provider.SYNOP,),
)

ts = ts.apply(ms.units.to_fahrenheit, ms.Parameter.TEMP)

df = ts.fetch(squash=False)

print(df)
exit()


# point = ms.Point(50, 8, 100)
# start = datetime(2020, 1, 1, 10, 0)
# end = datetime(2020, 1, 1, 11, 0)

# stations = ms.stations.nearby(point)

# data = []

# for station in stations[stations['elevation'] < 800]:
#     data.append(ms.hourly(station, start, end))

# ts = ms.concat(data)
# df = ms.interpolate.idw(ts, point, lapse_rate=True)

###

logging.basicConfig(level=logging.INFO)
ms.purge_cache(0)

point = ms.Point(50, 8, 100)
start = datetime(2020, 1, 1, 10, 0)
end = datetime(2020, 1, 1, 11, 0)

# print(ms.stations.meta('10637'))
exit()

nearby = ms.stations.nearby(point, limit=4)

ts = ms.hourly(
    ["10637", "10635", "10729"],
    start,
    end,
    parameters=(ms.Parameter.TEMP,),
    providers=(ms.Provider.SYNOP,),
    lite=False,
)

df = ms.interpolate.idw(ts, point, lapse_rate=True)

print(df)
