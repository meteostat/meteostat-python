import pandas as pd
from requests import HTTPError, Timeout
from meteostat import settings
from meteostat.utils.decorators import cache


@cache(60 * 60 * 24, "pickle")
def index() -> pd.DataFrame | None:
    for mirror in settings.location_mirrors:
        try:
            return pd.read_csv(mirror, compression="gzip", index_col="id").sort_index()
        except (HTTPError, Timeout):
            continue
    return None
