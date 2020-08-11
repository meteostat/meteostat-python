"""
Core Class

Base class that provides methods which are used across the package

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import requests
from multiprocessing.pool import ThreadPool
import hashlib

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

  def _download_file(self, path = None):

      if path:
          # Get local file path
          local_path = self._get_file_path(path)

          # Check if file in cache
          if not self._file_in_cache(local_path):

              resource = requests.get(self.endpoint + path, stream = True)

              if resource.status_code == requests.codes.ok:

                  with open(local_path, 'wb') as file:
                      for data in resource:
                          file.write(data)

              else:
                  
                  # Create empty file
                  open(local_path, 'a').close()

          return {
              'path': local_path,
              'origin': path
          }

  def _load(self, paths = None):

      if paths:

          pool = ThreadPool(5).imap_unordered(self._download_file, paths)

          files = []

          for file in pool:
            files.append(file)

          return files
