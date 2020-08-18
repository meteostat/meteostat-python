"""
Hourly Class

Retrieve hourly weather observations for one or multiple weather stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat.core import Core
from math import floor
import os
import pandas as pd
import datetime

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

              for file in files:

                  if os.path.isfile(file['path']) and os.path.getsize(file['path']) > 0:
                      df = pd.read_feather(file['path'])

                      self.data = self.data.append(df[(df['time'] >= self.start) & (df['time'] <= self.end)])

  def __init__(self, stations = None, start = None, end = None):

          if isinstance(stations, pd.DataFrame):
              self.stations = stations
          else:
              self.stations = pd.DataFrame(stations, columns = ['id'])

          self.start = start
          self.end = end

          self._get_data(self.stations)

  def coverage(self, parameter = None):

      expect = floor((self.end - self.start).total_seconds() / 3600) + 1

      if parameter == None:
          return len(self.data.index) / expect
      else:
          return self.data[parameter].count() / expect

  def fetch(self, format = 'dict'):

      # Return data frame
      return self.data
