"""
Hourly Time Series Data

Access hourly time series data for one or multiple weather stations.
"""

from typing import List, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.core.data import data_service
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.typing import Station, Request
from meteostat.api.point import Point
from meteostat.utils.parsers import parse_station, parse_time

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
    station: str | Station | Point | List[str | Station | Point] | pd.Index | pd.Series,
    start: Optional[datetime | date],
    end: Optional[datetime | date],
    timezone: Optional[str] = None,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.HOURLY],
    model: bool = True,
):
    """
    Access hourly time series data.

    Parameters
    ----------
    station : str, Station, Point, List[str | Station | Point], pd.Index, pd.Series
        Weather station(s) or Point(s) to query data for. Can be a single station/point or a list.
        Points are converted to virtual stations with IDs like $0001, $0002, etc.
    start : datetime, date, optional
        Start date for the data query. If None, the earliest available date will be used.
    end : datetime, date, optional
        End date for the data query. If None, the latest available date will be used.
    timezone : str, optional
        Time zone for the data query. If None, UTC will be used.
    parameters : List[Parameter], optional
        List of parameters to include in the data query. Defaults to a set of common parameters.
    providers : List[Provider], optional
        List of data providers to use for the query. Defaults to the hourly provider.
    model : bool, optional
        Whether to include model data in the query. Defaults to True.

    Returns
    -------
    TimeSeries
        A TimeSeries object containing the hourly data for the specified stations and parameters.
    """
    parsed_stations = parse_station(station)

    # Determine if multi-station and convert to list
    if isinstance(parsed_stations, list):
        stations = parsed_stations
        multi_station = True
    else:
        stations = [parsed_stations]
        multi_station = False

    req = Request(
        granularity=Granularity.HOURLY,
        providers=providers,
        parameters=parameters,
        stations=stations,
        start=parse_time(start, timezone),
        end=parse_time(end, timezone, is_end=True),
        timezone=timezone,
        model=model,
        multi_station=multi_station,
    )

    return data_service.fetch(req)
