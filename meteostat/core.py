"""
Core Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import errno
import time
import hashlib
from copy import copy
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError
import pandas as pd

class Core:

    """
    Base class that provides methods which are used across the package
    """

    # Base URL of the Meteostat bulk data interface
    _endpoint = 'https://bulk.meteostat.net/'

    # Location of the cache directory
    cache_dir = os.path.expanduser(
        '~') + os.sep + '.meteostat' + os.sep + 'cache'

    # Maximum age of a cached file in seconds
    max_age = 24 * 60 * 60

    # Maximum number of threads used for downloading files
    max_threads = 1

    def _get_file_path(self, path=False):

        if path:
            # Get file ID
            file_id = hashlib.md5(path.encode('utf-8')).hexdigest()
            # Return path
            return self.cache_dir + os.sep + self.cache_subdir + os.sep + file_id

        return False

    def _file_in_cache(self, file_path=False):

        # Make sure the cache directory exists
        if not os.path.exists(self.cache_dir + os.sep + self.cache_subdir):
            try:
                os.makedirs(self.cache_dir + os.sep + self.cache_subdir)
            except OSError as creation_error:
                if creation_error.errno == errno.EEXIST:
                    pass
                else:
                    raise Exception('Cannot create cache directory') from creation_error

        if file_path:
            # Return the file path if it exists
            if os.path.isfile(file_path) and time.time() - \
                    os.path.getmtime(file_path) <= self.max_age:
                return True

            return False

        return False

    def _download_file(self, path=None):

        if path:

            # Get local file path
            local_path = self._get_file_path(path)

            # Check if file in cache
            if not self._file_in_cache(local_path):

                if path[-6:-3] == 'csv':

                    # Get class name
                    class_name = self.__class__.__name__

                    # Read CSV file from Meteostat endpoint
                    try:
                        df = pd.read_csv(
                            self._endpoint + path,
                            compression='gzip',
                            names=self._columns,
                            dtype=self._types,
                            parse_dates=self._parse_dates)
                    except HTTPError:
                        # Get column names
                        columns = copy(self._columns)
                        # Replace date/hour columns with time column
                        if class_name in ('Hourly', 'Daily'):
                            for col in reversed(self._parse_dates['time']):
                                del columns[col]
                            columns.append('time')
                            columns.append('station')
                        # Create empty DataFrane
                        df = pd.DataFrame(columns=columns)
                        # Set dtype of time column
                        if class_name in ('Hourly', 'Daily'):
                            df = df.astype({'time': 'datetime64'})

                    # Add index and weather station ID
                    if class_name in ('Hourly', 'Daily'):
                        df['station'] = path[-12:-7]
                        df = df.set_index(['station', 'time'])
                    elif class_name == 'Stations':
                        df = df.set_index('id')

                # Save as Parquet
                df.to_parquet(local_path)

            return {
                'path': local_path,
                'origin': path
            }

        return False

    def _load(self, paths=None):

        if paths:

            # Create array of local file paths
            files = []

            # Single-thread processing
            if self.max_threads < 2:

                for path in paths:
                    files.append(self._download_file(path))

            # Multi-thread processing
            else:

                try:
                    pool = ThreadPool(
                        self.max_threads).imap_unordered(
                        self._download_file, paths)
                except BaseException as pool_error:
                    raise Exception('Cannot create ThreadPool') from pool_error

                for file in pool:
                    if file:
                        files.append(file)

            # Return list of local file paths
            return files

        return False

    @classmethod
    def clear_cache(cls, max_age=None):

        """
        Clear the cache
        """

        try:
            # Set max_age
            if max_age is None:
                max_age = cls.max_age

            # Get current time
            now = time.time()

            # Go through all files
            for file in os.listdir(
                    cls.cache_dir + os.sep + cls.cache_subdir):

                # Get full path
                path = os.path.join(
                    cls.cache_dir + os.sep + cls.cache_subdir, file)

                # Check if file is older than max_age
                if now - \
                        os.path.getmtime(path) > max_age and os.path.isfile(path):

                    # Delete file
                    os.remove(path)

        except BaseException as clear_error:
            raise Exception('Cannot clear cache') from clear_error
