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
from meteostat.interface.enumerations.parameters import Parameters
from meteostat.interface.enumerations.providers import Providers
from meteostat.interface.enumerations.granularity import Granularity
from meteostat.interface.point import Point
from meteostat.interface.collection import Collection

__all__ = [
    'config',
    'Parameters',
    'Providers',
    'Granularity',
    'Point',
    'Collection',
    'stations',
    'timeseries',
    'framework'
]