"""
Base Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""


class Base:

    """
    Base class that provides features which are used across the package
    """

    # Import configuration
    from meteostat.core.config import endpoint, cache_dir, max_age, max_threads
