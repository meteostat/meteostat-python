"""
Station Module

Provides functions to fetch individual weather station metadata.
"""

from typing import Optional
from requests import HTTPError, Timeout
from meteostat.core.config import config
from meteostat.core.logger import logger
from meteostat.core.network import network_service
from meteostat.enumerations import TTL
from meteostat.typing import Station
from meteostat.core.cache import cache_service
from meteostat.api.stations import stations


@cache_service.cache(TTL.WEEK)
def _fetch_station(station_id: str) -> Optional[dict]:
    """
    Fetch meta data for a specific weather station from static JSON file
    """
    mirrors = config.stations_meta_mirrors

    if not mirrors:
        logger.error("No station meta data mirrors configured")

    for mirror in mirrors:
        try:
            with network_service.get(mirror.format(id=station_id)) as res:
                if res.status_code == 200:
                    # Parse JSON response
                    station_data = res.json()
                    # Extract English name
                    station_data["name"] = station_data["name"]["en"]
                    # Extract location data
                    station_data["latitude"] = station_data["location"]["latitude"]
                    station_data["longitude"] = station_data["location"]["longitude"]
                    station_data["elevation"] = station_data["location"]["elevation"]
                    # Remove unused data
                    station_data.pop("location", None)
                    station_data.pop("active", None)
                    # Return station dictionary
                    return station_data
        except (HTTPError, Timeout):
            logger.warning(
                "Could not fetch weather station meta data from '%s'", mirror
            )
    return None


def station(id: str) -> Optional[Station]:
    """
    Get meta data for a specific weather station.

    Parameters
    ----------
    id : str
        Unique identifier of the weather station.

    Returns
    -------
    Station
        A Station object containing the meta data for the specified weather station.
    """
    if config.stations_db_prefer:
        return stations.meta(id)

    meta_data = _fetch_station(id)

    return Station(**meta_data) if meta_data else None
