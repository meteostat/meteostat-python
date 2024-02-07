"""
Daily time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import date, datetime
from typing import List, Optional, Union

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
    Parameter.TAVG,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.SNOW,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.TSUN,
]

SUPPORTED_PROVIDERS = [Provider.BULK_DAILY, Provider.DWD_DAILY, Provider.GHCND]

DEFAULT_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.WSPD,
    Parameter.WDIR,
    Parameter.PRES,
]


def daily(
    station: str | List[str] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = (Provider.BULK_HOURLY,),
    lite=True,
):
    """
    Retrieve daily time series data
    """
    # Gather data
    return load_ts(
        Granularity.DAILY,
        parse_providers(providers, SUPPORTED_PROVIDERS),
        parse_parameters(parameters, SUPPORTED_PARAMETERS),
        parse_station(station),
        parse_time(start),
        parse_time(end, is_end=True),
        None,
        lite,
    )