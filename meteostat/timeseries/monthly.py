"""
Monthly time series data

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
    PROVIDER_MONTHLY,
    PROVIDER_MONTHLY_DERIVED,
    PROVIDER_DWD_MONTHLY,
    PROVIDER_ECCC_MONTHLY,
)
from meteostat.utils.parsers import (
    parse_month,
    parse_parameters,
    parse_providers,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    PROVIDER_DWD_MONTHLY,
    PROVIDER_ECCC_MONTHLY,
    PROVIDER_MONTHLY,
    PROVIDER_MONTHLY_DERIVED,
]
SUPPORTED_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TAMN,
    Parameter.TAMX,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.PRES,
    Parameter.TSUN,
]
DEFAULT_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TAMN,
    Parameter.TAMX,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.PRES,
    Parameter.TSUN,
]


def monthly(
    station: str | List[str] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = [Provider.MONTHLY],
    lite=True,
):
    """
    Retrieve monthly time series data
    """
    return fetch_ts(
        Granularity.MONTHLY,
        parse_providers(providers, SUPPORTED_PROVIDERS),
        parse_parameters(parameters, SUPPORTED_PARAMETERS),
        parse_station(station),
        parse_time(parse_month(start)),
        parse_time(parse_month(end, is_end=True), is_end=True),
        None,
        lite,
    )
