import pandas as pd
from requests import get, HTTPError, Timeout
from meteostat import settings
from meteostat.utils.decorators import cache
from meteostat.types import Station
from meteostat.utils.stations import get_distance


@cache(60 * 60 * 24, "pickle")
def _get_locations() -> pd.DataFrame | None:
    COLUMNS = ["id", "latitude", "longitude"]

    for mirror in settings.stations_locations_mirrors:
        try:
            df = pd.read_csv(mirror, compression="gzip", names=COLUMNS)
            return df.set_index(COLUMNS[0])
        except (HTTPError, Timeout):
            continue
    return None


def meta(id: str) -> Station | None:
    """
    Get meta data for a specific weather station
    """
    # Get all meta data mirrors
    mirrors = settings.stations_meta_mirrors
    # Get meta data for weather station
    for mirror in mirrors:
        try:
            with get(mirror.format(id=id)) as res:
                if res.status_code == 200:
                    return res.json()
        except (HTTPError, Timeout):
            continue
    # If meta data could not be found, return None
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

    ids = df.index.get_level_values("id").to_list()

    return ids[0:limit] if limit else ids
