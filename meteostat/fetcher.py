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
from pulire import Schema
from meteostat.logger import logger
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.enumerations import Granularity
from meteostat.typing import ProviderDict, QueryDict, StationDict
from meteostat.utils.filters import filter_providers, filter_time


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


def concat_fragments(fragments: List[pd.DataFrame], schema: Schema) -> pd.DataFrame:
    """
    Concatenate multiple fragments into a single DataFrame
    """
    try:
        df = pd.concat(
            [df.dropna(how="all", axis=1) if not df.empty else None for df in fragments]
        )
        df = schema.fill(df)
        df = schema.purge(df)
        return df
    except ValueError:
        return pd.DataFrame()


def fetch_ts(
    granularity: Granularity,
    providers: List[ProviderDict],
    schema: Schema,
    stations: List[StationDict],
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    timezone: Optional[str] = None,
    lite: bool = True,
) -> TimeSeries:
    """
    Load meteorological time series data from different providers
    """
    logger.debug(f"{granularity} time series requested for {len(stations)} station(s)")

    fragments = []
    included_stations: list[StationDict] = []
    included_providers: list[ProviderDict] = []

    # Go through all weather stations
    for station in stations:
        station_fragments = []  # DataFrame fragments for current weather station

        # Go through all applicable providers
        for provider in filter_providers(
            granularity, schema.names, providers, station["country"], start, end
        ):
            try:
                # Fetch DataFrame for current provider
                query = QueryDict(
                    {
                        "station": station,
                        "start": start if start else provider["start"],
                        "end": end if end else (provider.get("end", datetime.now())),  # type: ignore
                        "parameters": schema.names,
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

                # Add provider to list of included providers
                included_providers.append(provider)

                # Exit loop if request is satisfied
                if (
                    lite
                    and TimeSeries(
                        Granularity.HOURLY,
                        schema,
                        included_providers,
                        [station],
                        concat_fragments(station_fragments, schema),
                        start,
                        end,
                    ).completeness()
                    == 1
                ):
                    break

            except Exception:
                logger.error(f'Could not fetch data for provider "{provider["id"]}"', exc_info=True)

        # Save weather station & corresponding weather data
        if len(station_fragments):
            fragments.append(station_fragments)
            included_stations.append(station)

    # Merge data in a single DataFrame
    df = (
        concat_fragments(chain.from_iterable(fragments), schema)
        if fragments
        else pd.DataFrame()
    )

    # Set data types
    df = schema.format(df)

    # Return final time series
    return TimeSeries(
        granularity,
        schema,
        included_providers,
        stations_to_df(included_stations),
        df,
        start,
        end,
        timezone,
    )
