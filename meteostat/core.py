import os
import urllib.request
import hashlib

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

  # Location of the cache directory
  cache_dir = os.path.expanduser("~") + os.sep + ".meteostat"

  def _get_file_path(self, path = False):

      if path:
          # Get file ID
          file_id = hashlib.md5(path.encode('utf-8')).hexdigest()
          # Return path
          return self.cache_dir + os.sep + file_id
      else:
          # Return false
          return False

  def _file_in_cache(self, file_path = False):

      if file_path:
          # Return the file path if it exists
          if os.path.isfile(file_path):
              return True
          else:
              return False
      else:
          return False

  def _load_file(self, path = False):

      if path:
          # Make sure the cache directory exists
          if not os.path.exists(self.cache_dir):
              os.mkdir(self.cache_dir)

          # Get file path
          file_path = self._get_file_path(path)

          # Check if file in cache
          if self._file_in_cache(file_path):
              return file_path
          else:
              # Download file and save locally
              urllib.request.urlretrieve(self.endpoint + path, file_path)
              # Return file file
              return file_path
