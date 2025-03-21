from typing import List, Optional
import pandas as pd
from requests import get, HTTPError, Timeout
from meteostat.api.point import Point
from meteostat.core.logger import logger
from meteostat.typing import Station
from meteostat.utils.decorators import cache
from meteostat.utils.helpers import get_distance

INDEX_MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/locations.csv.gz",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz",
]

STATION_MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/stations/{id}.json",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json",
]


@cache(60 * 60 * 24 * 7)
def _fetch_station(id: str) -> Optional[Station]:
    """
    Fetch meta data for a specific weather station
    """

    for mirror in STATION_MIRRORS:
        try:
            with get(mirror.format(id=id)) as res:
                if res.status_code == 200:
                    # Parse JSON response
                    station = res.json()
                    # Extract English station name
                    station["name"] = station["name"]["en"]
                    # Extract location data
                    station["latitude"] = station["location"]["latitude"]
                    station["longitude"] = station["location"]["longitude"]
                    station["elevation"] = station["location"]["elevation"]
                    # Remove unused data
                    station.pop("location", None)
                    station.pop("active", None)
                    # Return station dictionary
                    return station
        except (HTTPError, Timeout):
            logger.warning(f"Could not fetch weather station meta data from '{mirror}'")


def station(id: str) -> Optional[Station]:
    """
    Get meta data for a specific weather station
    """
    meta_data = _fetch_station(id)

    return Station(**meta_data) if meta_data else None


@cache(60 * 60 * 24, "pickle")
def stations() -> Optional[pd.DataFrame]:
    """
    Get a DataFrame of all weather stations
    """
    for mirror in INDEX_MIRRORS:
        try:
            return pd.read_csv(mirror, compression="gzip", index_col="id").sort_index()
        except (HTTPError, Timeout):
            logger.warning(f"Could not fetch weather stations from '{mirror}'")


def nearby(
    point: Point, radius: float = None, limit: int = None
) -> Optional[List[str]]:
    """
    Get a list of weather station IDs ordered by distance
    """
    df = stations()

    if df is None:
        return None

    # Get distance for each station
    df["distance"] = get_distance(
        point.latitude, point.longitude, df["latitude"], df["longitude"]
    )

    # Filter by radius
    if radius:
        df = df[df["distance"] <= radius]

    # Sort stations by distance
    df.columns.str.strip()
    df = df.sort_values("distance")

    return df[0:limit] if limit else df
