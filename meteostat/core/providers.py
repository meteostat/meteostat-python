from datetime import datetime
from typing import Iterator, Optional, Set, Tuple, TypeGuard
from meteostat import Provider, typing
from meteostat.enumerations import Parameter, Granularity
from meteostat.providers.index import PROVIDERS


def get_provider(id: str) -> typing.Provider | None:
    """
    Get a provider by its ID
    """
    return next(
        (provider for provider in PROVIDERS if provider["id"] == id),
        None,
    )


def filter_providers(
    granularity: Granularity,
    parameters: Tuple[Parameter, ...],
    providers: Tuple[Provider, ...],
    country: str,
    start: Optional[datetime],
    end: Optional[datetime],
) -> Iterator[typing.Provider]:
    """
    Get a filtered list of providers
    """

    def _filter(provider: typing.Provider) -> TypeGuard[Provider]:
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
