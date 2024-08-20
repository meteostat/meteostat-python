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

from meteostat.settings import settings, env
from meteostat.cache import purge as purge_cache
from meteostat.enumerations import Parameter, Provider
from meteostat.stations.index import index
from meteostat.stations.station import station
from meteostat.stations.nearby import nearby
from meteostat.point import Point
from meteostat.timeseries.hourly import hourly
from meteostat.timeseries.daily import daily
from meteostat.timeseries.monthly import monthly
from meteostat.timeseries.normals import normals
from meteostat import units, interpolate

__all__ = [
    "settings",
    "env",
    "Parameter",
    "Provider",
    "index",
    "station",
    "nearby",
    "Point",
    "hourly",
    "daily",
    "monthly",
    "normals",
    "units",
    "interpolate",
    "purge_cache",
]
