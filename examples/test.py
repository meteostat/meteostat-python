from meteostat import config, timeseries, Parameters, Providers

config.debug = True
config.max_workers=12
config.log_file = '/Users/chris/Meteostat/meteostat-python/examples/debug.log'

if __name__ == '__main__':
  ts = timeseries.hourly(
    ['10637', '10635', '10729', '71508', '71624', '71265', '71639'],
    '2020-01-01',
    '2023-08-07',
    parameters=[Parameters.TEMP],
    providers=[Providers.NOAA_ISD_LITE]
  )