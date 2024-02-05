from datetime import datetime
from typing import Iterator, List, Optional, TypeGuard
from meteostat import Provider
from meteostat.typing import ProviderDict
from meteostat.enumerations import Parameter, Granularity
from meteostat.providers.index import PROVIDERS


def get_provider(id: str) -> ProviderDict | None:
    """
    Get a provider by its ID
    """
    return next(
        (provider for provider in PROVIDERS if provider["id"] == id),
        None,
    )


def filter_providers(
    granularity: Granularity,
    parameters: List[Parameter],
    providers: List[Provider],
    country: str,
    start: Optional[datetime],
    end: Optional[datetime],
) -> Iterator[ProviderDict]:
    """
    Get a filtered list of providers
    """

    def _filter(provider: ProviderDict) -> TypeGuard[Provider]:
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
        if (
            "end" in provider
            and provider["end"] is not None
            and start is not None
            and start > provider["end"]
        ):
            return False
        return True

    return filter(_filter, PROVIDERS)
