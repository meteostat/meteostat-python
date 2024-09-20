from requests import get, HTTPError, Timeout
from meteostat.typing import StationDict
from meteostat.utils.decorators import cache


MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/stations/{id}.json",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json",
]


@cache(60 * 60 * 24 * 7)
def station(id: str) -> StationDict | None:
    """
    Get meta data for a specific weather station
    """
    # Get meta data for weather station
    for mirror in MIRRORS:
        try:
            with get(mirror.format(id=id)) as res:
                if res.status_code == 200:
                    return res.json()
        except (HTTPError, Timeout):
            continue
    # If meta data could not be found, return None
    return None
