"""
Monthly Time Series Data

Access monthly time series data for one or multiple weather stations.
"""

from typing import List, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.typing import Station, Request
from meteostat.utils.parsers import parse_station, parse_time

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
    station: str | Station | List[str | Station] | pd.Index | pd.Series,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.MONTHLY],
    model: bool = True,
):
    """
    Access monthly time series data
    """
    req = Request(
        granularity=Granularity.MONTHLY,
        providers=providers,
        parameters=parameters,
        stations=parse_station(station),
        start=parse_time(start),
        end=parse_time(end, is_end=True),
        model=model,
    )

    return data_service.fetch(req)