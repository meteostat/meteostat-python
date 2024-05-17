import numpy as np
import pandas as pd
from requests import HTTPError, Timeout
from meteostat import settings
from meteostat.utils.decorators import cache


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

    return round(radius * arch_sin)


@cache(60 * 60 * 24, "pickle")
def _get_locations() -> pd.DataFrame | None:
    for mirror in settings.location_mirrors:
        try:
            return pd.read_csv(mirror, compression="gzip", index_col="id")
        except (HTTPError, Timeout):
            continue
    return None


def nearby(
    latitude: float, longitude: float, radius: float = None, limit: int = None
) -> list[str] | None:
    """
    Get a list of weather station IDs ordered by distance
    """
    df = _get_locations()

    if df is None:
        return None

    # Get distance for each station
    df["distance"] = get_distance(latitude, longitude, df["latitude"], df["longitude"])

    # Filter by radius
    if radius:
        df = df[df["distance"] <= radius]

    # Sort stations by distance
    df.columns.str.strip()
    df = df.sort_values("distance")

    return df[0:limit] if limit else df
