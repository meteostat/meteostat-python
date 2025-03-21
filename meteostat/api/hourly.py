"""
Hourly Data

Access hourly time series data for one or multiple weather stations.
"""

from typing import List, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.schema import HOURLY_SCHEMA
from meteostat.core.providers import provider_service
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.api.point import Point
from meteostat.typing import Station, Request
from meteostat.utils.parsers import (
    get_schema,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    Provider.DWD_HOURLY,
    Provider.DWD_POI,
    Provider.DWD_MOSMIX,
    Provider.ECCC_HOURLY,
    Provider.ISD_LITE,
    Provider.METAR,
    Provider.HOURLY,
    Provider.METNO_FORECAST,
    Provider.SYNOP,
    Provider.METAR_LEGACY,
    Provider.MODEL,
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
    station: str | Station | List[str | Station] | pd.Index | pd.Series | Point,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    timezone: Optional[str] = None,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.HOURLY],
    model: bool = True,
    commercial: bool = False,
):
    """
    Retrieve hourly time series data
    """
    schema = get_schema(HOURLY_SCHEMA, parameters)

    req = Request(
        granularity=Granularity.HOURLY,
        providers=provider_service.parse_providers(providers, SUPPORTED_PROVIDERS),
        schema=schema,
        stations=parse_station(station),
        start=parse_time(start, timezone),
        end=parse_time(end, timezone, is_end=True),
        timezone=timezone,
        model=model,
        commercial=commercial,
    )

    return data_service.fetch(req)
