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
import pandas as pd
from meteostat import Granularity
from meteostat.enumerations import Parameter
from meteostat.types import Station
from meteostat.utils.mutations import fill_df, localize, squash_df


class Timeseries:
    """
    TimeSeries class which provides features which are
    used across all granularities
    """

    _granularity: Granularity
    _df = pd.DataFrame()
    _stations: list[Station] = []
    _start: datetime
    _end: datetime
    _timezone: str

    def __init__(
        self,
        granularity: Granularity,
        stations: list[Station],
        df: pd.DataFrame,
        start: datetime | None = None,
        end: datetime | None = None,
        timezone: str = None,
    ) -> None:
        self._granularity = granularity
        self._stations = stations
        self._df = df
        if not start:
            start = df.index.get_level_values("time").min()
        self._start = start
        if not end:
            end = df.index.get_level_values("time").max()
        self._end = end
        self._timezone = timezone

    def _get_expected_row_count(self) -> int:
        diff = self._end - self._start
        return (
            diff.days + 1
            if self._granularity is Granularity.DAILY
            else floor(diff.total_seconds() / 3600) + 1
        ) * len(self._stations)

    def fetch(self, squash=True, fill=False):
        """
        Force specific granularity on the time series
        """
        df = copy(self._df)

        if squash:
            df = squash_df(df)

        if fill:
            df = fill_df(
                df,
                self._start,
                self._end,
                "H" if self._granularity is Granularity.HOURLY else "D",
            )

        if self._timezone:
            df = localize(df, self._timezone)

        return df.sort_index()

    def coverage(self, parameter: Parameter | str | None = None) -> float:
        """
        Get coverage for a specific parameter or the whole DataFrame
        """
        df = self.fetch()

        if parameter:
            return round(
                df[
                    parameter.value if isinstance(parameter, Parameter) else parameter
                ].count()
                / self._get_expected_row_count(),
                2,
            )

        return round(mean([self.coverage(p) for p in df.columns]), 2)
