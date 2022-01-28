"""
Timeseries Class

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
from meteostat.utilities.validations import validate_series
from meteostat.utilities.aggregations import weighted_average
from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.interface.point import Point
from meteostat.interface.base import Base


class Timeseries(Base):

    """
    Timeseries class which provides features which are used across all time series classes
    """

    # The list of weather Stations
    _stations: Union[pd.Index, None] = None

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

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    @staticmethod
    def _localize(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
        """
        Convert time data to any time zone
        """

        return df.tz_localize(
            'UTC',
            level='time'
        ).tz_convert(
            timezone,
            level='time'
        )

    @staticmethod
    def _filter_time(df: pd.DataFrame, start: datetime,
                     end: datetime) -> pd.DataFrame:
        """
        Filter time series data based on start and end date
        """

        # Get time index
        time = df.index.get_level_values('time')

        # Filter & return
        return df.loc[(time >= start) & (time <= end)]

    def _load_data(
        self,
        station: str,
        year: Union[int, None] = None
    ) -> None:
        """
        Load file for a single station from Meteostat
        """

        # File name
        file = generate_endpoint_path(
            self.granularity,
            station,
            year
        )

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
                self._types,
                self._parse_dates)

            # Validate Series
            df = validate_series(df, station)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Localize time column
        if self.granularity == Granularity.HOURLY and self._timezone is not None and len(
                df.index) > 0:
            df = Timeseries._localize(df, self._timezone)

        # Filter time period and append to DataFrame
        if self._start and self._end:
            df = Timeseries._filter_time(df, self._start, self._end)

        # Return
        return df

    def _load_flags(
        self,
        station: str,
        year: Union[int, None] = None
    ) -> None:
        """
        Load flag file for a single station from Meteostat
        """

        # File name
        file = generate_endpoint_path(
            self.granularity,
            station,
            year,
            True
        )

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
                None,
                self._parse_dates)

            # Validate Series
            df = validate_series(df, station)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Localize time column
        if self.granularity == Granularity.HOURLY and self._timezone is not None and len(
                df.index) > 0:
            df = Timeseries._localize(df, self._timezone)

        # Filter time period and append to DataFrame
        if self._start and self._end:
            df = Timeseries._filter_time(df, self._start, self._end)

        return df

    def _get_datasets(self) -> list:
        """
        Get list of datasets
        """

        if self.granularity == Granularity.HOURLY and self.chunked:
            datasets = [(str(station), year)
                        for station in self._stations for year in self._annual_steps]
        else:
            datasets = [(str(station),) for station in self._stations]

        return datasets

    def _get_data(self) -> None:
        """
        Get all required data dumps
        """

        if len(self._stations) > 0:

            # Get list of datasets
            datasets = self._get_datasets()

            # Data Processings
            return processing_handler(
                datasets,
                self._load_data,
                self.processes,
                self.threads
            )

        # Empty DataFrame
        return pd.DataFrame(columns=[*self._types])

    def _get_flags(self) -> None:
        """
        Get all source flags
        """

        if len(self._stations) > 0:

            # Get list of datasets
            datasets = self._get_datasets()

            # Data Processings
            return processing_handler(
                datasets,
                self._load_flags,
                self.processes,
                self.threads
            )

        # Empty DataFrame
        return pd.DataFrame(columns=[*self._types])

    @staticmethod
    def adjust_temp(df: pd.DataFrame, alt: int):
        """
        Adjust temperature-like data based on altitude
        """

        # Temperature-like columns
        temp_like = ('temp', 'dwpt', 'tavg', 'tmin', 'tmax')

        # Adjust values for all temperature-like data
        for col_name in temp_like:
            if col_name in df.columns:
                df.loc[df[col_name] != np.NaN, col_name] = df[col_name] + \
                    ((2 / 3) * ((df['elevation'] - alt) / 100))

        return df

    def _resolve_point(
        self,
        method: str,
        stations: pd.DataFrame,
        alt: int,
        adapt_temp: bool
    ) -> None:
        """
        Project weather station data onto a single point
        """

        if self._stations.size == 0 or self._data.size == 0:
            return None

        if method == 'nearest':

            if adapt_temp:

                # Join elevation of involved weather stations
                data = self._data.join(
                    stations['elevation'], on='station')

                # Adapt temperature-like data based on altitude
                data = Timeseries.adjust_temp(data, alt)

                # Drop elevation & round
                data = data.drop('elevation', axis=1).round(1)

            else:

                data = self._data

            self._data = data.groupby(
                pd.Grouper(level='time', freq=self._freq)).agg('first')

        else:

            # Join score and elevation of involved weather stations
            data = self._data.join(
                stations[['score', 'elevation']], on='station')

            # Adapt temperature-like data based on altitude
            if adapt_temp:
                data = Timeseries.adjust_temp(data, alt)

            # Exclude non-mean data & perform aggregation
            excluded = data['wdir']
            excluded = excluded.groupby(
                pd.Grouper(level='time', freq=self._freq)).agg('first')

            # Aggregate mean data
            data = data.groupby(
                pd.Grouper(level='time', freq=self._freq)).apply(weighted_average)

            # Drop RangeIndex
            data.index = data.index.droplevel(1)

            # Merge excluded fields
            data['wdir'] = excluded

            # Drop score and elevation
            self._data = data.drop(['score', 'elevation'], axis=1).round(1)

        # Set placeholder station ID
        self._data['station'] = 'XXXXX'
        self._data = self._data.set_index(
            ['station', self._data.index.get_level_values('time')])
        self._stations = pd.Index(['XXXXX'])

    def _filter_model(self) -> None:
        """
        Remove model data from time series
        """

        columns = self._columns[self._first_met_col:]

        for col_name in columns:
            self._data.loc[self._data[f'{col_name}_flag']
                           == 'M', col_name] = np.NaN

        # Drop NaN-only rows
        self._data.dropna(how='all', inplace=True)

        # Conditionally, remove flags from DataFrame
        if not self._flags:
            self._data.drop(
                map(lambda col_name: f'{col_name}_flag', columns),
                axis=1,
                inplace=True)

    def _init_timeseries(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start: datetime = None,
        end: datetime = None,
        model: bool = True,  # Include model data?
        flags: bool = False  # Load source flags?
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
            stations = loc.get_stations('daily', start, end, model)
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
                flags,
                on=['station', 'time'],
                how='left',
                suffixes=[None, '_flag'])

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
