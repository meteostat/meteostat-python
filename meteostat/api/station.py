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
def _fetch_station(id: str) -> Optional[dict]:
    """
    Fetch meta data for a specific weather station from static JSON file
    """
    mirrors = config.stations_meta_mirrors

    if not mirrors:
        logger.error("No station meta data mirrors configured")

    for mirror in mirrors:
        try:
            with network_service.get(mirror.format(id=id)) as res:
                if res.status_code == 200:
                    # Parse JSON response
                    station = res.json()
                    # Extract English name
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
