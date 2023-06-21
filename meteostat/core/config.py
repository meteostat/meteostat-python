import os
from functools import cache
from yaml import safe_load
from meteostat.utilities.flatten import flatten_dict

class _DefaultConfig:
    debug = False
    meteostat_dir = os.path.expanduser("~") + os.sep + ".meteostat"
    cache_dir = meteostat_dir + os.sep + "cache"
    log_file = meteostat_dir + os.sep + 'debug.log'
    max_threads = 8
    cache_enable = True
    cache_max_age = 60*60*24*30 # 30 days
    cache_autoclean = True
    stations_meta_mirrors = [
        'https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json'
    ]

class Config(_DefaultConfig):
    """
    A class for loading, reading and writing configuration data
    """
    def load_local_config(self) -> dict:
        """
        Read local config file and merge with default configuration
        """
        with open(self.meteostat_dir + os.sep + 'config.yml', 'r') as file:
            data = safe_load(file.read())
            if data:
                return flatten_dict(data)
            
    def set(self, key: str, value: str) -> None:
        if hasattr(self, key) and self.__getattribute__(key) == _DefaultConfig().__getattribute__(key):
            self.__setattr__(key, value)

    def __init__(self) -> None:
        for key, value in os.environ.items():
            if key.startswith('METEOSTAT_'):
                key = key.replace('METEOSTAT_', '').lower()
                self.set(key, value)
        os.makedirs(self.meteostat_dir, exist_ok=True)
        local_config = self.load_local_config()
        if local_config:
            for key, value in local_config.items():
                self.set(key, value)
    
    def get_max_threads(self, max_required_threads = 1) -> int:
        """
        Get maximum number of threads for an async operation
        """
        return min(self.max_threads, max_required_threads)


@cache
def config() -> Config:
    return Config()