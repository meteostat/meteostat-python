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
from meteostat.core.logger import logger
from meteostat.core.meta import filter_providers, get_parameter
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.enumerations import Granularity, Parameter
from meteostat.typing import QueryDict, StationDict
from meteostat.utils.filters import filter_parameters, filter_time
from meteostat.utils.helpers import get_intersection


def fetch_data(provider_module, query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch data from a given provider module
    """
    module = import_module(provider_module)
    df = module.fetch(query)
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


def load_ts(
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

    # Collect data
    fragments = []
    included_stations: list[StationDict] = []

    # Go through all weather stations
    for station in stations:
        # Collect data for current weather station
        station_fragments = []
        # Go through all applicable providers
        for provider in filter_providers(
            granularity, parameters, providers, station["country"], start, end
        ):
            try:
                # Fetch DataFrame for given provider
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
                df["source"] = provider["id"]
                df.set_index(["source"], append=True, inplace=True)
                # Filter DataFrame for requested parameters and time range
                df = filter_parameters(df, parameters)
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
                        pd.concat(station_fragments),
                        start,
                        end,
                    ).completeness()
                    == 1
                ):
                    break
            except Exception as error:
                logger.error(error)
        # Save weather station & corresponding weather data
        if station_fragments:
            fragments.append(station_fragments)
            included_stations.append(station)

    # Merge data in a single DataFrame
    df = pd.concat(chain.from_iterable(fragments)) if fragments else pd.DataFrame()

    # Only included requested coplumns
    df = df[get_intersection(parameters, df.columns.to_list())]

    # Convert columns to correct data type
    dtypes = {p["id"].value: p["dtype"] for p in [get_parameter(p) for p in parameters]}
    for col, dtype in dtypes.items():
        if dtype == 'Int64':
            df[col] = pd.to_numeric(df[col]).round(0)
    df = df.astype(dtypes)

    # Return final time series
    return TimeSeries(
        granularity, stations_to_df(included_stations), df, start, end, timezone
    )
