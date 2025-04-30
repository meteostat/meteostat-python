"""
Normals Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from typing import Optional, Union
from datetime import datetime
import numpy as np
import pandas as pd
from meteostat.core.cache import file_in_cache, get_local_file_path
from meteostat.core.loader import load_handler
from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.enumerations.granularity import Granularity
from meteostat.core.warn import warn
from meteostat.interface.meteodata import MeteoData
from meteostat.interface.point import Point


class Normals(MeteoData):
    """
    Retrieve climate normals for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir = "normals"

    # Granularity
    granularity = Granularity.NORMALS

    # The list of weather Stations
    _stations: Optional[pd.Index] = None

    # The first year of the period
    _start: Optional[int] = None

    # The last year of the period
    _end: Optional[int] = None

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    # Columns
    _columns = [
        "start",
        "end",
        "month",
        "tmin",
        "tmax",
        "prcp",
        "wspd",
        "pres",
        "tsun",
    ]

    # Index of first meteorological column
    _first_met_col = 3

    # Which columns should be parsed as dates?
    _parse_dates = None

    def _load_data(self, station: str, year: Optional[int] = None) -> None:
        """
        Load file for a single station from Meteostat
        """

        # File name
        file = generate_endpoint_path(self.granularity, station, year)

        # Get local file path
        path = get_local_file_path(self.cache_dir, self.cache_subdir, file)

        # Check if file in cache
        if self.max_age > 0 and file_in_cache(path, self.max_age):
            # Read cached data
            df = pd.read_pickle(path)

        else:
            # Get data from Meteostat
            df = load_handler(
                self.endpoint,
                file,
                self.proxy,
                self._columns,
            )

            # Validate and prepare data for further processing
            if not df.empty:
                # Add weather station ID
                df["station"] = station

                # Set index
                df = df.set_index(["station", "start", "end", "month"])

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Filter time period and append to DataFrame
        if self.granularity == Granularity.NORMALS and not df.empty and self._end:
            # Get time index
            end = df.index.get_level_values("end")
            # Filter & return
            return df.loc[end == self._end]

        # Return
        return df

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        start: int = None,
        end: int = None,
    ) -> None:
        # Set list of weather stations
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index

        elif isinstance(loc, Point):
            if start and end:
                stations = loc.get_stations(
                    "monthly", datetime(start, 1, 1), datetime(end, 12, 31)
                )
            else:
                stations = loc.get_stations()

            self._stations = stations.index

        else:
            if not isinstance(loc, list):
                loc = [loc]

            self._stations = pd.Index(loc)

        # Check period
        if (start and end) and (
            end - start != 29 or end % 10 != 0 or end >= datetime.now().year
        ):
            raise ValueError("Invalid reference period")

        # Set period
        self._start = start
        self._end = end

        # Get data for all weather stations
        self._data = self._get_data()

        # Interpolate data
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Clear cache
        if self.max_age > 0 and self.autoclean:
            self.clear_cache()

    def normalize(self):
        """
        Normalize the DataFrame
        """

        # Create temporal instance
        temp = copy(self)

        if self.count() == 0:
            warn("Pointless normalization of empty DataFrame")

        # Go through list of weather stations
        for station in temp._stations:
            # The list of periods
            periods: pd.Index = pd.Index([])
            # Get periods
            if self.count() > 0:
                periods = temp._data[
                    temp._data.index.get_level_values("station") == station
                ].index.unique("end")
            elif periods.size == 0 and self._end:
                periods = pd.Index([self._end])
            # Go through all periods
            for period in periods:
                # Create DataFrame
                df = pd.DataFrame(
                    columns=temp._columns[temp._first_met_col :], dtype="float64"
                )
                # Populate index columns
                df["month"] = range(1, 13)
                df["station"] = station
                df["start"] = period - 29
                df["end"] = period
                # Set index
                df.set_index(["station", "start", "end", "month"], inplace=True)
                # Merge data
                temp._data = (
                    pd.concat([temp._data, df], axis=0)
                    .groupby(["station", "start", "end", "month"], as_index=True)
                    .first()
                    if temp._data.index.size > 0
                    else df
                )

        # None -> nan
        temp._data = temp._data.fillna(np.nan)

        # Return class instance
        return temp

    def fetch(self) -> pd.DataFrame:
        """
        Fetch DataFrame
        """

        # Copy DataFrame
        temp = copy(self._data)

        # Add avg. temperature column
        temp.insert(
            0, "tavg", temp[["tmin", "tmax"]].dropna(how="any").mean(axis=1).round(1)
        )

        # Remove station index if it's a single station
        if len(self._stations) == 1 and "station" in temp.index.names:
            temp = temp.reset_index(level="station", drop=True)

        # Remove start & end year if period is set
        if self._start and self._end and self.count() > 0:
            temp = temp.reset_index(level="start", drop=True)
            temp = temp.reset_index(level="end", drop=True)

        # Return data frame
        return temp

    # Import methods
    from meteostat.series.convert import convert
    from meteostat.series.count import count
    from meteostat.core.cache import clear_cache
