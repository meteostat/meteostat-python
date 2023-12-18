"""
Load meteorological data from providers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

from typing import List
from datetime import datetime
from importlib import import_module
from itertools import chain
import pandas as pd
from meteostat import Provider, types
from meteostat.core.providers import filter_providers
from meteostat.api.timeseries import Timeseries
from meteostat.enumerations import Granularity, Parameter
from meteostat.utils.mutations import filter_parameters, filter_time


def fetch_data(provider_module, *args) -> pd.DataFrame:
    """
    Fetch data from a given provider module
    """
    module = import_module(provider_module)
    df = module.fetch(*args)
    return df


def call_providers(
    granularity: Granularity,
    parameters: List[Parameter],
    providers: List[Provider],
    station: types.Station,
    start: datetime,
    end: datetime,
    lite: bool,
    max_station_count: int | None,
) -> List[pd.DataFrame]:
    """
    Call providers to fetch data for a station
    """
    station_data = []
    for provider in filter_providers(
        granularity, parameters, providers, station["country"], start, end
    ):
        df = fetch_data(
            provider["module"],
            station,
            start if start else provider["start"],
            end if end else (provider.get("end", datetime.now())),
            parameters,
        )
        df = pd.concat([df], keys=[station["id"]], names=["station"])
        df["source"] = provider["id"].value
        df.set_index(["source"], append=True, inplace=True)
        df = filter_parameters(df, parameters)
        df = filter_time(df, start, end)
        df = df.dropna(how="all")
        station_data.append(df)
        if (
            lite
            and Timeseries(
                Granularity.HOURLY, [station], pd.concat(station_data), start, end
            ).coverage()
            == 1
        ):
            break
        if max_station_count and len(station_data) == max_station_count:
            break
    return station_data


def load_data(
    granularity: Granularity,
    providers: List[Provider],
    parameters: List[Parameter],
    stations: List[types.Station],
    start: datetime | None = None,
    end: datetime | None = None,
    lite: bool = True,
    max_station_count: int | None = None,
) -> types.LoaderResponse:
    """
    Load meteorological data from different providers
    """
    data = []
    included_stations = []

    for station in stations:
        station_data = call_providers(
            granularity,
            parameters,
            providers,
            station,
            start,
            end,
            lite,
            max_station_count,
        )
        if station_data:
            data.append(station_data)
            included_stations.append(station)
        if max_station_count and len(data) == max_station_count:
            break

    df = pd.concat(chain.from_iterable(data)) if data else pd.DataFrame()

    return types.LoaderResponse({"stations": included_stations, "df": df})
