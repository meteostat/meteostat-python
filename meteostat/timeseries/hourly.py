"""
Hourly time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import Tuple, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.core.loader import load_ts
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.utils.parsers import (
    parse_parameters,
    parse_providers,
    parse_station,
    parse_time,
)

SUPPORTED_PARAMETERS = (
    Parameter.TEMP,
    Parameter.DWPT,
    Parameter.PRCP,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.RHUM,
    Parameter.PRES,
    Parameter.SNOW,
    Parameter.TSUN,
    Parameter.COCO,
)

SUPPORTED_PROVIDERS = (
    Provider.HOURLY,
    Provider.SYNOP,
    Provider.METAR,
    Provider.MOSMIX,
    Provider.NOAA_ISD_LITE,
    Provider.DWD_CLIMATE_HOURLY,
)

DEFAULT_PARAMETERS = (
    Parameter.TEMP,
    Parameter.PRCP,
    Parameter.WSPD,
    Parameter.WDIR,
    Parameter.RHUM,
    Parameter.PRES,
)


def hourly(
    station: str | Tuple[str, ...] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    timezone: Optional[str] = None,
    parameters: Tuple[Parameter | str, ...] = DEFAULT_PARAMETERS,
    providers: Tuple[Provider | str, ...] = (Provider.HOURLY,),
    lite=True,
):
    """
    Retrieve hourly time series data
    """
    return load_ts(
        Granularity.HOURLY,
        parse_providers(providers, SUPPORTED_PROVIDERS),
        parse_parameters(parameters, SUPPORTED_PARAMETERS),
        parse_station(station),
        parse_time(start, timezone),
        parse_time(end, timezone, is_end=True),
        timezone,
        lite,
    )
