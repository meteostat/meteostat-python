from meteostat.core import Core
import pandas as pd
import datetime

"""
A Python library for accessing open weather and climate data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

class Hourly(Core):

  # The list of weather Stations
  stations = None

  # The start date
  start = None

  # The end date
  end = None

  # The data frame
  data = pd.DataFrame()

  # Columns
  columns = ['date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']

  def _get_data(self, stations = None):

      if len(stations.index) > 0:

          paths = []

          for index, row in stations.iterrows():
              paths.append('hourly/' + row['id'] + '.csv.gz')

          files = self._load(paths)

          if len(files) > 0:
              """
              for file in file_paths:
                  iter_csv = pd.read_csv(file, compression = 'gzip', names = self.columns, parse_dates = { 'time': [0,1] }, iterator = True, chunksize = 1000)
                  self.data.concat([chunk[self.start <= chunk['time'] <= self.end] for chunk in iter_csv])
                  pd.concat((pd.read_csv(f) for f in all_files))
              """
              for file in files:
                  for chunk in pd.read_csv(file['path'], compression = 'gzip', names = self.columns, parse_dates = { 'time': [0,1] }, iterator = True, chunksize = 1000):
                      chunk['station'] = file['origin'][-12:-7]
                      self.data = self.data.append(chunk[(chunk['time'] >= self.start) & (chunk['time'] <= self.end)])

              # self.data = pd.concat([chunk[(chunk['time'] >= self.start) & (chunk['time'] <= self.end)] for chunk in pd.read_csv(file, compression = 'gzip', names = self.columns, parse_dates = { 'time': [0,1] }, iterator = True, chunksize = 1000)] for file in file_paths)

  def __init__(self, stations = None, start = None, end = None):

      if stations:
          self.stations = stations
          self.start = start
          self.end = end

          self._get_data(stations.stations)

  def fetch(self):

      # Return data as dictionary
      return self.data.to_dict('records')
