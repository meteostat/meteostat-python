"""
Core Class - Cache

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
import time
import hashlib


def get_file_path(
    cache_dir: str,
    cache_subdir: str,
    path: str
) -> str:
    """
    Get the local file path
    """

    # Get file ID
    file = hashlib.md5(path.encode('utf-8')).hexdigest()

    # Return path
    return cache_dir + os.sep + cache_subdir + os.sep + file


def file_in_cache(
    path: str,
    max_age: int = 0
) -> bool:
    """
    Check if a file exists in the local cache
    """

    # Get directory
    directory = os.path.dirname(path)

    # Make sure the cache directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Return the file path if it exists
    if os.path.isfile(path) and time.time() - \
            os.path.getmtime(path) <= max_age:
        return True

    return False


@classmethod
def clear_cache(
    cls,
    max_age: int = None
) -> None:
    """
    Clear the cache
    """

    if os.path.exists(cls.cache_dir + os.sep + cls.cache_subdir):

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
