from typing import Literal, Optional
from datetime import datetime
from importlib import import_module
import pandas as pd
from meteostat import Parameter, providers
from meteostat.stations import meta
from meteostat.types import Station
from .exceptions import ParameterException
from meteostat.utilities.time import parse_time

def validate_parameters(supported_parameters: list[Parameter], requested_parameters: list[Parameter]) -> None:
    if not requested_parameters:
        return None
    diff = set(requested_parameters).difference(set(supported_parameters))
    if len(diff):
        raise ParameterException(f'Tried to request data for unsupported parameters: {", ".join([p.value for p in diff])}')

def call_provider(provider, station, start, end) -> pd.DataFrame:
    details = providers.get(provider)
    handler = import_module(details['handler'])
    df = handler.handler(station, start, end)
    df['station'] = station['id']
    return df.set_index("station", append=True)

def gather_data(
    stations: list[Station],
    start: datetime,
    end: datetime = None,
    parameters: Optional[list[str]] = None,
    providers: Optional[list[Literal]] = None,
    squash = True
) -> pd.DataFrame:
    data = []
    for station in stations:
        for provider in providers:
            data.append(call_provider(provider, station, start, end))
    return pd.concat(data)