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

    # Import methods
    from meteostat.core.cache import _get_file_path, _file_in_cache, clear_cache
    from meteostat.core.loader import _processing_handler, _load_handler
    from meteostat.core.helper import _validate_series, _weighted_average, _degree_mean
