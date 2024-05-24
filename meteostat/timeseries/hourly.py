"""
Hourly time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import List, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.fetcher import fetch_ts
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.utils.parsers import (
    parse_parameters,
    parse_providers,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    Provider.DWD_HOURLY,
    Provider.ISD_LITE,
    Provider.SYNOP,
    Provider.METAR,
    Provider.MODEL,
    Provider.BULK_HOURLY,
]
SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.DWPT,
    Parameter.RHUM,
    Parameter.PRCP,
    Parameter.SNOW,
    Parameter.SNWD,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.TSUN,
    Parameter.CLDC,
    Parameter.VSBY,
    Parameter.COCO,
]
DEFAULT_PARAMETERS = [
    Parameter.TEMP,
    Parameter.RHUM,
    Parameter.PRCP,
    Parameter.SNWD,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.TSUN,
    Parameter.CLDC,
    Parameter.COCO,
]


def hourly(
    station: str | List[str] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    timezone: Optional[str] = None,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = [Provider.BULK_HOURLY],
    lite=True,
):
    """
    Retrieve hourly time series data
    """
    return fetch_ts(
        Granularity.HOURLY,
        parse_providers(providers, SUPPORTED_PROVIDERS),
        parse_parameters(parameters, SUPPORTED_PARAMETERS),
        parse_station(station),
        parse_time(start, timezone),
        parse_time(end, timezone, is_end=True),
        timezone,
        lite,
    )
