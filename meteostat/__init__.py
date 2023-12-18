"""
█▀▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▀ ▀█▀ ▄▀█ ▀█▀
█░▀░█ ██▄ ░█░ ██▄ █▄█ ▄█ ░█░ █▀█ ░█░

A Python library for accessing open weather and climate data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

__appname__ = "meteostat"
__version__ = "2.0.0"

from meteostat.core.settings import settings
from meteostat.core.cache import purge as purge_cache
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.api import stations
from meteostat.api.hourly import hourly
from meteostat.api.daily import daily
from meteostat import types
from meteostat import units

__all__ = [
    "settings",
    "Parameter",
    "Provider",
    "Granularity",
    "stations",
    "hourly",
    "daily",
    "types",
    "units",
    "purge_cache",
]
