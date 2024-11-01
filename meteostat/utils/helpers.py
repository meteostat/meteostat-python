"""
Miscellaneous helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import itertools
from typing import Any, Iterable, List, Tuple
import numpy as np
import pandas as pd
from meteostat.enumerations import Granularity, Priority
from meteostat.model import ALL_PROVIDERS
from meteostat.typing import StationDict


def get_freq(granularity: Granularity) -> str:
    """
    Convert granularity to frequency
    """
    return "1h" if granularity is Granularity.HOURLY else "1D"


def stations_to_df(stations: Tuple[StationDict]) -> pd.DataFrame:
    """
    TODO: Rename to join_station_details and provide drop_station_details, move to mutations

    Add the weather station's meta data to a given DataFrame
    """
    return pd.DataFrame.from_records(
        [
            {
                "id": station["id"],
                "latitude": station["location"]["latitude"],
                "longitude": station["location"]["longitude"],
                "elevation": station["location"]["elevation"],
            }
            for station in stations
        ],
        index="id",
    )


def get_distance(lat1, lon1, lat2, lon2) -> int:
    """
    Calculate distance between weather station and geo point
    """
    # Earth radius in meters
    radius = 6371000

    # Degress to radian
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])

    # Deltas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate distance
    arch = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    arch_sin = 2 * np.arcsin(np.sqrt(arch))

    return round(radius * arch_sin)


def get_provider_priority(id: str) -> Priority:
    """
    A factory function for getting the provider priority
    """

    provider = next(
        (provider for provider in ALL_PROVIDERS if provider["id"] == id), None
    )
    return Priority.LOWEST if not provider else provider["priority"]


def get_index(obj: Iterable, index: int, default=None) -> Any:
    try:
        return obj[index]
    except TypeError:
        return default


def get_intersection(list1, list2) -> List[Any]:
    set1 = set(list1)
    set2 = set(list2)
    intersection_set = set1.intersection(set2)

    intersection_list = [item for item in list1 if item in intersection_set]

    return intersection_list


def aggregate_sources(series: pd.Series) -> str:
    """
    Concatenate multiple data sources into a unique source string
    """
    sources = [str(item) for item in series if pd.notna(item)]
    flat_sources = set(itertools.chain(*[source.split() for source in sources]))
    return " ".join(flat_sources)
