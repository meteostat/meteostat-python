from typing import Literal, Optional
from datetime import datetime
from meteostat import Parameter, Granularity
from meteostat.stations import meta
from meteostat.core import logger, loader
from meteostat.utilities.time import parse_time
from .timeseries import Timeseries

SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.PRCP,
    Parameter.RHUM
]

def hourly(
    stations: list[str] | str,
    start: str | datetime,
    end: str | datetime = None,
    parameters: Optional[list[str]] = None,
    providers: Optional[list[Literal]] = None,
    squash = True
):
    """
    Retrieve hourly time series data
    """
    logger.info(f'timeseries.hourly called for {len(stations) if isinstance(stations, list) else 1} station(s) with start={start} and end={end}')
    loader.validate_parameters(SUPPORTED_PARAMETERS, parameters)
    stations = list(map(meta, [stations] if isinstance(stations, str) else stations))
    start = parse_time(start)
    end = parse_time(end, start)
    df = loader.gather_data(stations, start, end, parameters, providers, squash)
    return Timeseries(Granularity.HOURLY, stations, df, 24)