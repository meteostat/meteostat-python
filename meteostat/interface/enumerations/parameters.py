"""
Parameters Enumeration

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from enum import Enum


class Parameters(Enum):
    """
    The different meteorological parameters supported by Meteostat
    """

    TEMP = "TEMP" # Hourly
    TAVG = "TAVG" # Daily
    TMIN = "TMIN" # Daily
    TMAX = "TMAX" # Daily
    DWPT = "DWPT" # Hourly
    PRCP = "PRCP" # Hourly, daily
    WDIR = "WDIR" # Hourly, daily
    WSPD = "WSPD" # Hourly, daily (avg)
    WPGT = "WPGT" # Hourly, daily
    RHUM = "RHUM" # Hourly, daily (avg)
    PRES = "PRES" # Hourly, daily (avg)
    SNOW = "SNOW" # Hourly, daily (max)
    TSUN = "TSUN" # Hourly, daily
    COCO = "COCO" # Hourly