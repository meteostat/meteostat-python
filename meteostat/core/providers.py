"""
Providers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
from meteostat.types import Provider
from meteostat.config.providers import DEFAULT_PROVIDERS
    
class _Providers:
    _list: list[Provider] = []

    def __init__(self, default_providers: list[Provider] = []) -> None:
        [self.register(provider) for provider in default_providers]

    def get(self, id: str) -> Provider | list[Provider] | None:
        return next(
            (provider for provider in self._list if provider['id'] == id),
            None
        )
    
    def register(self, provider: Provider) -> None:
        if provider['id'] in map(lambda p: p['id'], self._list):
            raise Exception(f'Provider {provider["id"]} already exists')

        self._list.append(provider)


providers = _Providers(DEFAULT_PROVIDERS)