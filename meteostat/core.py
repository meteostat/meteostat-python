"""
█▀▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▀ ▀█▀ ▄▀█ ▀█▀
█░▀░█ ██▄ ░█░ ██▄ █▄█ ▄█ ░█░ █▀█ ░█░

Core Class

Base class that provides methods which are used across the package

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import errno
import time
import hashlib
import pandas as pd
from copy import copy
from multiprocessing.pool import ThreadPool

class Core:

  # Base URL of the Meteostat bulk data interface
  _endpoint = 'https://bulk.meteostat.net/'

  # Location of the cache directory
  _cache_dir = os.path.expanduser('~') + os.sep + '.meteostat' + os.sep + 'cache'

  # Maximum age of a cached file in seconds
  _max_age = 24 * 60 * 60

  # Maximum number of threads used for downloading files
  _max_threads = 1

  def _get_file_path(self, path = False):

      if path:
          # Get file ID
          file_id = hashlib.md5(path.encode('utf-8')).hexdigest()
          # Return path
          return self._cache_dir + os.sep + self._cache_subdir + os.sep + file_id
      else:
          # Return false
          return False

  def _file_in_cache(self, file_path = False):

      # Make sure the cache directory exists
      if not os.path.exists(self._cache_dir + os.sep + self._cache_subdir):
          try:
              os.makedirs(self._cache_dir + os.sep + self._cache_subdir)
          except OSError as e:
              if e.errno == errno.EEXIST:
                  pass
              else:
                  raise Exception('Cannot create cache directory')

      if file_path:
          # Return the file path if it exists
          if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) <= self._max_age:
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

                  # Read CSV file from Meteostat endpoint
                  df = pd.read_csv(self._endpoint + path, compression = 'gzip', names = self._columns, dtype = self._types, parse_dates = self._parse_dates)

                  # Set weather station ID
                  if self.__class__.__name__ == 'Hourly' or self.__class__.__name__ == 'Daily':
                      df['station'] = path[-12:-7]
                      df = df.set_index(['station', 'time'])

              # Save as Parquet
              df.to_parquet(local_path)

          return {
              'path': local_path,
              'origin': path
          }

  def _load(self, paths = None):

      if paths:

          # Create array of local file paths
          files = []

          # Single-thread processing
          if self._max_threads < 2:

              for path in paths:
                  files.append(self._download_file(path))

          # Multi-thread processing
          else:

              try:
                  pool = ThreadPool(self._max_threads).imap_unordered(self._download_file, paths)
              except:
                  raise Exception('Cannot create ThreadPool')

              for file in pool:
                if file != False:
                    files.append(file)

          # Return list of local file paths
          return files

  def clear_cache(self, max_age = None):

      try:
          # Set max_age
          if max_age is None:
              max_age = self._max_age

          # Get current time
          now = time.time()

          # Go through all files
          for file in os.listdir(self._cache_dir + os.sep + self._cache_subdir):

              # Get full path
              path = os.path.join(self._cache_dir + os.sep + self._cache_subdir, file)

              # Check if file is older than max_age
              if now - os.path.getmtime(path) > max_age and os.path.isfile(path):

                  # Delete file
                  os.remove(path)

      except:
          raise Exception('Cannot clear cache')
