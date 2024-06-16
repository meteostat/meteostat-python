import os
import json
from typing import Any


class Settings:
    """
    A class for loading, reading, and writing configuration data
    """

    root_dir = (
        os.path.expanduser("~") + os.sep + ".meteostat"
    )  # Meteostat root directory
    cache_enable = True  # Enable caching of provider data?
    cache_dir = root_dir + os.sep + "cache"  # Cache directory
    cache_ttl_max = 60 * 60 * 24 * 30  # Maximum cache TTL (default: 30 days)
    cache_ttl_min = 0  # Minimum cache TTL
    cache_autoclean = True  # Automatically remove stale files from cache?
    request_timeout = 5  # Timeout for HTTP requests
    stations_db_ttl = 60 * 60 * 24 * 7  # TTL for the stations.db file (default: 7 days)
    inventory_db_ttl = (
        60 * 60 * 24 * 7
    )  # TTL for the stations.db file (default: 7 days)
    station_mirrors = [
        "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/stations/{id}.json",
        "https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json",
    ]
    location_mirrors = [
        "https://cdn.jsdelivr.net/gh/meteostat/weather-stations/locations.csv.gz",
        "https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz",
    ]
    bulk_load_sources = False

    @classmethod
    def set_value(cls, key: str, value: Any) -> None:
        """
        Set a configuration value
        """
        if hasattr(cls, key):
            value_type = type(getattr(cls, key))
            setattr(cls, key, value_type(value))
        else:
            raise AttributeError(f"'Settings' object has no attribute '{key}'")

    @classmethod
    def load_env(cls, prefix="MS") -> None:
        """
        Import configuration from environment variables
        """
        prefix = f"{prefix}_" if prefix else None
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            key = key.replace(prefix, "").lower()
            value = json.loads(value)
            cls.set_value(key, value)


settings = Settings()
