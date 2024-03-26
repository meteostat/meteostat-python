from io import BytesIO
import os
import sqlite3
import pandas as pd
from requests import Response, get
from meteostat.settings import settings
from meteostat.core.cache import create_cache_dir, is_stale


def _get_local_db_path(file: str) -> str:
    """
    Get path of local DB file
    """
    return settings.root_dir + os.sep + file

def _get_remote_db_url(file: str) -> str:
    """
    Get URL of remote DB file
    """
    return f'{settings.ms_data_host}/{file}'

def _get_db_file(file: str) -> Response:
    """
    Get a DB file
    """
    url = _get_remote_db_url(file)
    try:
        res = get(url)
        if res.status_code == 200:
            return res
        else:
            raise Exception(f"status code {res.status_code}")
    except Exception as error:
        raise Exception(f"{url} returns error: {error}")

def _download_db_file(file: str) -> None:
    """
    Download a DB file
    """
    # Get stations.db file
    res = _get_db_file(file)
    # Create cache directory if it doesn't exist
    create_cache_dir()
    # Get local DB path
    path = _get_local_db_path(file)
    # Save file locally
    with open(path, "wb+") as file:
        file.write(res.content)


def _get_memory_connection(file: str) -> sqlite3.Connection:
    """
    Get in-memory connection to stations.db
    """
    res = _get_db_file(file)
    content = BytesIO(res.content)
    conn = sqlite3.connect(":memory:")
    conn.deserialize(content.read())
    return conn


def _connect(file: str, ttl: int) -> sqlite3.Connection:
    """
    Connect to an SQLite database
    """
    if not ttl:
        return _get_memory_connection(file)
    path = _get_local_db_path(file)
    if not os.path.isfile(path) or is_stale(path, ttl):
        _download_db_file(file)
    return sqlite3.connect(path)


def connect_stations_db() -> sqlite3.Connection:
    """
    Connect to weather stations database
    """
    return _connect('stations.db', settings.stations_db_ttl)


def connect_inventory_db() -> sqlite3.Connection:
    """
    Connect to inventory database
    """
    return _connect('inventory.db', settings.inventory_db_ttl)


def query_stations(sql: str, *args, **kwargs) -> pd.DataFrame:
    """
    Run a query against the weather stations database
    """
    return pd.read_sql(sql, connect_stations_db(), *args, **kwargs)

def query_inventory(sql: str, *args, **kwargs) -> pd.DataFrame:
    """
    Run a query against the inventory database
    """
    return pd.read_sql(sql, connect_inventory_db(), *args, **kwargs)