"""
Monthly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Union
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.interface.timeseries import TimeSeries
from meteostat.interface.point import Point


class Monthly(TimeSeries):

    """
    Retrieve monthly weather data for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = "monthly"

    # Granularity
    granularity = Granularity.MONTHLY

    # Default frequency
    _freq: str = "1MS"

    # Flag which represents model data
    _model_flag = "I"

    # Columns
    _columns: list = [
        "year",
        "month",
        "tavg",
        "tmin",
        "tmax",
        "prcp",
        "wspd",
        "pres",
        "tsun",
    ]

    # Index of first meteorological column
    _first_met_col = 2

    # Data types
    _types: dict = {
        "tavg": "float64",
        "tmin": "float64",
        "tmax": "float64",
        "prcp": "float64",
        "wspd": "float64",
        "pres": "float64",
        "tsun": "float64",
    }

    # Columns for date parsing
    _parse_dates: dict = {"time": [0, 1]}

    # Default aggregation functions
    aggregations: dict = {
        "tavg": "mean",
        "tmin": "mean",
        "tmax": "mean",
        "prcp": "sum",
        "wspd": "mean",
        "pres": "mean",
        "tsun": "sum",
    }

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start: datetime = None,
        end: datetime = None,
        model: bool = True,  # Include model data?
        flags: bool = False,  # Load source flags?
    ) -> None:

        # Set start date
        if start is not None:
            start = start.replace(day=1)

        # Initialize time series
        self._init_time_series(loc, start, end, model, flags)

    def expected_rows(self) -> int:
        """
        Return the number of rows expected for the defined date range
        """

        return (
            (self._end.year - self._start.year) * 12
            + self._end.month
            - self._start.month
        ) + 1
