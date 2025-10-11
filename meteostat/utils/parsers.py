"""
Data parsers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

import calendar
from typing import List
import datetime
import pandas as pd
import pytz
from meteostat.api.station import station as get_station
from meteostat.api.point import Point
from meteostat.enumerations import Parameter
from meteostat.typing import Station


def parse_station(
    station: (
        str
        | Station
        | Point
        | List[str | Station | Point]
        | pd.Index
        | pd.Series
        | pd.DataFrame
    ),
) -> List[Station]:
    """
    Parse one or multiple station(s) or a geo point

    Point objects are converted to virtual stations with IDs like $0001, $0002, etc.
    based on their position in the input list.
    """
    # Return data if it contains station meta data
    if isinstance(station, Station):
        return [station]

    # Handle Point objects
    if isinstance(station, Point):
        return [_point_to_station(station, 1)]

    # Convert station identifier(s) to list
    if isinstance(station, pd.Series) or isinstance(station, pd.DataFrame):
        stations = station.index.tolist()
    elif isinstance(station, pd.Index):
        stations = station.tolist()
    elif isinstance(station, str):
        stations = [station]
    else:
        stations = station

    # Get station meta data
    data = []
    point_counter = 0
    for s in stations:
        # Append data early if it contains station meta data
        if isinstance(s, Station):
            data.append(s)
            continue
        # Handle Point objects
        if isinstance(s, Point):
            point_counter += 1
            data.append(_point_to_station(s, point_counter))
            continue
        # Get station meta data
        meta = get_station(s)
        # Raise exception if station could not be found
        if meta is None:
            raise ValueError(f'Weather station with ID "{s}" could not be found')
        # Append station meta data
        data.append(meta)

    # Return station meta data
    return data


def _point_to_station(point: Point, index: int) -> Station:
    """
    Convert a Point object to a virtual Station object

    Parameters
    ----------
    point : Point
        The Point object to convert
    index : int
        The position in the list of points (1-indexed)

    Returns
    -------
    Station
        A virtual Station object with an ID like $0001
    """
    # Create virtual station ID
    station_id = f"${index:04d}"

    # Create Station object with Point as location
    return Station(
        id=station_id,
        location=point,
        latitude=point.latitude,
        longitude=point.longitude,
        elevation=point.elevation,
    )


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
