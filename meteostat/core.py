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
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError
from typing import Callable
import pandas as pd


class Core:

    """
    Base class that provides features which are used across the package
    """

    # Base URL of the Meteostat bulk data interface
    _endpoint: str = 'https://bulk.meteostat.net/'

    # Location of the cache directory
    cache_dir: str = os.path.expanduser(
        '~') + os.sep + '.meteostat' + os.sep + 'cache'

    # Maximum age of a cached file in seconds
    max_age: int = 24 * 60 * 60

    # Maximum number of threads used for downloading files
    max_threads: int = 1

    def _get_file_path(
        self,
        subdir: str,
        path: str
    ) -> str:
        """
        Get the local file path
        """

        # Get file ID
        file = hashlib.md5(path.encode('utf-8')).hexdigest()

        # Return path
        return self.cache_dir + os.sep + subdir + os.sep + file

    def _file_in_cache(
        self,
        path: str
    ) -> bool:
        """
        Check if a file exists in the local cache
        """

        # Get directory
        directory = os.path.dirname(path)

        # Make sure the cache directory exists
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as creation_error:
                if creation_error.errno == errno.EEXIST:
                    pass
                else:
                    raise Exception(
                        'Cannot create cache directory') from creation_error

        # Return the file path if it exists
        if os.path.isfile(path) and time.time() - \
                os.path.getmtime(path) <= self.max_age:
            return True

        return False

    @staticmethod
    def _processing_handler(
        datasets: list,
        load: Callable[[dict], None],
        max_threads: int
    ) -> None:

        # Single-thread processing
        if max_threads < 2:

            for dataset in datasets:
                load(*dataset)

        # Multi-thread processing
        else:

            pool = ThreadPool(max_threads)
            pool.starmap(load, datasets)

            # Wait for Pool to finish
            pool.close()
            pool.join()

    def _load_handler(
        self,
        path: str,
        columns: list,
        types: dict,
        parse_dates: list
    ) -> pd.DataFrame:

        try:

            # Read CSV file from Meteostat endpoint
            df = pd.read_csv(
                self._endpoint + path,
                compression='gzip',
                names=columns,
                dtype=types,
                parse_dates=parse_dates)

        except HTTPError:

            # Create empty DataFrane
            df = pd.DataFrame(columns=[*types])

        # Return DataFrame
        return df

    @staticmethod
    def _validate_series(
        df: pd.DataFrame,
        station: str
    ) -> pd.DataFrame:

        # Add missing column(s)
        if 'time' not in df.columns:
            df['time'] = None

        # Add weather station ID
        df['station'] = station

        # Set index
        df = df.set_index(['station', 'time'])

        # Return DataFrame
        return df

    @classmethod
    def clear_cache(
        cls,
        max_age: int = None
    ) -> None:
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
