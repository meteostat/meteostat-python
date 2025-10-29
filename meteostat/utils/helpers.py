"""
Miscellaneous helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import itertools
from collections import Counter
from typing import Any, Iterable, List

import numpy as np
import pandas as pd


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


def get_index(obj: Iterable, index: int, default=None) -> Any:
    """
    Get an item from an iterable by index, returning a default value if not accessible
    """
    try:
        return obj[index]
    except TypeError:
        return default


def get_intersection(list1, list2) -> List[Any]:
    """
    Get the intersection of two lists while preserving the order from list1
    """
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
