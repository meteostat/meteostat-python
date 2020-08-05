import gzip
import urllib.request

"""
A Python library for accessing open weather and climate data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

class Core:

  # Base URL of the Meteostat bulk data interface
  endpoint = 'https://bulk.meteostat.net/'

  def _get_file(self, path = False):
      if path:
          return gzip.decompress(urllib.request.urlopen(self.endpoint + path).read())
      else:
          return False
