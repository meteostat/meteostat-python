import os
import json

class _Config(Settings):
    """
    A class for loading, reading and writing configuration data.

    This class is not meant to be consumed directly.
    Please use the class instance "config" instead.
    """
    def __init__(self) -> None:
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
            if not type(self.__getattribute__(key)) == type(value):
                raise Exception('Types do not match')
            self.__setattr__(key, value)
    
    def get_max_threads(self, max_required_threads = 1) -> int:
        """
        SHOULD BE MOVED TO LOADER ETC.
        Get maximum number of threads for an async operation
        """
        return min(self.max_threads, max_required_threads)


config = _Config()