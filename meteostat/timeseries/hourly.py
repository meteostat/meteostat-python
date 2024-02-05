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
from meteostat.core.loader import load_ts
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.utils.parsers import (
    parse_parameters,
    parse_providers,
    parse_station,
    parse_time,
)

SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.DWPT,
    Parameter.RHUM,
    Parameter.PRCP,
    Parameter.SNWD,
    Parameter.SNOW,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.TSUN,
    Parameter.CLDC,
    Parameter.COCO,
]

SUPPORTED_PROVIDERS = [
    Provider.BULK_HOURLY,
    Provider.SYNOP,
    Provider.METAR,
    Provider.MOSMIX,
    Provider.ISD_LITE,
    Provider.DWD_HOURLY,
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
    providers: List[Provider | str] = (Provider.BULK_HOURLY,),
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
