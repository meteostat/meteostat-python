from typing import Literal, Optional
from datetime import datetime

import pandas as pd
from meteostat import Parameter, Provider, Granularity, stations
from meteostat.core.logger import logger
from meteostat.core.providers import providers as providers_service
from meteostat.types import Station
from meteostat.utils.parameters import validate_parameters
from meteostat.utils.time import parse_time
from .timeseries import Timeseries

SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.PRCP,
    Parameter.RHUM
]

def hourly(
    station: list[str] | str,
    start: str | datetime,
    end: str | datetime = None,
    parameters: Optional[list[Parameter]] = None,
    providers: Optional[list[Provider]] = None,
    lite = True
):
    """
    Retrieve hourly time series data
    """
    logger.info(f'timeseries.hourly called for {len(station) if isinstance(station, list) else 1} station(s)')
    # Raise exception if request includes unsupported parameter(s)
    validate_parameters(SUPPORTED_PARAMETERS, parameters)
    # Get meta data for all station IDs
    station: list[Station | None] = list(map(stations.meta, [station] if isinstance(station, str) else station))
    # Parse start & end time
    start = parse_time(start)
    end = parse_time(end, start)
    # Gather data
    data = []
    for s in station:
        for provider in providers:
            df = providers_service.call_provider(provider, s, start, end)
            df = pd.concat([df], keys=[s['id']], names=['station'])
            df['source'] = provider.value
            df.set_index(['source'], append=True, inplace=True)
            data.append(df)
    df = pd.concat(data)
    # Return Timerseries
    return Timeseries(Granularity.HOURLY, station, df, 24)