"""
Enumerations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from enum import Enum


class Granularity(Enum):
    """
    The different levels of data granularity
    """

    HOURLY = "hourly"
    DAILY = "daily"


class Parameter(Enum):
    """
    The different meteorological parameters supported by Meteostat
    """

    TEMP = "temp"  # Hourly
    TAVG = "tavg"  # Daily
    TMIN = "tmin"  # Daily
    TMAX = "tmax"  # Daily
    DWPT = "dwpt"  # Hourly
    PRCP = "prcp"  # Hourly, daily
    WDIR = "wdir"  # Hourly, daily
    WSPD = "wspd"  # Hourly, daily (avg)
    WPGT = "wpgt"  # Hourly, daily
    RHUM = "rhum"  # Hourly, daily (avg)
    PRES = "pres"  # Hourly, daily (avg)
    SNWD = "snow"  # Hourly, daily (max)
    SNOW = "snow"  # Hourly, daily (max)
    TSUN = "tsun"  # Hourly, daily
    SGHI = "sghi"  # Hourly, daily
    SDNI = "sdni"  # Hourly, daily
    SDHI = "sdhi"  # Hourly, daily
    CLDC = "cldc"  # Hourl, daily
    VSBY = "vsby"  # Hourly, daily
    COCO = "coco"  # Hourly


class Provider(Enum):
    """
    The default providers supported by Meteostat
    """

    NOAA_GHCND = "noaa_ghcnd"
    NOAA_ISD_LITE = "noaa_isd_lite"
    DWD_CLIMATE_HOURLY = "dwd_climate_hourly"
    DWD_CLIMATE_DAILY = "dwd_climate_daily"
    SYNOP = "synop"
    METAR = "metar"
    MOSMIX = "mosmix"
    COMPOSITE_HOURLY = "composite_hourly"
    COMPOSITE_DAILY = "composite_daily"


class Priority(Enum):
    HIGHEST = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    LOWEST = 1