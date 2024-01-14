"""
Data parsers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

from typing import Tuple
import datetime
import pandas as pd
import pytz
from meteostat import Parameter, stations
from meteostat.enumerations import Provider
from meteostat.typing import Station


def parse_station(
    station: str | Tuple[str, ...] | pd.Index | pd.Series,
) -> Tuple[Station, ...]:
    data = []

    for s in tuple(station):
        meta = stations.meta(s)
        if meta is None:
            raise ValueError(f'Weather station with ID "{s}" could not be found')
        data.append(meta)

    return tuple(data)


def parse_providers(
    requested: Tuple[Provider | str, ...], supported: Tuple[Provider, ...]
) -> Tuple[Provider, ...]:
    """
    Raise exception if a requested provider is not supported
    """
    # Convert providers to set
    providers = set(
        map(lambda p: p if isinstance(p, Provider) else Provider[p], requested)
    )
    # Get difference between providers and supported providers
    diff = providers.difference(supported)
    # Log warning
    if len(diff):
        raise ValueError(
            f"""Tried to request data for unsupported provider(s): {
            ", ".join([p for p in diff])
        }"""
        )
    # Return intersection
    return tuple(providers)


def parse_parameters(
    requested: Tuple[Parameter | str, ...], supported: Tuple[Parameter, ...]
) -> Tuple[Parameter, ...]:
    """
    Raise exception if a requested parameter is not supported
    """
    # Convert parameters to set
    parameters = set(
        map(lambda p: p if isinstance(p, Parameter) else Parameter[p], requested)
    )
    # Get difference between parameters and supported parameters
    diff = parameters.difference(supported)
    # Log warning
    if len(diff):
        raise ValueError(
            f"""Tried to request data for unsupported parameter(s): {
            ", ".join([p for p in diff])
        }"""
        )
    # Return intersection
    return tuple(parameters)


def parse_time(
    value: datetime.date | datetime.datetime | None,
    timezone: str | None = None,
    is_end: bool = False,
) -> datetime.datetime | None:
    """
    Convert a given date/time input to datetime

    To set the time of a date to 23:59:59, pass is_end=True
    """
    if not value:
        return None

    if isinstance(value, datetime.date):
        parsed = datetime.datetime.combine(
            value,
            datetime.datetime.max.time() if is_end else datetime.datetime.min.time(),
        )
    else:
        parsed = value

    if timezone:
        tz = pytz.timezone(timezone)
        parsed = parsed.astimezone(tz).astimezone(pytz.utc).replace(tzinfo=None)

    return parsed
