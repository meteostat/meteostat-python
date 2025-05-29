"""
Base Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from typing import Optional


class Base:
    """
    Base class that provides features which are used across the package
    """

    # Base URL of the Meteostat bulk data interface
    endpoint = "https://bulk.meteostat.net/v2/"

    # Proxy URL for the Meteostat (bulk) data interface
    proxy: Optional[str] = None

    # Location of the cache directory
    cache_dir = os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "cache"

    # Auto clean cache directories?
    autoclean = True

    # Maximum age of a cached file in seconds
    max_age = 24 * 60 * 60

    # Number of processes used for processing files
    processes = 1

    # Number of threads used for processing files
    threads = 1
