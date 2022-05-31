"""
TimeSeries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Union
import numpy as np
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.core.cache import get_local_file_path, file_in_cache
from meteostat.core.loader import processing_handler, load_handler
from meteostat.utilities.mutations import localize, filter_time
from meteostat.utilities.validations import validate_series
from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.interface.point import Point
from meteostat.interface.meteodata import MeteoData


class TimeSeries(MeteoData):

    """
    TimeSeries class which provides features which are
    used across all time series classes
    """

    # The list of origin weather Stations
    _origin_stations: Union[pd.Index, None] = None

    # The start date
    _start: Union[datetime, None] = None

    # The end date
    _end: Union[datetime, None] = None

    # Include model data?
    _model: bool = True

    # Fetch source flags?
    _flags = bool = False

    def _load_flags(self, station: str, year: Union[int, None] = None) -> None:
        """
        Load flag file for a single station from Meteostat
        """

        # File name
        file = generate_endpoint_path(self.granularity, station, year, True)

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
                self._columns,
                {key: "string" for key in self._columns[self._first_met_col :]},
                self._parse_dates,
            )

            # Validate Series
            df = validate_series(df, station)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Localize time column
        if (
            self.granularity == Granularity.HOURLY
            and self._timezone is not None
            and len(df.index) > 0
        ):
            df = localize(df, self._timezone)

        # Filter time period and append to DataFrame
        if self._start and self._end:
            df = filter_time(df, self._start, self._end)

        return df

    def _get_flags(self) -> None:
        """
        Get all source flags
        """

        if len(self._stations) > 0:

            # Get list of datasets
            datasets = self._get_datasets()

            # Data Processings
            return processing_handler(
                datasets, self._load_flags, self.processes, self.threads
            )

        # Empty DataFrame
        return pd.DataFrame(columns=[*self._types])

    def _filter_model(self) -> None:
        """
        Remove model data from time series
        """

        columns = self._columns[self._first_met_col :]

        for col_name in columns:
            self._data.loc[
                (pd.isna(self._data[f"{col_name}_flag"]))
                | (self._data[f"{col_name}_flag"].str.contains(self._model_flag)),
                col_name,
            ] = np.NaN

        # Conditionally, remove flags from DataFrame
        if not self._flags:
            self._data.drop(
                map(lambda col_name: f"{col_name}_flag", columns), axis=1, inplace=True
            )

        # Drop NaN-only rows
        self._data.dropna(how="all", subset=columns, inplace=True)

    def _init_time_series(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start: datetime = None,
        end: datetime = None,
        model: bool = True,  # Include model data?
        flags: bool = False,  # Load source flags?
    ) -> None:
        """
        Common initialization for all time series, regardless
        of its granularity
        """

        # Set list of weather stations based on user
        # input or retrieve list of stations programatically
        # if location is a geographical point
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index
        elif isinstance(loc, Point):
            stations = loc.get_stations("daily", start, end, model)
            self._stations = stations.index
        else:
            if not isinstance(loc, list):
                loc = [loc]
            self._stations = pd.Index(loc)

        # Preserve settings
        self._start = start if self._start is None else self._start
        self._end = end if self._end is None else self._end
        self._model = model
        self._flags = flags

        # Get data for all weather stations
        self._data = self._get_data()

        # Load source flags through map file
        # if flags are explicitly requested or
        # model data is excluded
        if flags or not model:
            flags = self._get_flags()
            self._data = self._data.merge(
                flags, on=["station", "time"], how="left", suffixes=[None, "_flag"]
            )

        # Remove model data from DataFrame and
        # drop flags if not specified otherwise
        if not model:
            self._filter_model()

        # Interpolate data spatially if requested
        # location is a geographical point
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Clear cache if auto cleaning is enabled
        if self.max_age > 0 and self.autoclean:
            self.clear_cache()

    # Import methods
    from meteostat.series.normalize import normalize
    from meteostat.series.interpolate import interpolate
    from meteostat.series.aggregate import aggregate
    from meteostat.series.convert import convert
    from meteostat.series.coverage import coverage
    from meteostat.series.count import count
    from meteostat.series.fetch import fetch
    from meteostat.series.stations import stations
    from meteostat.core.cache import clear_cache
