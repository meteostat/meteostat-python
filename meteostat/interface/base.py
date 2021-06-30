"""
Base Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os


class Base:

    """
    Base class that provides features which are used across the package
    """

    # Base URL of the Meteostat bulk data interface
    endpoint: str = 'https://bulk.meteostat.net/v2/'

    # Location of the cache directory
    cache_dir: str = os.path.expanduser(
        '~') + os.sep + '.meteostat' + os.sep + 'cache'

    # Auto clean cache directories?
    autoclean: bool = True

    # Maximum age of a cached file in seconds
    max_age: int = 24 * 60 * 60

    # Number of processes used for processing files
    processes: int = 1

    # Number of threads used for processing files
    threads: int = 1
