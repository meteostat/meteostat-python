"""
Useful utilities for parsing data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

from datetime import datetime
import pytz


def parse_time(
    value: str | datetime | None, timezone: str | None = None, is_end: bool = False
) -> datetime | None:
    """
    Convert a given date/time input to datetime

    To set the time of a date-only string to 23:59:59, pass is_end=True
    """
    if not value:
        return None

    if isinstance(value, str) and len(value) == 10:
        value = f"{value} 23:59:59" if is_end else f"{value} 00:00:00"
        value = datetime.fromisoformat(value)
    elif isinstance(value, str):
        value = datetime.fromisoformat(value)

    if timezone:
        timezone = pytz.timezone(timezone)
        value = value.astimezone(timezone).astimezone(pytz.utc).replace(tzinfo=None)

    return value
