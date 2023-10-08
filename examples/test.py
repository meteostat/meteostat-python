from meteostat import settings, timeseries, Parameter, Provider, stations

settings.debug = True
settings.log_file = '/Users/christianlamprecht/Private/meteostat-python/examples/debug.log'

if __name__ == '__main__':
  ts = timeseries.hourly(
    ['10637'],
    '2020-01-01',
    '2020-01-01',
    parameters=[Parameter.TEMP],
    providers=[Provider.NOAA_ISD_LITE]
  )