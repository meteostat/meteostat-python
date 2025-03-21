"""
Monthly Data

Access monthly time series data for one or multiple weather stations.
"""

from datetime import date, datetime
from typing import List, Optional, Union

import pandas as pd
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.providers.index import (
    PROVIDER_MONTHLY,
    PROVIDER_MONTHLY_DERIVED,
    PROVIDER_DWD_MONTHLY,
    PROVIDER_ECCC_MONTHLY,
)
from meteostat.schema import MONTHLY_SCHEMA
from meteostat.utils.parsers import (
    get_schema,
    parse_month,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    PROVIDER_DWD_MONTHLY,
    PROVIDER_ECCC_MONTHLY,
    PROVIDER_MONTHLY,
    PROVIDER_MONTHLY_DERIVED,
]
DEFAULT_PARAMETERS = [
    Parameter.TEMP,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.TXMN,
    Parameter.TXMX,
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
    max_stations=4,
):
    """
    Retrieve monthly time series data
    """
    schema = get_schema(MONTHLY_SCHEMA, parameters)

    return data_service(
        granularity=Granularity.MONTHLY,
        providers=parse_providers(providers, SUPPORTED_PROVIDERS),
        schema=schema,
        stations=parse_station(station),
        start=parse_time(parse_month(start)),
        end=parse_time(parse_month(end, is_end=True), is_end=True),
        timezone=None,
        lite=lite,
        max_stations=max_stations,
    )
