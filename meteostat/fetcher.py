"""
Load meteorological data from providers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The cod is licensed under the MIT license.
"""

from datetime import datetime
from importlib import import_module
from itertools import chain
from typing import List, Optional
import pandas as pd
from meteostat import Provider
from meteostat.logger import logger
from meteostat.model import PARAMETER_DTYPES
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.enumerations import Granularity, Parameter
from meteostat.typing import QueryDict, StationDict
from meteostat.utils.filters import filter_parameters, filter_providers, filter_time
from meteostat.utils.helpers import get_intersection


def fetch_data(provider_module, query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch data from a given provider module
    """
    module = import_module(provider_module)
    df = module.fetch(query)
    return df


def add_source(df: pd.DataFrame, provider_id: str) -> pd.DataFrame:
    """
    Add source column to DataFrame
    """
    if not "source" in df.index.names:
        df["source"] = provider_id
        df.set_index(["source"], append=True, inplace=True)
    return df


def set_dtypes(df: pd.DataFrame, parameters) -> pd.DataFrame:
    """
    Convert columns to correct data type
    """
    dtypes = {p.value: PARAMETER_DTYPES[p] for p in parameters}
    for col, dtype in dtypes.copy().items():
        if col not in df:
            del dtypes[col]
            continue
        if dtype == "Int64":
            df[col] = pd.to_numeric(df[col]).round(0)
    return df.astype(dtypes, errors="ignore")


def stations_to_df(stations: List[StationDict]) -> pd.DataFrame | None:
    """
    Convert list of weather stations to DataFrame
    """
    return (
        pd.DataFrame.from_records(
            [
                {
                    "id": station["id"],
                    "name": station["name"]["en"],
                    "country": station["country"],
                    "latitude": station["location"]["latitude"],
                    "longitude": station["location"]["longitude"],
                    "elevation": station["location"]["elevation"],
                    "timezone": station["timezone"],
                }
                for station in stations
            ],
            index="id",
        )
        if len(stations)
        else []
    )


def concat_fragments(fragments: List[pd.DataFrame], parameters: List[Parameter]) -> pd.DataFrame:
    """
    Concatenate multiple fragments into a single DataFrame
    """
    df = pd.concat(
        [df.dropna(how='all', axis=1) if not df.empty else None for df in fragments]
    )
    return filter_parameters(df, parameters)


def fetch_ts(
    granularity: Granularity,
    providers: List[Provider],
    parameters: List[Parameter],
    stations: List[StationDict],
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    timezone: Optional[str] = None,
    lite: bool = True,
) -> TimeSeries:
    """
    Load meteorological time series data from different providers
    """
    logger.info(f"{granularity} time series requested for {len(stations)} station(s)")

    fragments = []  # DataFrame fragments across all weather stations and providers
    included_stations: list[
        StationDict
    ] = []  # List of weather stations which returned data

    # Go through all weather stations
    for station in stations:
        station_fragments = []  # DataFrame fragments for current weather station

        # Go through all applicable providers
        for provider in filter_providers(
            granularity, parameters, providers, station["country"], start, end
        ):
            try:
                # Fetch DataFrame for current provider
                query = QueryDict(
                    {
                        "station": station,
                        "start": start if start else provider["start"],
                        "end": end if end else (provider.get("end", datetime.now())),  # type: ignore
                        "parameters": parameters,
                    }
                )
                df = fetch_data(provider["module"], query)

                # Continue if no data was returned
                if df is None:
                    continue

                # Add current station ID to DataFrame
                df = pd.concat([df], keys=[station["id"]], names=["station"])

                # Add source index column to DataFrame
                df = add_source(df, provider["id"])

                # Filter DataFrame for requested parameters and time range
                df = filter_time(df, start, end)

                # Drop empty rows
                df = df.dropna(how="all")

                # Save DataFrame
                station_fragments.append(df)

                # Exit loop if request is satisfied
                if (
                    lite
                    and TimeSeries(
                        Granularity.HOURLY,
                        [station],
                        concat_fragments(station_fragments, parameters),
                        start,
                        end,
                    ).completeness()
                    == 1
                ):
                    break

            except Exception as error:
                logger.error(error)

        # Save weather station & corresponding weather data
        if len(station_fragments):
            fragments.append(station_fragments)
            included_stations.append(station)

    # Merge data in a single DataFrame
    df = concat_fragments(chain.from_iterable(fragments), parameters) if fragments else pd.DataFrame()
    # Only included requested coplumns
    df = df[get_intersection(parameters, df.columns.to_list())]
    # Set data types
    df = set_dtypes(df, parameters)

    # Return final time series
    return TimeSeries(
        granularity, stations_to_df(included_stations), df, start, end, timezone
    )
