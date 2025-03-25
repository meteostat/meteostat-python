import os
import sqlite3
from typing import List, Optional
import pandas as pd
from requests import get, HTTPError, Timeout
from meteostat.api.point import Point
from meteostat.core.logger import logger
from meteostat.core.network import network_service
from meteostat.enumerations import TTL
from meteostat.typing import Station
from meteostat.core.cache import cache_service
from meteostat.utils.helpers import get_distance

INDEX_MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/locations.csv.gz",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz",
]
STATION_MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/stations/{id}.json",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json",
]
DATABASE_MIRROR = (
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations.db"
)
DEFAULT_DB_FILE = (
    os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "stations.db"
)


@cache_service.cache(60 * 60 * 24 * 7)
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


@cache_service.cache(60 * 60 * 24, "pickle")
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


def _download_db_file(filepath: str, ttl: int) -> Optional[str]:
    """
    Downloads an SQLite file from the given URL
    """
    if os.path.exists(filepath) and not cache_service.is_stale(filepath, ttl):
        logger.debug(f"Using cached file '{filepath}'")
        return filepath

    response = network_service.get(DATABASE_MIRRORS[1], stream=True)

    if response.status_code == 200:
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.debug(f"Downloaded file '{filepath}' successfully")
    else:
        logger.error(f"Failed to download file. Status code: {response.status_code}")
        return None

    return filepath


def connect_stations_db(
    file: str = DEFAULT_DB_FILE,
    ttl: int = TTL.WEEK,
):
    """
    Connect to the stations SQLite database
    """
    file = _download_db_file(file, ttl)

    if not file:
        return None

    try:
        conn = sqlite3.connect(file)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to SQLite database: {e}")
        return None
