"""
Providers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
from meteostat.framework import Provider
from meteostat.data.providers import DEFAULT_PROVIDERS
    
class _Providers:
    _list: list[Provider] = DEFAULT_PROVIDERS

    def get(self, id: str | None = None) -> Provider | list[Provider] | None:
        """
        Returns a single provider when passing a key or a list of all providers otherwise
        """
        return next(
            (provider for provider in self._list if provider['id'] == id),
            None
        ) if id else self._list
    
    def add(self, id: str, name: str, countries: list[str], parameters: list[str], license: str, handler: str) -> None:
        if id in map(lambda provider: provider['id'], self._list):
            raise Exception(f'Provider {id} already exists')

        self._list.append(Provider(
            name,
            countries,
            parameters,
            license,
            handler
        ))


providers = _Providers()