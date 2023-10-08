"""
A global cache system which provides utilities for caching data both
on the local file system.
"""

from typing import Any, Callable
import json
import os
from os.path import exists
import functools
from hashlib import md5
from meteostat import settings
from meteostat.core import logger
import pandas as pd
from time import time

def cache(ttl: int | Callable[[Any], int] = 60 * 60 * 24, format: str = 'json'):
    """
    A simple decorator which caches a function's return value
    based on its payload and type annotation

    All data is persisted in JSON format, except functions
    annotated with a Pandas DataFrame return type.
    This data is stored as pickle.
    """    
    def _decorator(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            if settings.cache_autoclean:
                purge_cache()
            if not settings.cache_enable:
                logger.info(f'Ommitting cache for {func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs}')
                return func(*args, **kwargs)
            return _from_func(func, args, kwargs, ttl if isinstance(ttl, int) else ttl(args, kwargs), format)

        return _wrapper

    return _decorator

def purge_cache(max_age: int | None = None) -> None:
    """
    Remove stale files from disk cache
    """
    if max_age is None:
        max_age = settings.cache_max_age

    cache_dir = settings.cache_dir

    if os.path.exists(cache_dir):
        # Get current time
        now = time()
        # Go through all files
        for file in os.listdir(cache_dir):
            # Get full path
            path = os.path.join(cache_dir, file)
            # Check if file is older than max_age
            if now - os.path.getmtime(path) > max_age and os.path.isfile(path):
                # Delete file
                os.remove(path)

def _func_to_uid(func, args: tuple, kwargs: dict[str, Any]) -> str:
    """
    Get a unique ID from a function call based on its module, name and arguments
    """
    return md5(';'.join((func.__module__, func.__name__, *map(str, args), *[f'{key}:{str(value)}' for key, value in kwargs.items()])).encode("utf-8")).hexdigest()

def _write_pickle(path: str, df: pd.DataFrame) -> None:
    """
    Persist a DataFrame in pickle format
    """
    df.to_pickle(path)

def _read_pickle(path) -> pd.DataFrame:
    """
    Read a pickle file into a DataFrame
    """
    return pd.read_pickle(path)

def _write_json(path: str, data: dict | list) -> None:
    """
    Persist data in JSON format
    """
    with open(path, 'w') as file:
        json.dump(data, file)

def _read_json(path) -> dict | list:
    """
    Read JSON data into memory
    """
    with open(path, 'r') as file:
        raw = file.read()
    return json.loads(raw)

def _persist(path: str, data: pd.DataFrame | dict | list, type: str):
    """
    Persist any given data under a specific path
    """
    if type == 'json':
        _write_json(path, data)
    else:
        _write_pickle(path, data)

def _fetch(path, type: str) -> pd.DataFrame | dict | list:
    """
    Fetch data from a given path
    """
    if type == 'json':
        return _read_json(path)
    return _read_pickle(path)

def _get_cache_path(uid: str, filetype: str):
    """
    Get path of a cached file based on its uid and file type
    """
    return settings.cache_dir + os.sep + f"{uid}.{filetype}"
    
def _is_expired(path: str, ttl: int) -> bool:
    return True if time() - os.path.getmtime(path) > ttl else False

def _from_func(func, args, kwargs, ttl: int, format: str) -> pd.DataFrame | dict | list:
    """
    Cache a function's return value
    """
    uid = _func_to_uid(func, args, kwargs) # Get UID for function call
    path = _get_cache_path(uid, format) # Get the local cache path
    result = _fetch(path, format) if ttl > 0 and exists(path) and not _is_expired(path, ttl) else False

    logger.info(f'{func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs} returns {format} and {"is" if isinstance(result, pd.DataFrame) or result else "is not"} served from cache')

    if isinstance(result, pd.DataFrame) or result:
        return result
    else:
        result = func(*args, **kwargs)
        if ttl > 0:
            _persist(path, result, format)

    return result