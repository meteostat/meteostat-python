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
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.interface.point import Point
from meteostat.interface.collection import Collection
from meteostat.core.providers import providers
from meteostat import types

__all__ = [
    'settings',
    'Parameter',
    'Provider',
    'Granularity',
    'providers',
    'Point',
    'Collection',
    'stations',
    'timeseries',
    'types'
]