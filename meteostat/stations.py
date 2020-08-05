from meteostat import core
import json
from math import cos, sqrt

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

      raw = self._get_file('stations/stations.json.gz')
      self.stations = json.loads(raw)

  def _distance(self, a, b):
      # Earth radius in m
      R = 6371000

      x = (b[1] - a[1]) * cos(0.5 * (b[0] + a[0]))
      y = (b[0] - a[0])

      return R * sqrt(x * x + y * y)

  def nearby(self, lat = False, lon = False):

      # Sort weather stations by distance
      self.stations = sorted(self.stations, key = lambda d: self._distance([d["latitude"], d["longitude"]], [lat, lon]))

      # Return self
      return self

  def country(self, country = False):

      # Check if country is set
      if country != False:
          self.stations = list(filter(lambda d: d["country"] == country, self.stations))

      # Return self
      return self

  def region(self, region = False):

      # Check if country is set
      if region != False:
          self.stations = list(filter(lambda d: d["region"] == region, self.stations))

      # Return self
      return self

  def area(self, top_lat = False, top_lon = False, bottom_lat = False, bottom_lon = False):

      # Return stations in boundaries
      self.stations = list(filter(lambda d: d["latitude"] <= top_lat and d["latitude"] >= bottom_lat and d["longitude"] <= bottom_lon and d["longitude"] >= top_lon, self.stations))

      # Return self
      return self

  def count(self):

      # Return number of weather stations in current selection
      return len(self.stations)

  def fetch(self, limit = 1):

      # Apply limit and return weather stations
      return self.stations[:limit]
