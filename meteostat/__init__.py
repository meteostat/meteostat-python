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

from meteostat.core.config import Config
from meteostat.enumerations import Parameters
from meteostat.enumerations import Providers
from meteostat.types import Station
from meteostat.interface.point import Point
from meteostat.interface.meta import meta, meta_bulk
from meteostat.interface.nearby import nearby
from meteostat.interface.hourly import hourly

__all__ = [
    'Config',
    'Parameters',
    'Providers',
    'Station',
    'Point',
    'meta',
    'meta_bulk',
    'nearby',
    'hourly',
    'framework'
]