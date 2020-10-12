"""
Daily Class

Retrieve daily weather observations for one or multiple weather stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat.core import Core
import os
import pandas as pd
import datetime
from math import nan

class Daily(Core):

  # The list of weather Stations
  stations = None

  # The start date
  start = None

  # The end date
  end = None

  # The data frame
  data = pd.DataFrame()

  # Columns
  columns = [
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
  parse_dates = { 'time': [0] }

  # Default aggregations
  aggregations = {
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

                      self.data = self.data.append(df[(df['time'] >= self.start) & (df['time'] <= self.end)])

  def __init__(
    self,
    stations = None,
    start = None,
    end = None,
    cache_dir = None,
    max_age = None
  ):

      # Configuration - Cache directory
      if cache_dir != None:
          self.cache_dir = cache_dir

      # Configuration - Maximum file age
      if max_age != None:
          self.max_age = max_age

      # Set list of weather stations
      if isinstance(stations, pd.DataFrame):
          self.stations = stations
      else:
          self.stations = pd.DataFrame(stations, columns = ['id'])

      # Set start date
      self.start = start

      # Set end date
      self.end = end

      # Get data
      self._get_data(self.stations)

  def normalize(self):

      # List of columns
      columns = ['station', 'time']

      # Dynamically append columns
      for column in self.columns[2:]:
          columns.append(column)

      # Create result DataFrame
      result = pd.DataFrame(columns = columns)

      # Go through list of weather stations
      for station in self.stations['id'].tolist():
          # Create data frame
          df = pd.DataFrame(columns = columns)
          # Add time series
          df['time'] = pd.date_range(self.start, self.end, freq = '1D')
          # Add station ID
          df['station'] = station
          # Add columns
          for column in columns[2:]:
              # Add column to DataFrame
              df[column] = nan

          result = pd.concat([result, df], axis = 0)

      # Merge data
      self.data = pd.concat([self.data, result], axis = 0).groupby(['station', 'time'], as_index = False).first()

      # Return self
      return self

  def interpolate(self, limit = 3):

      # Apply interpolation
      self.data = self.data.groupby('station').apply(lambda group: group.interpolate(method = 'linear', limit = limit, limit_direction = 'both', axis = 0))

      # Return self
      return self

  def aggregate(self, freq = None, functions = None, spatial = False):

      # Update default aggregations
      if functions is not None:
          self.aggregations.update(functions)

      # Time aggregation
      self.data = self.data.groupby(['station', pd.Grouper(key = 'time', freq = freq)]).agg(self.aggregations)

      # Spatial aggregation
      if spatial:
          self.data = self.data.groupby([pd.Grouper(key = 'time', freq = freq)]).mean()

      # Return self
      return self

  def coverage(self, parameter = None):

      expect = (self.end - self.start).days + 1

      if parameter == None:
          return len(self.data.index) / expect
      else:
          return self.data[parameter].count() / expect


  def fetch(self, format = 'dict'):

          # Return data frame
          return self.data
