from typing import Any
import os
import json

class DefaultSettings:
    debug = False
    meteostat_dir = os.path.expanduser("~") + os.sep + ".meteostat"
    cache_dir = meteostat_dir + os.sep + 'cache'
    cache_enable = True
    cache_max_age = 60*60*24*30 # 30 days
    cache_purge = True
    stations_meta_mirrors = [
        'https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json'
    ]
    stations_locations_mirrors = [
        'https://raw.githubusercontent.com/meteostat/weather-stations/master/locations.csv.gz'
    ]

class SettingsService(DefaultSettings):
    """
    A class for loading, reading and writing configuration data
    """ 
    def _set(self, key: str, value: Any) -> None:
        if hasattr(self, key):
            if not type(self.__getattribute__(key)) == type(value):
                raise Exception('Types do not match')
            self.__setattr__(key, value)

    def load_env(self, prefix = 'MS') -> None:
        """
        Import configuration from environment variables

        Use the MS_ prefix for the variables to be recognized by Meteostat

        The variable's value is parsed as JSON
        """
        prefix = f'{prefix}_' if prefix else None
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            key = key.replace(prefix, '').lower()
            value = json.loads(value)
            self._set(key, value)

    def __init__(self) -> None:
        self.load_env()


settings = SettingsService()