import pandas as pd
from requests import HTTPError, Timeout
from meteostat import settings
from meteostat.utils.decorators import cache

MIRRORS = [
    "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/locations.csv.gz",
    "https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz",
]


@cache(60 * 60 * 24, "pickle")
def index() -> pd.DataFrame | None:
    for mirror in MIRRORS:
        try:
            return pd.read_csv(mirror, compression="gzip", index_col="id").sort_index()
        except (HTTPError, Timeout):
            continue
    return None
