from typing import Any
import os
import json
from meteostat.data.config import DefaultConfig

class _Config(DefaultConfig):
    """
    A class for loading, reading and writing configuration data
    """ 
    def _set(self, key: str, value: Any) -> None:
        if hasattr(self, key):
            if not type(self.__getattribute__(key)) == type(value):
                raise Exception('Types do not match')
            self.__setattr__(key, value)

    def from_env(self) -> None:
        """
        Import configuration from environment variables

        Use the METEOSTAT_ prefix for the variables to be recognized by Meteostat
        The variable's value is parsed as JSON
        """
        for key, value in os.environ.items():
            if not key.startswith('METEOSTAT_'):
                continue
            key = key.replace('METEOSTAT_', '').lower()
            value = json.loads(value)
            self._set(key, value)

    def from_dict(self, data: dict) -> None:
        """
        Import configuration from a dict
        """
        for key, value in data.items():
            self._set(key, value)

    def __init__(self) -> None:
        self.from_env()
    
    def get_max_threads(self, max_required_threads = 1) -> int:
        """
        SHOULD BE MOVED TO LOADER ETC.
        Get maximum number of threads for an async operation
        """
        return min(self.max_threads, max_required_threads)


config = _Config()