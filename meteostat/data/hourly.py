from typing import Optional
from datetime import datetime
from meteostat import Parameter, Provider, Granularity
from meteostat.core.logger import logger
from meteostat.core.loader import (
    validate_parameters,
    load_stations,
    parse_time,
    load_data,
)
from meteostat.enumerations import Granularity
from .timeseries import Timeseries

SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.DWPT,
    Parameter.PRCP,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.RHUM,
    Parameter.PRES,
    Parameter.SNOW,
    Parameter.TSUN,
    Parameter.COCO,
]


def hourly(
    station: list[str] | str,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    timezone: str | None = None,
    parameters: list[Parameter] = [
        Parameter.TEMP,
        Parameter.PRCP,
        Parameter.WSPD,
        Parameter.WDIR,
        Parameter.RHUM,
        Parameter.PRES,
    ],
    providers: Optional[list[Provider]] = [Provider.COMPOSITE_HOURLY],
    lite=True,
    max_station_count=None,
):
    """
    Retrieve hourly time series data
    """
    logger.info(
        f"timeseries.hourly called for {len(station) if isinstance(station, list) else 1} station(s)"
    )
    # Raise exception if request includes unsupported parameter(s)
    validate_parameters(SUPPORTED_PARAMETERS, parameters)
    # Get meta data for all station IDs
    stations = load_stations(station)
    # Parse start & end time
    start = parse_time(start, timezone)
    end = parse_time(end, timezone, is_end=True)
    # Gather data
    res = load_data(
        Granularity.HOURLY,
        providers,
        parameters,
        stations,
        start,
        end,
        lite,
        max_station_count,
    )
    # Return Timerseries
    return Timeseries(
        Granularity.HOURLY, res["stations"], res["df"], start, end, timezone
    )
