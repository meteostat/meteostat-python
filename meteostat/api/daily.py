"""
Daily time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import Optional
from datetime import datetime
from meteostat import Parameter, Provider, Granularity
from meteostat.api.stations import meta
from meteostat.core.logger import logger
from meteostat.core.loader import load_data
from meteostat.enumerations import Granularity
from meteostat.utils.parsers import parse_time
from meteostat.utils.validators import validate_parameters
from .timeseries import Timeseries

SUPPORTED_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.WDIR,
    Parameter.WSPD,
    Parameter.WPGT,
    Parameter.PRES,
    Parameter.SNOW,
    Parameter.TSUN,
]

DEFAULT_PARAMETERS = [
    Parameter.TAVG,
    Parameter.TMIN,
    Parameter.TMAX,
    Parameter.PRCP,
    Parameter.WSPD,
    Parameter.WDIR,
    Parameter.PRES,
]


def daily(
    station: list[str] | str,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    parameters: list[Parameter] = DEFAULT_PARAMETERS,
    providers: Optional[list[Provider]] = [Provider.COMPOSITE_DAILY],
    lite=True,
    max_station_count=None,
):
    """
    Retrieve daily time series data
    """
    logger.info(
        f"daily called for {len(station) if isinstance(station, list) else 1} station(s)"
    )
    # Log warning if request includes unsupported parameter(s)
    validate_parameters(SUPPORTED_PARAMETERS, parameters)
    # Get meta data for all station IDs
    stations = list(map(meta, [station] if isinstance(station, str) else station))
    # Parse start & end time
    start = parse_time(start)
    end = parse_time(end, is_end=True)
    # Gather data
    res = load_data(
        Granularity.DAILY,
        providers,
        parameters,
        stations,
        start,
        end,
        lite,
        max_station_count,
    )
    # Return Timerseries
    return Timeseries(Granularity.DAILY, res["stations"], res["df"], start, end)
