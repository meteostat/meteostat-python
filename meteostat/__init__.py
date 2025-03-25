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

from meteostat.core.config import config
from meteostat.enumerations import Parameter, Provider
from meteostat.api.stations import stations, station, nearby, connect_stations_db
from meteostat.api.point import Point
from meteostat.api.hourly import hourly
from meteostat.api.daily import daily
from meteostat.api.monthly import monthly
from meteostat.api.normals import normals
from meteostat.api.concat import concat
from meteostat.api.interpolate import interpolate
from meteostat import units, interpolate

__all__ = [
    "config",
    "env",
    "Parameter",
    "Provider",
    "stations",
    "station",
    "nearby",
    "connect_stations_db",
    "Point",
    "hourly",
    "daily",
    "monthly",
    "normals",
    "units",
    "interpolate",
    "concat",
    "interpolate",
]
