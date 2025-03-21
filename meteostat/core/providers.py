from datetime import datetime
from importlib import import_module
from typing import List, Optional, TypeGuard

import pandas as pd

from meteostat.enumerations import Granularity, Priority, Provider, Grade
from meteostat.providers.index import DEFAULT_PROVIDERS
from meteostat.typing import (
    Query,
    ProviderSpec,
    Station,
    Request,
)


class ProviderService:
    """
    Provider Service
    """

    _providers: List[ProviderSpec]

    def __init__(self, providers: List[ProviderSpec]) -> None:
        self._providers = providers

    @property
    def providers(self) -> List[ProviderSpec]:
        """
        Get supported providers
        """
        return self._providers

    def register(self, provider: ProviderSpec) -> None:
        """
        Register a provider
        """
        self._providers.append(provider)

    def get_provider(self, provider_id: Provider) -> Optional[ProviderSpec]:
        """
        Get provider by ID
        """
        return next(
            (provider for provider in self._providers if provider.id == provider_id),
            None,
        )

    def get_provider_priority(self, provider_id: Provider) -> int:
        """
        Get priority of a provider by its ID
        """
        BASELINES = {
            Granularity.HOURLY: 0,
            Granularity.DAILY: 100,
            Granularity.MONTHLY: 200,
            Granularity.NORMALS: 300,
        }

        provider = self.get_provider(provider_id)

        if not provider:
            return Priority.NONE

        baseline = BASELINES[provider.granularity]

        return int(provider.priority + baseline)

    def get_source_priority(self, source: str) -> int:
        """
        Get priority of a source string
        """
        provider_ids = source.split(" ")

        if len(provider_ids) == 1:
            return self.get_provider_priority(provider_ids[0])

        priorities = [self.get_provider_priority(provider) for provider in provider_ids]

        return min(priorities)

    def filter_providers(self, query: Request, station: Station) -> List[Provider]:
        """
        Get a filtered list of providers
        """

        def _filter(provider_id: Provider) -> TypeGuard[Provider]:
            provider = self.get_provider(provider_id)

            # Filter out providers with diverging granularities
            if provider.granularity is not query.granularity:
                return False

            # Filter out providers with no overlap in parameters
            if set(provider.parameters).isdisjoint(query.schema.names):
                return False

            # Filter out providers with non-commercial license
            # if data is intended to be used commercially
            if (
                query.commercial is True
                and provider.license
                and provider.license.commercial is False
            ):
                return False

            # Filter out providers with modeled data if non-model data has been requested
            if query.model is False and provider.grade in (
                Grade.FORECAST,
                Grade.ANALYSIS,
            ):
                return False

            # Filter out providers which do not serve the station's country
            if provider.countries and station.country not in provider.countries:
                return False

            # Filter out providers which stopped providing data before the request's start date
            if query.end and query.end < datetime.combine(
                provider.start, datetime.min.time()
            ):
                return False

            # Filter out providers which only started providing data after the request's end date
            if (
                provider.end is not None
                and query.start is not None
                and query.start > datetime.combine(provider.end, datetime.max.time())
            ):
                return False

            return True

        return filter(_filter, query.providers)

    def fetch_data(
        self, provider_id: Provider, req: Request, station: Station
    ) -> Optional[pd.DataFrame]:
        """
        Fetch data from a given provider
        """
        provider = self.get_provider(provider_id)
        query = Query(
            station=station,
            start=req.start if req.start else provider.start,
            end=req.end if req.end else (provider.end or datetime.now()),
            parameters=req.schema.names,
        )

        if not provider:
            return None

        module = import_module(provider.module)
        df = module.fetch(query)
        return df

    @staticmethod
    def parse_providers(
        requested: List[Provider], supported: List[Provider]
    ) -> List[Provider]:
        """
        Raise exception if a requested provider is not supported
        """
        # Convert providers to set
        providers = list(
            map(lambda p: p if isinstance(p, Provider) else Provider[p], requested)
        )
        # Get difference between providers and supported providers
        diff = set(providers).difference(supported)
        # Log warning
        if len(diff):
            raise ValueError(
                f"""Tried to request data for unsupported provider(s): {
                ", ".join([p for p in diff])
            }"""
            )
        # Return intersection
        return list(filter(lambda provider_id: provider_id in requested, supported))


provider_service = ProviderService(providers=DEFAULT_PROVIDERS)
