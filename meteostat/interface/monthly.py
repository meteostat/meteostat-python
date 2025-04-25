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
    cache_subdir = "monthly"

    # Granularity
    granularity = Granularity.MONTHLY

    # Default frequency
    _freq = "1MS"

    # Source mappings
    _source_mappings = {
        "dwd_monthly": "A",
        "eccc_monthly": "A",
        "dwd_daily": "C",
        "eccc_daily": "C",
        "ghcnd": "D",
        "dwd_hourly": "E",
        "eccc_hourly": "E",
        "isd_lite": "F",
        "synop": "G",
        "dwd_poi": "G",
        "metar": "H",
        "model": "I",
        "dwd_mosmix": "I",
        "metno_forecast": "I",
    }

    # Flag which represents model data
    _model_flag = "I"

    # Columns
    _columns = [
        "year",
        "month",
        {"tavg": "temp"},
        "tmin",
        "tmax",
        "prcp",
        "wspd",
        "pres",
        "tsun",
    ]

    # Index of first meteorological column
    _first_met_col = 2

    # Columns for date parsing
    _parse_dates = ["year", "month"]

    # Default aggregation functions
    aggregations = {
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
