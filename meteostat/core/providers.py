"""
Providers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
import os
import importlib.resources
from functools import cache
from yaml import safe_load
from meteostat.framework import config
from meteostat.utilities.pool import pool
    
class _Providers:
    _dict = {}

    @staticmethod
    def _get_default_providers() -> dict:
        with importlib.resources.open_text("meteostat.data", "providers.yml") as file:
            return safe_load(file)

    @staticmethod    
    def _get_local_providers():
        with open(config().meteostat_dir + os.sep + 'providers.yml', 'r') as file:
            return safe_load(file.read())
        
    def __init__(self) -> None:
        default_providers = _Providers._get_default_providers()
        local_providers = _Providers._get_local_providers()
        self._dict = default_providers | _Providers._get_local_providers() if local_providers else default_providers

    def get(self, key: str | None = None) -> dict | dict[dict]:
        """
        Returns a single provider when passing a key or a dict of all providers otherwise
        """
        return self._dict[key] if key else self._dict
    
    def add(self, id: str, name: str, countries: list[str], parameters: list[str], license: str, handler: str) -> None:
        if id in self._dict:
            raise Exception(f'Provider {id} already exists')

        self._dict[id] = {
            'name': name,
            'countries': countries,
            'parameters': parameters,
            'license': license,
            'handler': handler
        }


@cache
def providers() -> _Providers:
    """
    Get providers
    """
    return _Providers()