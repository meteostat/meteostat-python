"""
Core Class

Base class that provides methods which are used across the package

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import time
import pandas as pd
from multiprocessing.pool import ThreadPool
import hashlib

class Core:

  # Base URL of the Meteostat bulk data interface
  endpoint = 'https://bulk.meteostat.net/'

  # Location of the Meteostat directory
  ms_dir = os.path.expanduser('~') + os.sep + '.meteostat'

  # Location of the cache directory
  cache_dir = ms_dir + os.sep + 'cache'

  # Maximum age of a cached file in seconds
  cache_max_age = 24 * 60 * 60

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
          if os.path.isfile(file_path) and os.path.getmtime(file_path) - time.time() <= self.cache_max_age:
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

              if path[-6:-3] == 'csv':

                  # The columns which are used for parsing date and time
                  time_cols = [0, 1]

                  # Update time columns for daily data
                  if self.__class__.__name__ == 'Daily':
                      time_cols = [0]

                  # Read CSV file from Meteostat endpoint
                  df = pd.read_csv(self.endpoint + path, compression = 'gzip', names = self.columns, parse_dates = { 'time': time_cols })

                  # Set weather station ID
                  df['station'] = path[-12:-7]

              else:

                  # Read JSON file
                  df = pd.read_json(self.endpoint + path, orient = 'records', compression = 'gzip')

              # Save as Feather
              df.to_feather(local_path)

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
