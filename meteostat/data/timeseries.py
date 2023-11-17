"""
TimeSeries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
import pandas as pd
from meteostat import Granularity
from meteostat.types import Station
from .collection import Collection

class Timeseries(Collection):
    """
    TimeSeries class which provides features which are
    used across all granularities
    """
    _granularity: Granularity
    _expected_row_count: int

    def __init__(
        self,
        granularity: Granularity,
        stations: list[Station],
        df: pd.DataFrame,
        squash: bool,
        expected_row_count: int
    ) -> None:
        self._granularity = granularity
        self._stations = stations
        self._squash = squash
        self._df = df
        self._expected_row_count = expected_row_count

    def fill():
        """
        Force specific granularity on the time series
        """
        pass