"""
Hourly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from math import floor
from datetime import datetime, timedelta
from typing import Optional, Union
import pytz
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.utilities.aggregations import degree_mean
from meteostat.interface.timeseries import TimeSeries
from meteostat.interface.point import Point
from meteostat.utilities.mutations import calculate_dwpt


class Hourly(TimeSeries):
    """
    Retrieve hourly weather observations for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir = "hourly"

    # Granularity
    granularity = Granularity.HOURLY

    # Download data as annual chunks
    # This cannot be changed and is only kept for backward compatibility
    chunked = True

    # The time zone
    _timezone: Optional[str] = None

    # Default frequency
    _freq = "1h"

    # Source mappings
    _source_mappings = {
        "metar": "D",
        "model": "E",
        "isd_lite": "B",
        "synop": "C",
        "dwd_poi": "C",
        "dwd_hourly": "A",
        "dwd_mosmix": "E",
        "metno_forecast": "E",
        "eccc_hourly": "A",
    }

    # Flag which represents model data
    _model_flag = "E"

    # Raw data columns
    _columns = [
        "year",
        "month",
        "day",
        "hour",
        "temp",
        {"dwpt": calculate_dwpt},
        "rhum",
        "prcp",
        {"snow": "snwd"},
        "wdir",
        "wspd",
        "wpgt",
        "pres",
        "tsun",
        "coco",
    ]

    # Index of first meteorological column
    _first_met_col = 4

    # Columns for date parsing
    _parse_dates = ["year", "month", "day", "hour"]

    # Default aggregation functions
    aggregations = {
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
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timezone: Optional[str] = None,
    ) -> None:
        """
        Set & adapt the period's time zone
        """
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
            self._annual_steps = [
                start.year + i for i in range(end.year - start.year + 1)
            ]

        self._start = start
        self._end = end

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start=datetime(1890, 1, 1, 0, 0, 0),
        end=datetime.combine(
            datetime.today().date() + timedelta(days=10), datetime.max.time()
        ),
        timezone: Optional[str] = None,
        model=True,  # Include model data?
        flags=False,  # Load source flags?
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
