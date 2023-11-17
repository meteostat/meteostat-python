from meteostat import _stations, hourly, settings

settings.meteostat_dir = '/root/meteostat'

s = _stations.nearby(50, 8, limit=4)
ts = hourly(s, '2020-01-01')
df = ts.fetch()

print(df)