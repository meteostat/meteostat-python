from meteostat import core
import pandas as pd
from math import cos, sqrt, radians

"""
A Python library for accessing open weather and climate data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

class Stations(core.Core):

  # The list of selected weather Stations
  stations = None

  def __init__(self):

      file = self._load(['stations/stations.json.gz'])[0]
      self.stations = pd.read_json(file['path'], orient = 'records', compression = 'gzip')

  def _distance(self, station, point):
      # Earth radius in m
      R = 6371000

      x = (radians(point[1]) - radians(station['longitude'])) * cos(0.5 * (radians(point[0]) + radians(station['latitude'])))
      y = (radians(point[0]) - radians(station['latitude']))

      return R * sqrt(x * x + y * y)

  def sort_distance(self, lat = False, lon = False):

      # Sort weather stations by distance
      # self.stations = sorted(self.stations, key = lambda d: self._distance([d["latitude"], d["longitude"]], [lat, lon]))

      # Get distance for each stationsd
      # self.stations = self.stations.assign(distance = lambda x: self._distance([x['latitude'], x['longitude']], [lat, lon]))
      self.stations['distance'] = self.stations.apply(lambda station: self._distance(station, [lat, lon]), axis = 1)

      # Sort stations by distance
      self.stations.columns.str.strip()
      self.stations = self.stations.sort_values('distance')

      # Return self
      return self

  def filter_country(self, country = False):

      # Check if country is set
      if country != False:
          self.stations = self.stations[self.stations['country'] == country]

      # Return self
      return self

  def filter_region(self, region = False):

      # Check if country is set
      if region != False:
          self.stations = self.stations[self.stations['region'] == region]

      # Return self
      return self

  def filter_area(self, top_lat = False, top_lon = False, bottom_lat = False, bottom_lon = False):

      # Return stations in boundaries
      self.stations = self.stations[(self.stations["latitude"] <= top_lat) & (self.stations["latitude"] >= bottom_lat) & (self.stations["longitude"] <= bottom_lon) & (self.stations["longitude"] >= top_lon)]

      # Return self
      return self

  def count(self):

      # Return number of weather stations in current selection
      return len(self.stations.index)

  def limit(self, limit = 1):

      # Apply limit and return weather stations
      self.stations = self.stations.head(limit)

      return self

  def fetch(self, limit = 1):

      # Apply limit and return weather stations
      return self.stations.head(limit).to_dict('records')
