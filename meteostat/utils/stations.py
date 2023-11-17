from functools import wraps

import numpy as np
import meteostat as ms
from meteostat.types import Station


def get_meta_data(stations: list[str] | str) -> list[Station]:
    return list(map(ms.stations.meta, [stations] if isinstance(stations, str) else stations))


def use_meta():
    """
    A simple decorator which converts a station ID into a full-blown
    Station object.
    """    
    def decorator(func):

        wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > 0 and isinstance(args[0], str):
                station = ms.stations.meta(args[0])
                args[0] = station
                return func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator

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