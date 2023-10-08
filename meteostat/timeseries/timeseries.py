"""
TimeSeries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""
import polars as pl
from meteostat import Collection, Granularity

class Timeseries(Collection):
    """
    TimeSeries class which provides features which are
    used across all granularities
    """

    granularity: Granularity = None
    expected_row_count: int

    def __init__(self, df: pl.DataFrame, expected_row_count: int) -> None:
        self._df = df
        self.expected_row_count = expected_row_count

    def fill():
        """
        Force specific granularity on the time series
        """
        pass