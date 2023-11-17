from importlib import import_module
import pandas as pd
from meteostat import Provider
from meteostat.providers.index import PROVIDERS


class ProvidersService:
    @staticmethod
    def get_provider(id: str) -> Provider | list[Provider] | None:
        return next(
            (provider for provider in PROVIDERS if provider['id'] == id),
            None
        )
    
    @classmethod
    def call_provider(cls, provider: Provider, *args) -> pd.DataFrame:
        details = cls.get_provider(provider)
        module = import_module(details['module'])
        df = module.fetch(*args)
        return df
    
providers = ProvidersService()