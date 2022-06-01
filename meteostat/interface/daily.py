"""
Daily Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Union
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.utilities.aggregations import degree_mean
from meteostat.interface.timeseries import TimeSeries
from meteostat.interface.point import Point


class Daily(TimeSeries):

    """
    Retrieve daily weather observations for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = "daily"

    # Granularity
    granularity = Granularity.DAILY

    # Default frequency
    _freq: str = "1D"

    # Flag which represents model data
    _model_flag = "G"

    # Columns
    _columns: list = [
        "date",
        "tavg",
        "tmin",
        "tmax",
        "prcp",
        "snow",
        "wdir",
        "wspd",
        "wpgt",
        "pres",
        "tsun",
    ]

    # Index of first meteorological column
    _first_met_col = 1

    # Data types
    _types: dict = {
        "tavg": "float64",
        "tmin": "float64",
        "tmax": "float64",
        "prcp": "float64",
        "snow": "float64",
        "wdir": "float64",
        "wspd": "float64",
        "wpgt": "float64",
        "pres": "float64",
        "tsun": "float64",
    }

    # Columns for date parsing
    _parse_dates: dict = {"time": [0]}

    # Default aggregation functions
    aggregations: dict = {
        "tavg": "mean",
        "tmin": "min",
        "tmax": "max",
        "prcp": "sum",
        "snow": "max",
        "wdir": degree_mean,
        "wspd": "mean",
        "wpgt": "max",
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

        # Initialize time series
        self._init_time_series(loc, start, end, model, flags)

    def expected_rows(self) -> int:
        """
        Return the number of rows expected for the defined date range
        """

        return (self._end - self._start).days + 1
