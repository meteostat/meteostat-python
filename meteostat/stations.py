"""
Stations Class

Select weather stations from the full list of stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import pandas as pd
from meteostat.core import Core
from math import cos, sqrt, radians
from copy import copy

class Stations(Core):

  # The cache subdirectory
  _cache_subdir = 'stations'

  # The list of selected weather Stations
  _stations = None

  # Columns
  _columns = [
    'id',
    'name',
    'country',
    'region',
    'wmo',
    'icao',
    'latitude',
    'longitude',
    'elevation',
    'timezone',
    'hourly_start',
    'hourly_end',
    'daily_start',
    'daily_end'
  ]

  _types = {
    'id': 'string',
    'name': 'object',
    'country': 'string',
    'region': 'string',
    'wmo': 'string',
    'icao': 'string',
    'latitude': 'float64',
    'longitude': 'float64',
    'elevation': 'float64',
    'timezone': 'string'
  }

  # Columns for date parsing
  _parse_dates = [10, 11, 12, 13]

  def __init__(
    self,
    lat = None,
    lon = None,
    radius = None,
    country = None,
    region = None,
    bounds = None,
    id = None,
    wmo = None,
    icao = None,
    daily = None,
    hourly = None,
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

      # Get all weather stations
      try:
          file = self._load(['stations/lib.csv.gz'])[0]
          self._stations = pd.read_parquet(file['path'])
      except:
           raise Exception('Cannot read weather station directory')

      # Filter by identifier
      if id != None or wmo != None or icao != None:
          self._identifier(id, wmo, icao)

      # Filter by country or region
      if country != None or region != None:
          self._regional(country, region)

      # Filter by boundaries
      if bounds != None:
          self._area(bounds)

      # Filter by distance
      if lat != None and lon != None:
          self._nearby(lat, lon, radius)

      # Filter by daily inventory
      if daily != None:
          self._inventory(daily, None)

      # Filter by hourly inventory
      if hourly != None:
          self._inventory(None, hourly)

      # Clear cache
      self.clear_cache()

  def _identifier(self, id = None, wmo = None, icao = None):

      # Get station by Meteostat ID
      if id != None:

          if not isinstance(id, list):
              id = [id]

          self._stations = self._stations[self._stations['id'].isin(id)]

      # Get station by WMO ID
      elif wmo != None:

          if not isinstance(wmo, list):
              wmo = [wmo]

          self._stations = self._stations[self._stations['wmo'].isin(wmo)]

      # Get stations by ICAO ID
      elif icao != None:

          if isinstance(icao, list):
              icao = [icao]

          self._stations = self._stations[self._stations['icao'] == icao]

      # Return self
      return self

  def _distance(self, station, point):

      # Earth radius in m
      R = 6371000

      x = (radians(point[1]) - radians(station['longitude'])) * cos(0.5 * (radians(point[0]) + radians(station['latitude'])))
      y = (radians(point[0]) - radians(station['latitude']))

      return R * sqrt(x * x + y * y)

  def _nearby(self, lat = False, lon = False, radius = None):

      # Get distance for each stationsd
      self._stations['distance'] = self._stations.apply(lambda station: self._distance(station, [lat, lon]), axis = 1)

      # Filter by radius
      if radius != None:
          self._stations = self._stations[self._stations['distance'] <= radius]

      # Sort stations by distance
      self._stations.columns.str.strip()
      self._stations = self._stations.sort_values('distance')

      # Return self
      return self

  def _regional(self, country = None, region = None):

      # Check if country is set
      if country != None:
          self._stations = self._stations[self._stations['country'] == country]

      # Check if region is set
      if region != None:
          self._stations = self._stations[self._stations['region'] == region]

      # Return self
      return self

  def _area(self, bounds = None):

      # Return stations in boundaries
      if bounds != None:
          self._stations = self._stations[(self._stations['latitude'] <= bounds[0]) & (self._stations['latitude'] >= bounds[2]) & (self._stations['longitude'] <= bounds[3]) & (self._stations['longitude'] >= bounds[1])]

      # Return self
      return self

  def _inventory(self, daily = None, hourly = None):

      # Check if daily is set
      if daily != None:
          self._stations = self._stations[(self._stations['daily_start'] != None) & (self._stations['daily_start'] <= daily) & (self._stations['daily_end'] >= daily)]

      # Check if hourly is set
      if hourly != None:
          self._stations = self._stations[(self._stations['hourly_start'] != None) & (self._stations['hourly_start'] <= hourly) & (self._stations['hourly_end'] >= hourly)]

      return self

  def convert(self, units):

      # Create temporal instance
      temp = copy(self)

      # Change data units
      for parameter, unit in units.items():

          temp._stations[parameter] = temp._stations[parameter].apply(unit)

      # Return class instance
      return temp

  def count(self):

      # Return number of weather stations in current selection
      return len(self._stations.index)

  def fetch(self, limit = False, sample = False):

      # Copy DataFrame
      temp = copy(self._stations)

      if sample and limit:
          # Return limited number of sampled entries
          return temp.sample(limit)
      elif limit:
          # Return limited number of entries
          return temp.head(limit)
      else:
          # Return all entries
          return temp
