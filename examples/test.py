from meteostat import timeseries, Parameter, Provider

ts = timeseries.hourly(
  '10637',
  '2020-01-01',
  '2020-01-01',
  parameters=[Parameter.TEMP],
  providers=[Provider.NOAA_ISD_LITE]
)

print(ts.df)