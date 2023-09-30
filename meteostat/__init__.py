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
__version__ = "1.6.7"

from .interface.base import Base  # noqa
from .interface.timeseries import TimeSeries  # noqa
from .interface.stations import Stations  # noqa
from .interface.point import Point  # noqa
from .interface.hourly import Hourly  # noqa
from .interface.daily import Daily  # noqa
from .interface.monthly import Monthly  # noqa
from .interface.normals import Normals  # noqa
