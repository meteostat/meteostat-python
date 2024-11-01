"""
Enumerations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from enum import StrEnum, IntEnum


class Granularity(StrEnum):
    """
    The different levels of time series granularity
    """

    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    NORMALS = "normals"


class Frequency(StrEnum):
    """
    The different levels of time series frequency
    """

    HOURLY = "H"
    DAILY = "D"
    MONTHLY = "M"


class Parameter(StrEnum):
    """
    The different meteorological parameters supported by Meteostat
    """

    TEMP = "temp"  # Air temperature at time of observation
    TAVG = "tavg"  # Average air temperature
    TMIN = "tmin"  # Absolute minimum air temperature
    TMAX = "tmax"  # Absolute maximum air temperature
    TAMN = "tamn"  # Average minimum air temperature
    TAMX = "tamx"  # Average maximum air temperature
    DWPT = "dwpt"  # Dew point (aggregation: mean)
    PRCP = "prcp"  # Precipitation (aggregation: sum)
    PDAY = "pday"  # Days with precipitation equal to or greater than 1 millimeter
    WDIR = "wdir"  # Wind direction at observation time
    WSPD = "wspd"  # Wind speed (aggregation: mean)
    WPGT = "wpgt"  # Peak wind gust (aggregation: max)
    RHUM = "rhum"  # Relative humidity (aggregation: mean)
    PRES = "pres"  # Air pressure at MSL (aggregation: mean)
    SNWD = "snwd"  # Snow depth on ground
    SNOW = "snow"  # Snowfall (aggregation: sum)
    TSUN = "tsun"  # Sunshine duration (aggregation: sum)
    SGHI = "sghi"  # TBD
    SDNI = "sdni"  # TBD
    SDHI = "sdhi"  # TBD
    CLDC = "cldc"  # Cloud cover (aggregation: mean)
    VSBY = "vsby"  # Visibility (aggregation: mean)
    COCO = "coco"  # Weather condition code at time of observation


class Provider(StrEnum):
    """
    Providers supported by Meteostat
    """

    ISD_LITE = "isd_lite"
    METAR = "metar"
    GHCND = "ghcnd"
    DWD_HOURLY = "dwd_hourly"
    DWD_POI = "dwd_poi"
    DWD_MOSMIX = "dwd_mosmix"
    DWD_DAILY = "dwd_daily"
    DWD_MONTHLY = "dwd_monthly"
    ECCC_HOURLY = "eccc_hourly"
    ECCC_DAILY = "eccc_daily"
    ECCC_MONTHLY = "eccc_monthly"
    METNO_FORECAST = "metno_forecast"

    HOURLY = "hourly"
    DAILY = "daily"
    DAILY_DERIVED = "daily_derived"
    MONTHLY = "monthly"
    MONTHLY_DERIVED = "monthly_derived"


class Priority(IntEnum):
    """
    Provider priorities
    """

    HIGHEST = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    LOWEST = 1


class TTL(IntEnum):
    """
    Cache TTLs
    """

    HOUR = 60 * 60
    DAY = 60 * 60 * 24
    WEEK = 60 * 60 * 24 * 7
    MONTH = 60 * 60 * 24 * 30
