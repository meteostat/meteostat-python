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
from math import nan
from copy import copy

class Daily(Core):

  # The list of weather Stations
  _stations = None

  # The start date
  _start = None

  # The end date
  _end = None

  # The data frame
  _data = pd.DataFrame(index = ['station', 'time'])

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

  # Columns for date parsing
  _parse_dates = { 'time': [0] }

  # Default aggregation functions
  _aggregations = {
    'time': 'first',
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
                      df = pd.read_feather(file['path'])

                      self._data = self._data.append(df[(df['time'] >= self._start) & (df['time'] <= self._end)])

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
          self._stations = pd.DataFrame(stations, columns = ['id'])

      # Set start date
      self._start = start

      # Set end date
      self._end = end

      # Get data
      self._get_data(self._stations)

  def normalize(self):

      # List of columns
      columns = ['station', 'time']

      # Dynamically append columns
      for column in self._columns[1:]:
          columns.append(column)

      # Create result DataFrame
      result = pd.DataFrame(columns = columns)

      # Go through list of weather stations
      for station in self._stations['id'].tolist():
          # Create data frame
          df = pd.DataFrame(columns = columns)
          # Add time series
          df['time'] = pd.date_range(self._start, self._end, freq = '1D')
          # Add station ID
          df['station'] = station
          # Add columns
          for column in columns[2:]:
              # Add column to DataFrame
              df[column] = nan

          result = pd.concat([result, df], axis = 0)

      # Merge data
      self._data = pd.concat([self._data, result], axis = 0).groupby(['station', 'time'], as_index = False).first()

      # Return self
      return self

  def interpolate(self, limit = 3):

      # Apply interpolation
      self._data = self._data.groupby('station').apply(lambda group: group.interpolate(method = 'linear', limit = limit, limit_direction = 'both', axis = 0))

      # Return self
      return self

  def aggregate(self, freq = None, functions = None, spatial = False):

      # Update default aggregations
      if functions is not None:
          self._aggregations.update(functions)

      # Time aggregation
      self._data = self._data.groupby(['station', pd.Grouper(key = 'time', freq = freq)]).agg(self._aggregations)

      # Spatial aggregation
      if spatial:
          self._data = self._data.groupby([pd.Grouper(key = 'time', freq = freq)]).mean()

      # Return self
      return self

  def coverage(self, parameter = None):

      expect = (self._end - self._start).days + 1

      if parameter == None:
          return len(self._data.index) / expect
      else:
          return self._data[parameter].count() / expect


  def fetch(self):

          # Return data frame
          return copy(self._data)
