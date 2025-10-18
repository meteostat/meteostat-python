"""
Data Service

The Data Service is responsible for fetching meteorological data from
different providers and merging it into a single time series.
"""

from typing import List, Optional
import pandas as pd
from meteostat.api.timeseries import TimeSeries
from meteostat.core.logger import logger
from meteostat.core.parameters import parameter_service
from meteostat.core.providers import provider_service
from meteostat.core.schema import schema_service
from meteostat.enumerations import Grade, Granularity, Parameter, Provider
from meteostat.typing import Station, Request
from meteostat.utils.filters import filter_time


class DataService:
    """
    Data Service
    """

    @staticmethod
    def _add_source(df: pd.DataFrame, provider_id: str) -> pd.DataFrame:
        """
        Add source column to DataFrame
        """
        if not "source" in df.index.names:
            df["source"] = provider_id
            df = df.set_index(["source"], append=True)

        return df

    @staticmethod
    def concat_fragments(
        fragments: List[pd.DataFrame],
        parameters: List[Parameter],
    ) -> pd.DataFrame:
        """
        Concatenate multiple fragments into a single DataFrame
        """
        try:
            df = pd.concat(
                [
                    df.dropna(how="all", axis=1) if not df.empty else None
                    for df in fragments
                ]
            )
            df = schema_service.fill(df, parameters)
            df = schema_service.purge(df, parameters)
            return df
        except ValueError:
            return pd.DataFrame()

    def _fetch_provider_data(
        self, req: Request, station: Station, provider: Provider
    ) -> Optional[pd.DataFrame]:
        """
        Fetch data for a single weather station and provider
        """
        try:
            # Fetch DataFrame for current provider
            df = provider_service.fetch_data(provider, req, station)

            # Continue if no data was returned
            if df is None:
                return None

            # Add current station ID to DataFrame
            df = pd.concat([df], keys=[station.id], names=["station"])

            # Add source index column to DataFrame
            df = self._add_source(df, provider)

            # Filter DataFrame for requested parameters and time range
            df = filter_time(df, req.start, req.end)

            # Drop empty rows
            df = df.dropna(how="all")

            return df

        except Exception:
            logger.error(
                f'Could not fetch data for provider "{provider}"',
                exc_info=True,
            )

    def _fetch_station_data(self, req: Request, station: Station) -> List[pd.DataFrame]:
        """
        Fetch data for a single weather station
        """
        fragments = []

        filtered_providers = provider_service.filter_providers(req, station)

        for provider in filtered_providers:
            df = self._fetch_provider_data(req, station, provider)

            # Continue if no data was returned
            if df is None:
                continue

            fragments.append(df)

        return fragments

    def _filter_data(self, req: Request, ts: TimeSeries) -> TimeSeries:
        """
        Filter time series data
        """
        excluded_providers = []

        if req.model is False:
            excluded_providers.extend(
                provider.id
                for provider in provider_service.providers
                if provider.grade
                in (
                    Grade.FORECAST,
                    Grade.ANALYSIS,
                )
            )

        # Return filtered time series
        return (
            ts.filter_providers(excluded_providers, exclude=True)
            if len(excluded_providers)
            else ts
        )

    def fetch(
        self,
        req: Request,
    ) -> TimeSeries:
        """
        Load meteorological time series data from different providers
        """
        # Convert stations to list if single Station
        stations = req.station if isinstance(req.station, list) else [req.station]

        logger.debug(
            f"{req.granularity} time series requested for {len(stations)} station(s)"
        )

        # Filter parameters
        req.parameters = parameter_service.filter_parameters(
            req.granularity, req.parameters
        )

        fragments = []

        # Go through all weather stations
        for station in stations:
            station_fragments = self._fetch_station_data(req, station)

            if len(station_fragments):
                fragments.extend(station_fragments)

        # Merge data in a single DataFrame
        df = (
            self.concat_fragments(fragments, req.parameters)
            if fragments
            else pd.DataFrame()
        )

        # Set data types
        df = schema_service.format(df, req.granularity)

        # Create time series
        ts = TimeSeries(
            req.granularity,
            req.station,
            df,
            req.start,
            req.end,
            req.timezone,
        )

        # Filter data & return
        return self._filter_data(req, ts)


data_service = DataService()
