from typing import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from requests import get, HTTPError, Timeout
from meteostat.framework import config, cache
from meteostat import Station

@cache(60 * 60 * 24 * 7, False)
def meta(id: str) -> Station | None:
    """
    Get meta data for a specific weather station
    """
    # Get all meta data mirrors
    mirrors = config().stations_meta_mirrors
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

def meta_bulk(ids: list[str]) -> Iterable[Future[Station]]:
    """
    Get meta data for multiple weather stations
    """
    with ThreadPoolExecutor(config().get_max_threads(len(ids))) as executor:
        results = []
        for id in ids:
            results.append(executor.submit(meta, id))
        return as_completed(results)