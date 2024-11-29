"""
Daily time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import date, datetime
from typing import List, Optional, Union

import pandas as pd
from meteostat.fetcher import fetch_ts
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.model import (
    PROVIDER_DAILY,
    PROVIDER_DAILY_DERIVED,
    PROVIDER_DWD_DAILY,
    PROVIDER_ECCC_DAILY,
    PROVIDER_GHCND,
)
from meteostat.schema import DAILY_SCHEMA
from meteostat.utils.parsers import (
    get_schema,
    parse_providers,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    PROVIDER_DWD_DAILY,
    PROVIDER_ECCC_DAILY,
    PROVIDER_GHCND,
    PROVIDER_DAILY_DERIVED,
    PROVIDER_DAILY,
]
DEFAULT_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.RHUM,
    Parameter.PRCP,
    Parameter.SNWD,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.TSUN,
    Parameter.CLDC,
]


def daily(
    station: str | List[str] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = [Provider.DAILY],
    lite=True,
):
    """
    Retrieve daily time series data
    """
    schema = get_schema(DAILY_SCHEMA, parameters)

    return fetch_ts(
        Granularity.DAILY,
        parse_providers(providers, SUPPORTED_PROVIDERS),
        schema,
        parse_station(station),
        parse_time(start),
        parse_time(end, is_end=True),
        None,
        lite,
    )
