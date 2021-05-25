"""
Core Class - Configuration

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os

# Base URL of the Meteostat bulk data interface
endpoint: str = 'https://bulk.meteostat.net/v2/'

# Location of the cache directory
cache_dir: str = os.path.expanduser(
    '~') + os.sep + '.meteostat' + os.sep + 'cache'

# Maximum age of a cached file in seconds
max_age: int = 24 * 60 * 60

# Maximum number of threads used for downloading files
max_threads: int = 1
