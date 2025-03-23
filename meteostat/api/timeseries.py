"""
TimeSeries Class

A class to handle meteorological time series data.
"""
from copy import copy
from datetime import datetime
from math import floor
from statistics import mean
from typing import List, Optional
import pandas as pd
from meteostat.core.parameters import parameter_service
from meteostat.core.schema import schema_service
from meteostat.enumerations import Parameter, Granularity, Provider
from meteostat.typing import License, Station
from meteostat.utils.mutations import fill_df, localize, squash_df


class TimeSeries:
    """
    TimeSeries class which provides features which are
    used across all granularities
    """

    granularity: Granularity
    stations: List[Station]
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    timezone: Optional[str] = None

    _df: Optional[pd.DataFrame] = None

    def __init__(
        self,
        granularity: Granularity,
        stations: List[Station],
        df: Optional[pd.DataFrame],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timezone: Optional[str] = None,
    ) -> None:
        self.granularity = granularity
        self.stations = stations
        self.timezone = timezone
        if df is not None and not df.empty:
            self._df = df
            self.start = start if start else df.index.get_level_values("time").min()
            self.end = end if end else df.index.get_level_values("time").max()

    def __len__(self) -> int:
        """
        Return number of rows in DataFrame
        """
        return len(self._df) if self._df is not None else 0

    def __str__(self) -> str:
        """
        Return a stringified version of the DataFrame
        """
        return self._df.__str__() if self._df is not None else "Empty time series"

    @property
    def _target_length(self) -> int:
        """
        Expected number of non-NaN values
        """
        if not self.start or not self.end:
            return 0

        diff = self.end - self.start

        return (
            diff.days + 1
            if self.granularity is Granularity.DAILY
            else floor(diff.total_seconds() / 3600) + 1
        ) * len(self.stations)
    
    @property
    def parameters(self) -> List[Parameter]:
        """
        Get parameters
        """
        return self._df.columns.to_list() if self._df is not None else []

    @property
    def freq(self) -> str:
        """
        The time series frequency
        """
        return "1h" if self.granularity is Granularity.HOURLY else "1D"

    @property
    def empty(self) -> bool:
        """
        Is the time series empty?
        """
        return True if self._df is None else self._df.empty

    @property
    def attribution(self) -> str:
        """
        Get attribution string
        """
        attributions = [
            "Meteostat",
            *[
                provider.license.attribution
                for provider in self.providers
                if provider.license.attribution
            ],
        ]

        return ", ".join(attributions)

    @property
    def commercial(self) -> bool:
        """
        Is commercial use allowed?
        """
        return all([provider.license.commercial for provider in self.providers])

    @property
    def licenses(self) -> List[License]:
        """
        Get licenses
        """
        return [provider.license for provider in self.providers]

    @property
    def is_valid(self) -> bool:
        """
        Does the time series pass all validations?
        """
        df = self.fetch(fill=True, clean=False)

        for col in df:
            parameter = parameter_service.get_parameter(col, self.granularity)

            for validator in parameter.validators:
                test = validator(df[col])

                if not test.all():
                    return False

        return True

    @property
    def stations_df(self) -> pd.DataFrame:
        """
        Get included weather stations as DataFrame
        """
        return (
            pd.DataFrame.from_records(
                [
                    {
                        "id": station.id,
                        "name": station.name,
                        "country": station.country,
                        "latitude": station.latitude,
                        "longitude": station.longitude,
                        "elevation": station.elevation,
                        "timezone": station.timezone,
                    }
                    for station in self.stations
                ],
                index="id",
            )
            if len(self.stations)
            else []
        )

    def filter_stations(self, station: str | List[str], exclude=False) -> "TimeSeries":
        """
        Filter data by weather station(s)
        """
        temp = copy(self)
        mask = self._df.index.get_level_values("station").isin(
            station if isinstance(station, list) else [station]
        )
        temp._df = temp._df[mask if not exclude else ~mask]
        return temp

    def filter_providers(
        self, provider: Provider | List[Provider], exclude=False, strict=True
    ) -> "TimeSeries":
        """
        Filter data by provider(s)
        """
        temp = copy(self)
        mask = self._df.index.get_level_values("source").isin(
            provider if isinstance(provider, list) else [provider]
        )
        temp._df = temp._df[mask if not exclude else ~mask]
        return temp

    def fetch(
        self,
        squash=True,
        fill=False,
        sources=False,
        location=False,
        clean=True,
    ) -> Optional[pd.DataFrame]:
        """
        Force specific granularity on the time series
        """
        df = copy(self._df)

        if df is None:
            return None

        if squash:
            df = squash_df(df, sources=sources)

        if clean:
            df = schema_service.clean(df, self.granularity)

        if fill:
            df = fill_df(df, self.start, self.end, self.freq)

        if self.timezone:
            df = localize(df, self.timezone)

        if location:
            df = df.join(
                self.stations_df[["latitude", "longitude", "elevation"]], on="station"
            )

        return df.sort_index()

    def count(self, parameter: Parameter | str) -> int:
        """
        Get number of non-NaN values for a specific parameter
        """
        if self._df is None:
            return 0

        return self._df[
            parameter if isinstance(parameter, Parameter) else parameter
        ].count()

    def completeness(self, parameter: Parameter | str | None = None) -> float:
        """
        Get completeness for a specific parameter or the whole DataFrame
        """
        df = self.fetch()

        if df is None:
            return 0

        if parameter:
            return round(
                self.count(parameter) / self._target_length,
                2,
            )

        return round(mean([self.completeness(p) for p in df.columns]), 2)
