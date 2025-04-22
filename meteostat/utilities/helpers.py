"""
Utilities - Helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import Optional
import numpy as np


SOURCE_MAPPINGS: dict = {
    "metar": "D",
    "model": "E",
    "isd_lite": "B",
    "ghcnd": "B",
    "synop": "C",
    "dwd_poi": "C",
    "dwd_hourly": "A",
    "dwd_daily": "A",
    "dwd_monthly": "A",
    "dwd_mosmix": "E",
    "metno_forecast": "E",
    "eccc_hourly": "A",
    "eccc_daily": "A",
    "eccc_monthly": "A"
}


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


def _get_flag_from_single_source(source: str, source_mappings: dict) -> str:
    """
    Get flag from single source
    """
    if source in source_mappings:
        return source_mappings[source]
    return "E"

def get_flag_from_source_factory(source_mappings: dict) -> str:
    """
    Get flag from source
    """
    def _get_flag_from_source(source: Optional[str]) -> str:    
        sources = source.split(" ")

        flags = [_get_flag_from_single_source(src, source_mappings) for src in sources]
        flag = sorted(flags)[-1]

        return flag
    
    return _get_flag_from_source