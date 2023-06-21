"""
Providers Enumeration

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from enum import Enum


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