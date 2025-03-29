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

import os

from meteostat.core.config import config
from meteostat.enumerations import Parameter, Provider, TTL
from meteostat.api.station import station
from meteostat.api.stations import stations
from meteostat.api.point import Point
from meteostat.api.hourly import hourly
from meteostat.api.daily import daily
from meteostat.api.monthly import monthly
from meteostat.api.normals import normals
from meteostat.api.concat import concat
from meteostat.api.interpolate import interpolate
from meteostat import units, interpolate

# Set default configuration
config.set("cache.disable", False)
config.set(
    "cache.directory",
    os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "cache",
)
config.set("cache.ttl", 60 * 60 * 24 * 30)
config.set("cache.autoclean", True)
config.set("network.proxies", None)
config.set(
    "stations.meta.mirrors",
    [
        "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/stations/{id}.json",
        "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json",
    ],
)
config.set(
    "stations.index.mirrors",
    [
        "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/locations.csv.gz",
        "https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz",
    ],
)
config.set("stations.database.enable", False)
config.set("stations.database.ttl", TTL.WEEK)
config.set(
    "stations.database.url",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations.db",
)
config.set(
    "stations.database.file",
    os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "stations.db",
)

# Delete obsolete modules
del os, TTL

# Export public API
__all__ = [
    "config",
    "env",
    "Parameter",
    "Provider",
    "stations",
    "station",
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
