from meteostat import Config, hourly, Parameters, Providers

Config.debug = True
Config.log_file = '/Users/chris/Meteostat/meteostat-python/examples/debug.log'

ts = hourly(
  ['10637', '10635', '10729', '71508', '71624', '71265', '71639'],
  '2020-01-01',
  '2021-12-31',
  parameters=[Parameters.TEMP],
  providers=[Providers.DWD_CLIMATE_HOURLY]
)
