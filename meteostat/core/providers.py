from datetime import datetime
from meteostat import Provider, types
from meteostat.enumerations import Parameter, Granularity
from meteostat.providers.index import PROVIDERS


def get_provider(id: str) -> Provider | None:
    """
    Get a provider by its ID
    """
    return next(
        (
            provider
            for provider in PROVIDERS
            if provider["id"] == id or provider["id"].value == id
        ),
        None,
    )


def filter_providers(
    granularity: Granularity,
    parameters: list[Parameter],
    providers: list[Provider],
    country: str,
    start: datetime,
    end: datetime | None = None,
) -> list[types.Provider]:
    """
    Get a filtered list of providers
    """

    def filter_providers(provider: types.Provider) -> bool:
        if provider["granularity"] is not granularity:
            return False
        if set(provider["parameters"]).isdisjoint(parameters):
            return False
        if provider["id"] not in providers:
            return False
        if "countries" in provider and country not in provider["countries"]:
            return False
        if end and end < provider["start"]:
            return False
        if "end" in provider and start > provider["end"]:
            return False
        return True

    return filter(filter_providers, PROVIDERS)
