"""
Stations Class

Select weather stations from the full list of stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat.core import Core
import pandas as pd
from math import cos, sqrt, radians

class Stations(Core):

  # The list of selected weather Stations
  stations = None

  def __init__(self, lat = None, lon = None, radius = None, country = None, region = None, bounds = None):

      file = self._load(['stations/stations.json.gz'])[0]
      self.stations = pd.read_feather(file['path'])

      # Filter by country or region
      if country != None or region != None:
          self._regional(country, region)

      # Filter by boundaries
      if bounds != None:
          self._area(bounds)

      # Filter by distance
      if lat != None and lon != None:
          self._nearby(lat, lon, radius)

  def _distance(self, station, point):
      # Earth radius in m
      R = 6371000

      x = (radians(point[1]) - radians(station['longitude'])) * cos(0.5 * (radians(point[0]) + radians(station['latitude'])))
      y = (radians(point[0]) - radians(station['latitude']))

      return R * sqrt(x * x + y * y)

  def _nearby(self, lat = False, lon = False, radius = None):

      # Get distance for each stationsd
      self.stations['distance'] = self.stations.apply(lambda station: self._distance(station, [lat, lon]), axis = 1)

      # Filter by radius
      if radius != None:
          self.stations = self.stations[self.stations['distance'] <= radius]

      # Sort stations by distance
      self.stations.columns.str.strip()
      self.stations = self.stations.sort_values('distance')

      # Return self
      return self

  def _regional(self, country = None, region = None):

      # Check if country is set
      if country != None:
          self.stations = self.stations[self.stations['country'] == country]

      # Check if region is set
      if region != None:
          self.stations = self.stations[self.stations['region'] == region]

      # Return self
      return self

  def _area(self, bounds = None):

      # Return stations in boundaries
      if bounds != None:
          self.stations = self.stations[(self.stations['latitude'] <= bounds[0]) & (self.stations['latitude'] >= bounds[2]) & (self.stations['longitude'] <= bounds[3]) & (self.stations['longitude'] >= bounds[1])]

      # Return self
      return self

  def inventory(self, daily = None, hourly = None):

      # Check if daily is set
      if daily != None:
          self.stations = self.stations[(self.stations['daily.start'] != None) & (self.stations['daily.start'] <= daily) & (self.stations['daily.end'] >= daily)]

      # Check if hourly is set
      if hourly != None:
          self.stations = self.stations[(self.stations['hourly.start'] != None) & (self.stations['hourly.start'] <= hourly) & (self.stations['hourly.end'] >= hourly)]

      return self

  def sample(self, limit = 1):

      # Randomize the order of weather stations
      self.stations = self.stations.sample(limit)

      # Return self
      return self

  def count(self):

      # Return number of weather stations in current selection
      return len(self.stations.index)

  def fetch(self, limit = False):

      if limit:
          # Return data frame with limit
          return self.stations.head(limit)
      else:
          # Return all entries
          return self.stations
