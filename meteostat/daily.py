"""
Daily Class

Retrieve daily weather observations for one or multiple weather stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import datetime
import pandas as pd
from meteostat.core import Core
from meteostat import units
from math import nan
from copy import copy

class Daily(Core):

  # The cache subdirectory
  _cache_subdir = 'daily'

  # The list of weather Stations
  _stations = None

  # The start date
  _start = None

  # The end date
  _end = None

  # The data frame
  _data = pd.DataFrame()

  # Columns
  _columns = [
    'date',
    'tavg',
    'tmin',
    'tmax',
    'prcp',
    'snow',
    'wdir',
    'wspd',
    'wpgt',
    'pres',
    'tsun'
  ]

  # Data tapes
  _types = {
    'tavg': 'float64',
    'tmin': 'float64',
    'tmax': 'float64',
    'prcp': 'float64',
    'snow': 'float64',
    'wdir': 'float64',
    'wspd': 'float64',
    'wpgt': 'float64',
    'pres': 'float64',
    'tsun': 'float64'
  }

  # Columns for date parsing
  _parse_dates = { 'time': [0] }

  # Default aggregation functions
  _aggregations = {
    'tavg': 'mean',
    'tmin': 'min',
    'tmax': 'max',
    'prcp': 'sum',
    'snow': 'mean',
    'wdir': 'mean',
    'wspd': 'mean',
    'wpgt': 'max',
    'pres': 'mean',
    'tsun': 'sum'
  }

  def _get_data(self, stations = None):

      if len(stations.index) > 0:

          paths = []

          for index, row in stations.iterrows():
              paths.append('daily/' + row['id'] + '.csv.gz')

          files = self._load(paths)

          if len(files) > 0:

              for file in files:

                  if os.path.isfile(file['path']) and os.path.getsize(file['path']) > 0:

                      df = pd.read_parquet(file['path'])

                      time = df.index.get_level_values('time')
                      self._data = self._data.append(df.loc[(time >= self._start) & (time <= self._end)])

  def __init__(
    self,
    stations = None,
    start = None,
    end = None,
    cache_dir = None,
    max_age = None,
    max_threads = None
  ):

      # Configuration - Cache directory
      if cache_dir != None:
          self._cache_dir = cache_dir

      # Configuration - Maximum file age
      if max_age != None:
          self._max_age = max_age

      # Configuration - Maximum number of threads
      if max_threads != None:
          self._max_threads = max_threads

      # Set list of weather stations
      if isinstance(stations, pd.DataFrame):
          self._stations = stations
      else:
          if not isinstance(stations, list):
              stations = [stations]

          self._stations = pd.DataFrame(stations, columns = ['id'])

      # Set start date
      self._start = start

      # Set end date
      self._end = end

      # Get data
      try:
          self._get_data(self._stations)
      except:
          raise Exception('Cannot read daily data')

      # Clear cache
      self.clear_cache()

  def normalize(self):

      # Create temporal instance
      temp = copy(self)

      # Create result DataFrame
      result = pd.DataFrame(columns = temp._columns[1:])

      # Go through list of weather stations
      for station in temp._stations['id'].tolist():
          # Create data frame
          df = pd.DataFrame(columns = temp._columns[1:])
          # Add time series
          df['time'] = pd.date_range(temp._start, temp._end, freq = '1D')
          # Add station ID
          df['station'] = station
          # Add columns
          for column in temp._columns[1:]:
              # Add column to DataFrame
              df[column] = nan

          result = pd.concat([result, df], axis = 0)

      # Set index
      result = result.set_index(['station', 'time'])

      # Merge data
      temp._data = pd.concat([temp._data, result], axis = 0).groupby(['station', 'time'], as_index = True).first()

      # Return class instance
      return temp

  def interpolate(self, limit = 3):

      # Create temporal instance
      temp = copy(self)

      # Apply interpolation
      temp._data = temp._data.groupby('station').apply(lambda group: group.interpolate(method = 'linear', limit = limit, limit_direction = 'both', axis = 0))

      # Return class instance
      return temp

  def aggregate(self, freq = None, functions = None, spatial = False):

      # Create temporal instance
      temp = copy(self)

      # Update default aggregations
      if functions is not None:
          temp._aggregations.update(functions)

      # Time aggregation
      temp._data = temp._data.groupby(['station', pd.Grouper(level = 'time', freq = freq)]).agg(temp._aggregations)

      # Spatial aggregation
      if spatial:
          temp._data = temp._data.groupby([pd.Grouper(level = 'time', freq = freq)]).mean()

      # Return class instance
      return temp

  def convert(self, units):

      # Create temporal instance
      temp = copy(self)

      # Change data units
      for parameter, unit in units.items():

          temp._data[parameter] = temp._data[parameter].apply(unit)

      # Return class instance
      return temp

  def coverage(self, parameter = None):

      expect = (self._end - self._start).days + 1

      if parameter == None:
          return len(self._data.index) / expect
      else:
          return self._data[parameter].count() / expect

  def count(self):

      # Return number of rows in DataFrame
      return len(self._data.index)

  def fetch(self):

      # Copy DataFrame
      temp = copy(self._data)

      # Remove station index if it's a single station
      if len(self._stations.index) == 1 and 'station' in temp.index.names:
          temp = temp.reset_index(level = 'station', drop = True)

      # Return data frame
      return temp
