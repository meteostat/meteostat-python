"""
Daily Data

Access daily time series data for one or multiple weather stations.
"""

from datetime import date, datetime
from typing import List, Optional, Union

import pandas as pd
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.providers.index import (
    PROVIDER_DAILY,
    PROVIDER_DAILY_DERIVED,
    PROVIDER_DWD_DAILY,
    PROVIDER_ECCC_DAILY,
    PROVIDER_GHCND,
)
from meteostat.schema import DAILY_SCHEMA
from meteostat.utils.parsers import (
    get_schema,
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
    Parameter.TEMP,
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
    max_stations=4,
):
    """
    Retrieve daily time series data
    """
    schema = get_schema(DAILY_SCHEMA, parameters)

    return data_service.fetch(
        granularity=Granularity.DAILY,
        providers=parse_providers(providers, SUPPORTED_PROVIDERS),
        schema=schema,
        stations=parse_station(station),
        start=parse_time(start),
        end=parse_time(end, is_end=True),
        timezone=None,
        lite=lite,
        max_stations=max_stations,
    )
