import os
import sqlite3
import pandas as pd
from requests import get
from meteostat.settings import settings
from meteostat.core.cache import is_stale
from meteostat.core.logger import logger


def _download_db(path: str) -> None:
    """
    Download DB file from mirror
    """
    for mirror in settings.station_db_mirrors:
        try:
            res = get(mirror)
            if res.status_code == 200:
                with open(path, "wb") as file:
                    file.write(res.content)
            else:
                raise Exception(f"status code {res.status_code}")
        except Exception as error:
            logger.error(f"{mirror} returns error: {error}")


def connect() -> sqlite3.Connection:
    """
    Returns an SQLite connection to the database of weather stations
    """
    path = settings.root_dir + os.sep + "stations.db"
    if not os.path.isfile(path) or is_stale(path, settings.station_db_ttl):
        _download_db(path)
    return sqlite3.connect(path)


def query(sql: str, *args, **kwargs) -> pd.DataFrame:
    """
    Run a query against the database of weather stations
    """
    return pd.read_sql(sql, connect(), *args, **kwargs)
