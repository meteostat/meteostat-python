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


class Core:

    """
    Base class that provides features which are used across the package
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

    def _get_file_path(self, subdir, path) -> str:
        """
        Get the local file path
        """

        # Get file ID
        file = hashlib.md5(path.encode('utf-8')).hexdigest()

        # Return path
        return self.cache_dir + os.sep + subdir + os.sep + file

    def _file_in_cache(self, path) -> bool:
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

    @classmethod
    def clear_cache(cls, max_age=None) -> None:
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
