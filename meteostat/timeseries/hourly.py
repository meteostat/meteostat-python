"""
Hourly time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import List, Union, Optional
from datetime import datetime, date
import pandas as pd
from meteostat.concat import concat
from meteostat.schema import HOURLY_SCHEMA
from meteostat.settings import settings
from meteostat.fetcher import fetch_ts
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.model import (
    PROVIDER_DWD_MOSMIX,
    PROVIDER_DWD_POI,
    PROVIDER_HOURLY,
    PROVIDER_DWD_HOURLY,
    PROVIDER_ECCC_HOURLY,
    PROVIDER_ISD_LITE,
    PROVIDER_METAR,
    PROVIDER_METAR_LEGACY,
    PROVIDER_METNO_FORECAST,
    PROVIDER_MODEL,
    PROVIDER_SYNOP,
)
from meteostat.point import Point
from meteostat.stations.nearby import nearby
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.typing import StationDict
from meteostat.utils.parsers import (
    get_schema,
    parse_providers,
    parse_station,
    parse_time,
)


SUPPORTED_PROVIDERS = [
    PROVIDER_DWD_HOURLY,
    PROVIDER_DWD_POI,
    PROVIDER_DWD_MOSMIX,
    PROVIDER_ECCC_HOURLY,
    PROVIDER_ISD_LITE,
    PROVIDER_METAR,
    PROVIDER_HOURLY,
    PROVIDER_METNO_FORECAST,
    PROVIDER_SYNOP,
    PROVIDER_METAR_LEGACY,
    PROVIDER_MODEL,
]
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
    station: str | StationDict | List[str | StationDict] | pd.Index | pd.Series | Point,
    start: Optional[Union[datetime, date]] = None,
    end: Optional[Union[datetime, date]] = None,
    timezone: Optional[str] = None,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.HOURLY],
    lite=True,
):
    """
    Retrieve hourly time series data
    """

    schema = get_schema(HOURLY_SCHEMA, parameters)

    def _fetch(s) -> TimeSeries:
        return fetch_ts(
            Granularity.HOURLY,
            parse_providers(providers, SUPPORTED_PROVIDERS),
            schema,
            parse_station(s),
            parse_time(start, timezone),
            parse_time(end, timezone, is_end=True),
            timezone,
            lite,
        )

    if isinstance(station, Point):
        nearby_stations = nearby(
            station.latitude, station.longitude, settings["point_radius"]
        )

        fragments = []

        for index, _row in nearby_stations.iterrows():
            ts = _fetch(index)
            if not ts.empty:
                fragments.append(ts)
            if len(fragments) == settings["point_stations"]:
                return concat(fragments)

    return _fetch(station)
