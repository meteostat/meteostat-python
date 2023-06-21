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
    The different levels of time series granularity
    """

    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    NORMALS = "normals"

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

class Providers(Enum):
    """
    The default providers supported by Meteostat
    """

    NOAA_GHCND = "noaa_ghcnd"
    NOAA_ISD_LITE = "noaa_isd_lite"
    DWD_CLIMATE_HOURLY = "dwd_climate_hourly"
    DWD_CLIMATE_DAILY = "dwd_climate_daily"
    MS_SYNOP = "ms_synop"
    MS_METAR = "ms_metar"
    MS_MOSMIX = "ms_mosmix"
    NOAA = (NOAA_GHCND, NOAA_ISD_LITE)
    DWD = (DWD_CLIMATE_HOURLY, DWD_CLIMATE_DAILY)
    MS = (MS_SYNOP, MS_METAR, MS_MOSMIX)
    OBSERVATIONS = (*NOAA, *DWD, MS_SYNOP, MS_METAR)
    MODEL = (MS_MOSMIX)