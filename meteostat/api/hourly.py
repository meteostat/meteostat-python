"""
Hourly Data

Access hourly time series data for one or multiple weather stations.
"""

from typing import List, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.api.point import Point
from meteostat.typing import Station, Request
from meteostat.utils.parsers import (
    parse_station,
    parse_time,
)

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
    station: str | Station | List[str | Station] | pd.Index | pd.Series | Point,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    timezone: Optional[str] = None,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.HOURLY],
    model: bool = True,
):
    """
    Retrieve hourly time series data
    """
    req = Request(
        granularity=Granularity.HOURLY,
        providers=providers,
        parameters=parameters,
        stations=parse_station(station),
        start=parse_time(start, timezone),
        end=parse_time(end, timezone, is_end=True),
        timezone=timezone,
        model=model,
    )

    return data_service.fetch(req)
