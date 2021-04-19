"""
Monthly Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from datetime import datetime
from typing import Union
from numpy import NaN
import numpy as np
import pandas as pd
from meteostat.interface.base import Base
from meteostat.interface.point import Point


class Monthly(Base):

    """
    Retrieve monthly weather data for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = 'monthly'

    # The list of weather Stations
    stations: pd.Index = None

    # The start date
    start: datetime = None

    # The end date
    end: datetime = None

    # Include model data?
    model: bool = True

    # The data frame
    data: pd.DataFrame = pd.DataFrame()

    # Default frequency
    freq: str = '1MS'

    # Columns
    _columns: list = [
        'year',
        'month',
        'tavg',
        'tmin',
        'tmax',
        'prcp',
        'snow',
        'wdir',
        'wspd',
        'wpgt',
        'pres',
        'tsun'
    ]

    # Data tapes
    _types: dict = {
        'tavg': 'float64',
        'tmin': 'float64',
        'tmax': 'float64',
        'prcp': 'float64',
        'snow': 'float64',
        'wdir': 'float64',
        'wspd': 'float64',
        'wpgt': 'float64',
        'pres': 'float64',
        'tsun': 'float64'
    }

    # Columns for date parsing
    _parse_dates: dict = {
        'time': [0, 1]
    }

    # Default aggregation functions
    _aggregations: dict = {
        'tavg': 'mean',
        'tmin': 'min',
        'tmax': 'max',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': Base._degree_mean,
        'wspd': 'mean',
        'wpgt': 'max',
        'pres': 'mean',
        'tsun': 'sum'
    }

    def _load(
        self,
        station: str
    ) -> None:
        """
        Load file from Meteostat
        """

        # File name
        file = 'monthly/' + ('full' if self.model else 'obs') + \
            '/' + station + '.csv.gz'

        # Get local file path
        path = self._get_file_path(self.cache_subdir, file)

        # Check if file in cache
        if self.max_age > 0 and self._file_in_cache(path):

            # Read cached data
            df = pd.read_pickle(path)

        else:

            # Get data from Meteostat
            df = self._load_handler(
                file,
                self._columns,
                self._types,
                self._parse_dates)

            # Validate Series
            df = self._validate_series(df, station)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Filter time period and append to DataFrame
        if self.start and self.end:

            # Get time index
            time = df.index.get_level_values('time')

            # Filter & append
            self.data = self.data.append(
                df.loc[(time >= self.start) & (time <= self.end)])

        else:

            # Append
            self.data = self.data.append(df)

    def _get_data(self) -> None:
        """
        Get all required data
        """

        if len(self.stations) > 0:

            # List of datasets
            datasets = []

            for station in self.stations:
                datasets.append((
                    str(station),
                ))

            # Data Processing
            self._processing_handler(datasets, self._load, self.max_threads)

        else:

            # Empty DataFrame
            self.data = pd.DataFrame(columns=[*self._types])

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

        if self.stations.size == 0:
            return None

        if method == 'nearest':

            self.data = self.data.groupby(
                pd.Grouper(level='time', freq='1D')).agg('first')

        else:

            # Join score and elevation of involved weather stations
            data = self.data.join(
                stations[['score', 'elevation']], on='station')

            # Adapt temperature-like data based on altitude
            if adapt_temp:
                data.loc[data['tavg'] != np.NaN, 'tavg'] = data['tavg'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))
                data.loc[data['tmin'] != np.NaN, 'tmin'] = data['tmin'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))
                data.loc[data['tmax'] != np.NaN, 'tmax'] = data['tmax'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))

            # Exclude non-mean data & perform aggregation
            excluded = data['wdir']
            excluded = excluded.groupby(
                pd.Grouper(level='time', freq='1D')).agg('first')

            # Aggregate mean data
            data = data.groupby(
                pd.Grouper(level='time', freq='1D')).apply(self._weighted_average)

            # Drop RangeIndex
            data.index = data.index.droplevel(1)

            # Merge excluded fields
            data['wdir'] = excluded

            # Drop score and elevation
            self.data = data.drop(['score', 'elevation'], axis=1).round(1)

        # Set placeholder station ID
        self.data['station'] = 'XXXXX'
        self.data = self.data.set_index(
            ['station', self.data.index.get_level_values('time')])
        self.stations = pd.Index(['XXXXX'])

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        start: datetime = None,
        end: datetime = None,
        model: bool = True
    ) -> None:

        # Set list of weather stations
        if isinstance(loc, pd.DataFrame):
            self.stations = loc.index
        elif isinstance(loc, Point):
            stations = loc.get_stations('hourly', start, end)
            self.stations = stations.index
        else:
            if not isinstance(loc, list):
                loc = [loc]

            self.stations = pd.Index(loc)

        # Set start date
        self.start = start

        # Set end date
        self.end = end

        # Set model
        self.model = model

        # Get data for all weather stations
        self._get_data()

        # Interpolate data
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Clear cache
        if self.max_age > 0:
            self.clear_cache()

    # Import methods
    from meteostat.shared.normalize import normalize
    from meteostat.shared.interpolate import interpolate
    from meteostat.shared.aggregate import aggregate
    from meteostat.shared.convert import convert
    from meteostat.shared.coverage import coverage
    from meteostat.shared.count import count
    from meteostat.shared.fetch import fetch
