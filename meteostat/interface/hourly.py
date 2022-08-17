"""
Hourly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from math import floor
from datetime import datetime, timedelta
from typing import Union
import pytz
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.utilities.aggregations import degree_mean
from meteostat.interface.timeseries import TimeSeries
from meteostat.interface.point import Point


class Hourly(TimeSeries):

    """
    Retrieve hourly weather observations for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = "hourly"

    # Granularity
    granularity = Granularity.HOURLY

    # Download data as annual chunks
    chunked: bool = True

    # The time zone
    _timezone: str = None

    # Default frequency
    _freq: str = "1H"

    # Flag which represents model data
    _model_flag = "E"

    # Raw data columns
    _columns: list = [
        "date",
        "hour",
        "temp",
        "dwpt",
        "rhum",
        "prcp",
        "snow",
        "wdir",
        "wspd",
        "wpgt",
        "pres",
        "tsun",
        "coco",
    ]

    # Index of first meteorological column
    _first_met_col = 2

    # Data types
    _types: dict = {
        "temp": "float64",
        "dwpt": "float64",
        "rhum": "float64",
        "prcp": "float64",
        "snow": "float64",
        "wdir": "float64",
        "wspd": "float64",
        "wpgt": "float64",
        "pres": "float64",
        "tsun": "float64",
        "coco": "float64",
    }

    # Columns for date parsing
    _parse_dates: dict = {"time": [0, 1]}

    # Default aggregation functions
    aggregations: dict = {
        "temp": "mean",
        "dwpt": "mean",
        "rhum": "mean",
        "prcp": "sum",
        "snow": "max",
        "wdir": degree_mean,
        "wspd": "mean",
        "wpgt": "max",
        "pres": "mean",
        "tsun": "sum",
        "coco": "max",
    }

    def _set_time(
        self, start: datetime = None, end: datetime = None, timezone: str = None
    ) -> None:
        """
        Set & adapt the period's time zone
        """

        # Don't use chunks if full dataset is requested
        if start == None:
            self.chunked = False

        if timezone:
            # Save timezone
            self._timezone = timezone

            if start and end:

                # Initialize time zone
                timezone = pytz.timezone(self._timezone)

                # Set start date
                start = timezone.localize(start, is_dst=None).astimezone(pytz.utc)

                # Set end date
                end = timezone.localize(end, is_dst=None).astimezone(pytz.utc)

        if self.chunked:
            self._annual_steps = list(
                set(
                    [
                        (start + timedelta(days=365 * i)).year
                        for i in range(end.year - start.year + 2)
                    ]
                )
            )

        self._start = start
        self._end = end

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start: datetime = None,
        end: datetime = None,
        timezone: str = None,
        model: bool = True,  # Include model data?
        flags: bool = False,  # Load source flags?
    ) -> None:

        # Set time zone and adapt period
        self._set_time(start, end, timezone)

        # Initialize time series
        self._init_time_series(loc, start, end, model, flags)

    def expected_rows(self) -> int:
        """
        Return the number of rows expected for the defined date range
        """

        return floor((self._end - self._start).total_seconds() / 3600) + 1
