"""
Cache Service

The Cache Service provides utilities for caching data on the local file system.
"""

from functools import wraps
from typing import Any, Callable, Optional
import json
import os
from os.path import exists
from hashlib import md5
from meteostat.core.config import config
from meteostat.core.logger import logger
import pandas as pd
from time import time


class CacheService:
    """
    Cache Service
    """

    _purged = False  # Flag to indicate if cache has been purged automatically

    @staticmethod
    def _write_pickle(path: str, df: Optional[pd.DataFrame]) -> None:
        """
        Persist a DataFrame in Pickle format
        """
        pd.DataFrame().to_pickle(path) if df is None else df.to_pickle(path)

    @staticmethod
    def _read_pickle(path) -> Optional[pd.DataFrame]:
        """
        Read a pickle file into a DataFrame
        """
        df: pd.DataFrame = pd.read_pickle(path)
        return None if df.empty else df

    @staticmethod
    def _write_json(path: str, data: dict | list) -> None:
        """
        Persist data in JSON format
        """
        with open(path, "w") as file:
            json.dump(data, file)

    @staticmethod
    def _read_json(path) -> dict | list:
        """
        Read JSON data into memory
        """
        with open(path, "r") as file:
            raw = file.read()
        return json.loads(raw)

    @staticmethod
    def create_cache_dir() -> None:
        """
        Create the cache directory if it doesn't exist
        """
        cache_dir = config.get("cache.directory")

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    @staticmethod
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

    def persist(self, path: str, data: pd.DataFrame | dict | list, type: str) -> None:
        """
        Persist any given data under a specific path
        """
        # Create cache directory if it doesn't exist
        self.create_cache_dir()
        # Save data locally
        if type == "json":
            self._write_json(path, data)
        else:
            self._write_pickle(path, data)

    def fetch(self, path, type: str) -> pd.DataFrame | dict | list:
        """
        Fetch data from a given path
        """
        if type == "json":
            return self._read_json(path)
        return self._read_pickle(path)

    @staticmethod
    def get_cache_path(uid: str, filetype: str):
        """
        Get path of a cached file based on its uid and file type
        """
        return config.get("cache.directory") + os.sep + f"{uid}.{filetype}"

    @staticmethod
    def is_stale(path: str, ttl: int) -> bool:
        return (
            True
            if time() - os.path.getmtime(path) > max([ttl, config.get("cache.ttl")])
            else False
        )

    def from_func(
        self, func, args, kwargs, ttl: int, format: str
    ) -> pd.DataFrame | dict | list:
        """
        Cache a function's return value
        """
        uid = self.func_to_uid(func, args, kwargs)  # Get UID for function call
        path = self.get_cache_path(uid, format)  # Get the local cache path
        result = (
            self.fetch(path, format)
            if ttl > 0 and exists(path) and not self.is_stale(path, ttl)
            else False
        )

        logger.debug(
            f'{func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs} returns {format} and {"is" if isinstance(result, pd.DataFrame) or result else "is not"} served from cache'
        )

        if isinstance(result, pd.DataFrame) or result:
            return result
        else:
            result = func(*args, **kwargs)
            if ttl > 0:
                self.persist(path, result, format)

        return result

    @staticmethod
    def purge(ttl: Optional[int] = None) -> None:
        """
        Remove stale files from disk cache
        """
        if ttl is None:
            ttl = config.get("cache.ttl")

        logger.debug(f"Removing cached files older than {ttl} seconds")

        cache_dir = config.get("cache.directory")

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

    def cache(
        self, ttl: int | Callable[[Any], int] = 60 * 60 * 24, format: str = "json"
    ):
        """
        A simple decorator which caches a function's return value
        based on its payload.

        All data is persisted in either JSON or Pickle format.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not config.get("cache.enable"):
                    logger.debug(
                        f"Ommitting cache for {func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs}"
                    )
                    return func(*args, **kwargs)
                if config.get("cache.autoclean") and not self._purged:
                    self.purge()
                    self._purged = True
                return self.from_func(
                    func,
                    args,
                    kwargs,
                    ttl if isinstance(ttl, int) else ttl(*args, **kwargs),
                    format,
                )

            return wrapper

        return decorator


cache_service = CacheService()
