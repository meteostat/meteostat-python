import os
import urllib.request
from urllib.error import HTTPError
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

      # Make sure the cache directory exists
      if not os.path.exists(self.cache_dir):
          os.mkdir(self.cache_dir)

      if file_path:
          # Return the file path if it exists
          if os.path.isfile(file_path):
              return True
          else:
              return False
      else:
          return False

  def _load(self, paths = None):

      if paths:

          # The list of local file file paths
          file_paths = []

          # Go thorugh paths
          for path in paths:

              # Get file path
              file_path = self._get_file_path(path)

              # Check if file in cache
              if not self._file_in_cache(file_path):
                  # Download file and save locally
                  try:
                      urllib.request.urlretrieve(self.endpoint + path, file_path)
                  except HTTPError:
                      continue

              # Add file path to list
              file_paths.append({
                'path': file_path,
                'origin': path
              })

          return file_paths
