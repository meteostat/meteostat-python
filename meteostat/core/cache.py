"""
Global Cache System
"""

from typing import Any
import json
import os
from os.path import exists
import functools
from hashlib import md5
from meteostat.framework import logger, config
import polars as pl
from time import time


class _Cache:
    """
    A global cache system which provides utilities for caching data both
    on the local file system and in-memory.

    This class is not meant to be consumed directly.
    Please use the cache decorator instead.
    """
    enabled = True
    cache_dir: str | None = None # The local cache directory
    memory = {} # Cached data which is kept in-memory
    autocleaned = False

    @classmethod
    def get_uid(cls, func, args: tuple, kwargs: dict[str, Any]) -> str:
        """
        Get a unique ID from a function call based on its module, name and arguments
        """
        return md5(';'.join((func.__module__, func.__name__, *map(str, args), *[f'{key}:{str(value)}' for key, value in kwargs.items()])).encode("utf-8")).hexdigest()

    @classmethod
    def write_parquet(cls, path: str, df: pl.DataFrame) -> None:
        """
        Persist a DataFrame in Parquet format
        """
        df.write_parquet(path)

    @classmethod
    def read_parquet(cls, path) -> pl.DataFrame:
        """
        Read a Parquet file into a DataFrame
        """
        return pl.read_parquet(path)

    @classmethod
    def write_json(cls, path: str, data: dict | list) -> None:
        """
        Persist data in JSON format
        """
        with open(path, 'w') as file:
            json.dump(data, file)

    @classmethod
    def read_json(cls, path) -> dict | list:
        """
        Read JSON data into memory
        """
        with open(path, 'r') as file:
            raw = file.read()
        return json.loads(raw)

    @classmethod
    def persist(cls, path: str, data: pl.DataFrame | dict | list, type: str):
        """
        Persist any given data under a specific path
        """
        if type == 'json':
            cls.write_json(path, data)
        else:
            cls.write_parquet(path, data)

    @classmethod
    def fetch(cls, path, type: str) -> pl.DataFrame | dict | list:
        """
        Fetch data from a given path
        """
        if type == 'json':
            return cls.read_json(path)
        return cls.read_parquet(path)
    
    def __init__(self, cache_dir: str) -> None:
        self.enabled = config().cache_enable
        if self.enabled:
            os.makedirs(cache_dir, exist_ok=True)
        self.cache_dir = cache_dir

    def get_cache_path(self, uid: str, filetype: str):
        """
        Get path of a cached file based on its uid and file type
        """
        return self.cache_dir + os.sep + f"{uid}.{filetype}"
    
    def is_expired(self, path: str, ttl: int) -> bool:
        return True if time() - os.path.getmtime(path) > ttl else False
    
    def cache_function(self, func, args, kwargs, ttl: int, in_memory: bool) -> pl.DataFrame | dict | list:
        """
        Cache a function's return value
        """
        uid = self.get_uid(func, args, kwargs) # Get UID for function call
        return_type = func.__annotations__["return"] # Extract return type from the function's annotations
        type = 'parquet' if return_type == pl.DataFrame else 'json' # File type can be either JSON or Parquet
        path = self.get_cache_path(uid, type) # Get the local cache path
        result = self.memory[path] if in_memory and path in self.memory else self.fetch(path, type) if ttl > 0 and exists(path) and not self.is_expired(path, ttl) else False

        logger().info(f'{func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs} returns {type} and {"is" if result else "is not"} served from cache')

        if result:
            if in_memory:
                self.memory[path] = result
            return result
        else:
            result = func(*args, **kwargs)
            if ttl > 0:
                self.persist(path, result, type)
            if in_memory:
                self.memory[path] = result

        return result

# Use a single instance of GlobalCache
# This class instance is not meant to be consumed directly.
# Please use the cache decorator instead.
@functools.cache
def _cache() -> _Cache:
    return _Cache(config().cache_dir)

def cache(ttl: int = 60 * 60 * 24, in_memory = False):
    """
    A simple decorator which caches a function's return value
    based on its payload and type annotation
    """    
    def _decorator(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            if not _cache().autocleaned and config().cache_autoclean:
                _cache().autocleaned = True
                purge()
            if not _cache().enabled:
                logger().info(f'Ommitting cache for {func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs}')
                return func(*args, **kwargs)
            return _cache().cache_function(func, args, kwargs, ttl, in_memory)

        return _wrapper

    return _decorator

def purge(max_age: int | None = None) -> None:
    """
    Remove stale files from disk cache
    """
    if max_age is None:
        max_age = config().cache_max_age

    cache_dir = config().cache_dir

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