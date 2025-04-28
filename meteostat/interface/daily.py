"""
Daily Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime, timedelta
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
    cache_subdir = "daily"

    # Granularity
    granularity = Granularity.DAILY

    # Download data as annual chunks
    # This cannot be changed and is only kept for backward compatibility
    chunked = True

    # Default frequency
    _freq = "1D"

    # Source mappings
    _source_mappings = {
        "dwd_daily": "A",
        "eccc_daily": "A",
        "ghcnd": "B",
        "dwd_hourly": "C",
        "eccc_hourly": "C",
        "isd_lite": "D",
        "synop": "E",
        "dwd_poi": "E",
        "metar": "F",
        "model": "G",
        "dwd_mosmix": "G",
        "metno_forecast": "G",
    }

    # Flag which represents model data
    _model_flag = "G"

    # Columns
    _columns = [
        "year",
        "month",
        "day",
        {"tavg": "temp"},
        "tmin",
        "tmax",
        "prcp",
        {"snow": "snwd"},
        {"wdir": None},
        "wspd",
        "wpgt",
        "pres",
        "tsun",
    ]

    # Index of first meteorological column
    _first_met_col = 3

    # Columns for date parsing
    _parse_dates = ["year", "month", "day"]

    # Default aggregation functions
    aggregations = {
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
        start=datetime(1781, 1, 1, 0, 0, 0),
        end=datetime.combine(
            datetime.today().date() + timedelta(days=10), datetime.max.time()
        ),
        model=True,  # Include model data?
        flags=False,  # Load source flags?
    ) -> None:
        # Extract relevant years
        if self.chunked:
            self._annual_steps = [
                start.year + i for i in range(end.year - start.year + 1)
            ]
        # Initialize time series
        self._init_time_series(loc, start, end, model, flags)

    def expected_rows(self) -> int:
        """
        Return the number of rows expected for the defined date range
        """

        return (self._end - self._start).days + 1
