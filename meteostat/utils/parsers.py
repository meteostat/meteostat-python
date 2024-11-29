"""
Data parsers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

import calendar
from typing import Iterator, List
import datetime
import pandas as pd
from pulire import Schema
import pytz
import meteostat as ms
from meteostat.enumerations import Provider
from meteostat.typing import ProviderDict, StationDict


def parse_station(
    station: str | StationDict | List[str | StationDict] | pd.Index | pd.Series,
) -> List[StationDict]:
    """
    Parse one or multiple station(s) or a geo point
    """
    if isinstance(station, dict):
        return [station]

    data = []

    for s in [station] if isinstance(station, str) else list(station):
        if isinstance(s, dict):
            data.append(s)
        meta = ms.station(s)
        if meta is None:
            raise ValueError(f'Weather station with ID "{s}" could not be found')
        data.append(meta)

    return data


def parse_providers(
    requested: List[Provider], supported: List[ProviderDict]
) -> Iterator[ProviderDict]:
    """
    Raise exception if a requested provider is not supported
    """
    # Convert providers to set
    providers = list(
        map(lambda p: p if isinstance(p, Provider) else Provider[p], requested)
    )
    # Get difference between providers and supported providers
    diff = set(providers).difference([provider["id"] for provider in supported])
    # Log warning
    if len(diff):
        raise ValueError(
            f"""Tried to request data for unsupported provider(s): {
            ", ".join([p for p in diff])
        }"""
        )
    # Return intersection
    return filter(lambda provider: provider["id"] in requested, supported)


def get_schema(root_schema: Schema, parameters: List[ms.Parameter]) -> Schema:
    """
    Raise exception if a requested parameter is not part of the schema
    """
    # Get difference between requested parameters and root schema
    diff = set(parameters).difference(root_schema.names)
    # Log warning
    if len(diff):
        raise ValueError(
            f"""Tried to request data for unsupported parameter(s): {
            ", ".join([p for p in diff])
        }"""
        )
    # Return intersection
    return root_schema[parameters]


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

    if not isinstance(value, datetime.datetime):
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


def parse_month(
    value: datetime.date | datetime.datetime | None, is_end: bool = False
) -> datetime.date | None:
    """
    Convert a given date/time input to the first or last day of the month respectively
    """
    if not value:
        return None

    last_day = calendar.monthrange(value.year, value.month)[1]

    return datetime.date(value.year, value.month, last_day if is_end else 1)


def parse_year(year: int, is_end: bool = False) -> datetime.date:
    return datetime.date(year, 12, 31) if is_end else datetime.date(year, 1, 1)
