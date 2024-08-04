from requests import get, HTTPError, Timeout
from meteostat import settings
from meteostat.typing import StationDict
from meteostat.utils.decorators import cache


@cache(60 * 60 * 24 * 7)
def station(id: str) -> StationDict | None:
    """
    Get meta data for a specific weather station
    """
    # Get all meta data mirrors
    mirrors = settings["station_mirrors"]
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
