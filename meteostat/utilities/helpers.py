"""
Utilities - Helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import Optional
import numpy as np


def get_distance(lat1, lon1, lat2, lon2) -> float:
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

    return radius * arch_sin


def _get_flag_from_single_source(
    source: str, source_mappings: dict, model_flag: str
) -> str:
    """
    Get flag from single source
    """
    if source in source_mappings:
        return source_mappings[source]
    return model_flag


def get_flag_from_source_factory(source_mappings: dict, model_flag: str) -> str:
    """
    Get flag from source
    """

    def _get_flag_from_source(source: Optional[str]) -> str:
        sources = source.split(" ")

        flags = [
            _get_flag_from_single_source(src, source_mappings, model_flag)
            for src in sources
        ]

        return "".join(flags)

    return _get_flag_from_source


def with_suffix(items, suffix):
    """
    Takes a list of strings and a suffix, returns a new list containing
    the same items with the suffix added.
    """
    return [item + suffix for item in items]
