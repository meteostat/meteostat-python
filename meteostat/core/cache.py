"""
A global cache which provides utilities for caching data on the local file system
"""
from typing import Any
import json
import os
from os.path import exists
from hashlib import md5
from meteostat.settings import settings
from meteostat.core.logger import logger
import pandas as pd
from time import time


def write_pickle(path: str, df: pd.DataFrame) -> None:
    """
    Persist a DataFrame in Pickle format
    """
    df.to_pickle(path)


def read_pickle(path) -> pd.DataFrame:
    """
    Read a pickle file into a DataFrame
    """
    return pd.read_pickle(path)


def write_json(path: str, data: dict | list) -> None:
    """
    Persist data in JSON format
    """
    with open(path, "w") as file:
        json.dump(data, file)


def read_json(path) -> dict | list:
    """
    Read JSON data into memory
    """
    with open(path, "r") as file:
        raw = file.read()
    return json.loads(raw)


def func_to_uid(func, args: tuple, kwargs: dict[str, Any]) -> str:
    """
    Get a unique ID from a function call based on its module, name and arguments
    """
    return md5(
        ";".join(
            (
                func.__module__,
                func.__name__,
                *map(str, args),
                *[f"{key}:{str(value)}" for key, value in kwargs.items()],
            )
        ).encode("utf-8")
    ).hexdigest()


def persist(path: str, data: pd.DataFrame | dict | list, type: str) -> None:
    """
    Persist any given data under a specific path
    """
    if not os.path.exists(settings.cache_dir):
        os.makedirs(settings.cache_dir)
    if type == "json":
        write_json(path, data)
    else:
        write_pickle(path, data)


def fetch(path, type: str) -> pd.DataFrame | dict | list:
    """
    Fetch data from a given path
    """
    if type == "json":
        return read_json(path)
    return read_pickle(path)


def get_cache_path(uid: str, filetype: str):
    """
    Get path of a cached file based on its uid and file type
    """
    return settings.cache_dir + os.sep + f"{uid}.{filetype}"


def is_stale(path: str, ttl: int) -> bool:
    return (
        True
        if time() - os.path.getmtime(path)
        > min([max([ttl, settings.cache_ttl_min]), settings.cache_ttl_max])
        else False
    )


def from_func(func, args, kwargs, ttl: int, format: str) -> pd.DataFrame | dict | list:
    """
    Cache a function's return value
    """
    uid = func_to_uid(func, args, kwargs)  # Get UID for function call
    path = get_cache_path(uid, format)  # Get the local cache path
    result = (
        fetch(path, format)
        if ttl > 0 and exists(path) and not is_stale(path, ttl)
        else False
    )

    logger.info(
        f'{func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs} returns {format} and {"is" if isinstance(result, pd.DataFrame) or result else "is not"} served from cache'
    )

    if isinstance(result, pd.DataFrame) or result:
        return result
    else:
        result = func(*args, **kwargs)
        if ttl > 0:
            persist(path, result, format)

    return result


def purge(ttl: int | None = None) -> None:
    """
    Remove stale files from disk cache
    """
    if ttl is None:
        ttl = settings.cache_ttl_max

    logger.info(f"Removing cached files older than {ttl} seconds")

    cache_dir = settings.cache_dir

    if os.path.exists(cache_dir):
        # Get current time
        now = time()
        # Go through all files
        for file in os.listdir(cache_dir):
            # Get full path
            path = os.path.join(cache_dir, file)
            # Check if file is older than TTL
            if now - os.path.getmtime(path) > ttl and os.path.isfile(path):
                # Delete file
                os.remove(path)
