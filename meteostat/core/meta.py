from datetime import datetime
from typing import Iterator, List, Optional, TypeGuard
from meteostat import Provider
from meteostat.core.parameters import PARAMETERS
from meteostat.core.providers import PROVIDERS
from meteostat.typing import ParameterDict, ProviderDict
from meteostat.enumerations import Parameter, Granularity


def get_parameters(granularity: Granularity, default=False) -> List[Parameter]:
    """
    Get available parameters by granularity
    """
    return list(
        map(
            lambda p: p["id"],
            filter(
                lambda p: granularity
                in [
                    g["granularity"]
                    for g in p["granularities"]
                    if default == False or "default" in g and g["default"] == True
                ],
                PARAMETERS,
            ),
        )
    )


def get_parameter(id: Parameter) -> Optional[ParameterDict]:
    """
    Get a parameter by its ID
    """
    return next(
        (parameter for parameter in PARAMETERS if parameter["id"] == id),
        None,
    )


def get_providers(granularity: Granularity) -> List[Provider]:
    """
    Get available providers by granularity
    """
    return list(
        map(
            lambda p: p["id"],
            filter(lambda p: p["granularity"] == granularity, PROVIDERS),
        )
    )


def get_provider(id: str) -> Optional[ProviderDict]:
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
