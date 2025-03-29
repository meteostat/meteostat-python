"""
Functions for converting between different
meteorological data units

The code is licensed under the MIT license.
"""

import math
from typing import Optional
from numpy import isnan

from meteostat.enumerations import Parameter


def kelvin_to_celsius(value):
    """
    Convert Kelvin to Celsius
    """
    return value - 273.15 if value is not None and not isnan(value) else None


def ms_to_kmh(value):
    """
    # Convert m/s to km/h
    """
    return value * 3.6 if value is not None and not isnan(value) else None


def temp_dwpt_to_rhum(row: dict):
    """
    # Get relative humidity from temperature and dew point
    """
    return (
        100
        * (
            math.exp((17.625 * row["dwpt"]) / (243.04 + row["dwpt"]))
            / math.exp((17.625 * row["temp"]) / (243.04 + row["temp"]))
        )
        if row["temp"] is not None and row["dwpt"] is not None
        else None
    )


def pres_to_msl(row: dict, altitude: Optional[int] = None, temp: str = Parameter.TEMP):
    """
    # Convert local air pressure to MSL
    """
    try:
        return (
            None
            if (
                not row[Parameter.PRES]
                or not row[temp]
                or not altitude
                or row[Parameter.PRES] == -999
            )
            else round(
                row[Parameter.PRES]
                * math.pow(
                    (
                        1
                        - (
                            (0.0065 * altitude)
                            / (row[temp] + 0.0065 * altitude + 273.15)
                        )
                    ),
                    -5.257,
                ),
                1,
            )
        )
    except BaseException:
        return None


def percentage_to_okta(value):
    """
    Convert cloud cover percentage to oktas
    """
    return round(value / 12.5) if value is not None and not isnan(value) else None


def jcm2_to_wm2(value):
    """
    Convert Joule/CM^2 to Watt/M^2
    """
    return round(value * 2.78) if value is not None and not isnan(value) else None
