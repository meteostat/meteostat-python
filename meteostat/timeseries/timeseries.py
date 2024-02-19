"""
TimeSeries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
from copy import copy
from datetime import datetime
from math import floor
from statistics import mean
from typing import Any, Callable, Optional, Tuple
import pandas as pd
from meteostat.enumerations import Parameter, Granularity
from meteostat.utils.helpers import get_freq, get_index, get_provider_prio
from meteostat.utils.mutations import fill_df, localize, squash_df


class TimeSeries:
    """
    TimeSeries class which provides features which are
    used across all granularities
    """

    granularity: Granularity
    stations: pd.DataFrame
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    timezone: Optional[str] = None

    _df: Optional[pd.DataFrame] = None

    def __init__(
        self,
        granularity: Granularity,
        stations: pd.DataFrame,
        df: Optional[pd.DataFrame],
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timezone: Optional[str] = None,
    ) -> None:
        self.granularity = granularity
        self.stations = stations
        if df is not None and not df.empty:
            self._df = df
            self.start = start if start else df.index.get_level_values("time").min()
            self.end = end if end else df.index.get_level_values("time").max()
        self.timezone = timezone

    def __len__(self) -> int:
        """
        Return number of rows in DataFrame
        """
        return len(self._df) if self._df is not None else 0

    def __str__(self) -> str:
        return self._df.__str__() if self._df is not None else "Empty time series"

    @property
    def empty(self) -> bool:
        """
        Is the time series empty?
        """
        return True if self._df is None else self._df.empty

    @property
    def target_length(self) -> int:
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
    def sourcemap(self) -> Optional[pd.DataFrame]:
        """
        Get a DataFrame of squashed source strings
        """
        if self._df is None:
            return None

        df = copy(self._df)

        df["source_prio"] = df.index.get_level_values("source").map(get_provider_prio)

        return (
            df.sort_values(by="source_prio", ascending=False)
            .groupby(["station", "time"])
            .agg(lambda s: get_index(pd.Series.first_valid_index(s), 2))
            .drop("source_prio", axis=1)
            .convert_dtypes()
        )

    def apply(
        self,
        func: Callable,
        parameter: Optional[Tuple[Parameter | str, ...] | Parameter | str] = None,
    ):
        """
        Apply a function to the whole time series or specific parameter(s)
        """
        temp = copy(self)

        if parameter:
            for p in (
                [parameter] if isinstance(parameter, (Parameter, str)) else parameter
            ):
                if p in temp._df.columns:
                    temp._df[p] = temp._df[p].apply(func)
        else:
            temp._df = temp._df.apply(func)

        return temp

    def merge(self, objs: list[Any]) -> Any:
        """
        Merge one or multiple Meteostat time series into the current one
        """
        temp = copy(self)

        if not all(
            obj.granularity == temp.granularity
            and obj.start == temp.start
            and obj.end == temp.end
            and obj.timezone == temp.timezone
            for obj in objs
        ):
            raise ValueError(
                "Can't concatenate time series objects with divergent granularity, start, end or timezone"
            )

        for obj in objs:
            temp._df = pd.concat([temp._df, obj._df], verify_integrity=True)
            temp.stations = pd.concat([temp.stations, obj.stations]).drop_duplicates()

        return temp

    def fetch(self, squash=True, fill=False, sources=False) -> Optional[pd.DataFrame]:
        """
        Force specific granularity on the time series
        """
        df = copy(self._df)

        if df is None:
            return None

        if squash:
            df = squash_df(df)

        if squash and sources:
            sourcemap = self.sourcemap
            df = df.join(sourcemap, rsuffix="_source")

        if fill:
            df = fill_df(df, self.start, self.end, get_freq(self.granularity))

        if self.timezone:
            df = localize(df, self.timezone)

        return df.sort_index().convert_dtypes()

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
                self.count(parameter) / self.target_length,
                2,
            )

        return round(mean([self.completeness(p) for p in df.columns]), 2)
