"""
Miscellaneous helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import itertools
from collections import Counter
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


def get_provider_priority(id: str) -> int:
    """
    Get priority of a provider by its ID
    """
    BASELINES = {
        Granularity.HOURLY: 0,
        Granularity.DAILY: 100,
        Granularity.MONTHLY: 200,
        Granularity.NORMALS: 300,
    }

    provider = next(
        (provider for provider in ALL_PROVIDERS if provider["id"] == id), None
    )

    baseline = BASELINES[provider["granularity"]]

    return int((Priority.NONE if not provider else provider["priority"]) + baseline)


def get_source_priority(source: str) -> int:
    """
    Get priority of a source string
    """
    providers = source.split(" ")

    if len(providers) == 1:
        return get_provider_priority(providers[0])

    priorities = [get_provider_priority(provider) for provider in providers]

    return min(priorities)


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
    Concatenate multiple data sources into a unique source string,
    ordered by the number of occurrences.
    """
    # Extract sources and flatten them
    sources = [str(item) for item in series if pd.notna(item)]
    flat_sources = list(itertools.chain(*[source.split() for source in sources]))

    # Count occurrences of each source
    source_counts = Counter(flat_sources)

    # Sort sources by count in descending order
    sorted_sources = sorted(source_counts, key=source_counts.get, reverse=True)

    # Concatenate sorted sources into a unique source string
    return " ".join(sorted_sources)


def order_source_columns(columns: pd.Index) -> List[str]:
    """
    Order source columns
    """
    ordered_columns = []

    for col in columns:
        if not col.endswith("_source"):
            ordered_columns.append(col)
            ordered_columns.append(f"{col}_source")

    return ordered_columns
