"""
Daily Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from copy import copy
from datetime import datetime
from typing import Union
from numpy import NaN
import numpy as np
import pandas as pd
from meteostat.core import Core
from meteostat.point import Point


class Daily(Core):

    """
    Retrieve daily weather observations for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = 'daily'

    # The list of weather Stations
    stations = None

    # The start date
    start: datetime = None

    # The end date
    end: datetime = None

    # Include model data?
    model: bool = True

    # The data frame
    data = pd.DataFrame()

    # Columns
    _columns: list = [
        'date',
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
        'time': [0]
    }

    # Default aggregation functions
    _aggregations: dict = {
        'tavg': 'mean',
        'tmin': 'min',
        'tmax': 'max',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': Core._degree_mean,
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
        file = 'stations' + os.sep + 'daily' + os.sep + \
            ('full' if self.model else 'observation') + \
            os.sep + station + '.csv.gz'

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

    def normalize(self) -> 'Daily':
        """
        Normalize the DataFrame
        """

        # Create temporal instance
        temp = copy(self)

        # Create result DataFrame
        result = pd.DataFrame(columns=temp._columns[1:])

        # Go through list of weather stations
        for station in temp.stations:
            # Create data frame
            df = pd.DataFrame(columns=temp._columns[1:])
            # Add time series
            df['time'] = pd.date_range(temp.start, temp.end, freq='1D')
            # Add station ID
            df['station'] = station
            # Add columns
            for column in temp._columns[1:]:
                # Add column to DataFrame
                df[column] = NaN

            result = pd.concat([result, df], axis=0)

        # Set index
        result = result.set_index(['station', 'time'])

        # Merge data
        temp.data = pd.concat([temp.data, result], axis=0).groupby(
            ['station', 'time'], as_index=True).first()

        # None -> NaN
        temp.data = temp.data.fillna(NaN)

        # Return class instance
        return temp

    def interpolate(
        self,
        limit: int = 3
    ) -> 'Daily':
        """
        Interpolate NULL values
        """

        # Create temporal instance
        temp = copy(self)

        # Apply interpolation
        temp.data = temp.data.groupby('station').apply(
            lambda group: group.interpolate(
                method='linear', limit=limit, limit_direction='both', axis=0))

        # Return class instance
        return temp

    def aggregate(
        self,
        freq: str = '1D',
        spatial: bool = False
    ) -> 'Daily':
        """
        Aggregate observations
        """

        # Create temporal instance
        temp = copy(self)

        # Time aggregation
        temp.data = temp.data.groupby(['station', pd.Grouper(
            level='time', freq=freq)]).agg(temp._aggregations)

        # Spatial aggregation
        if spatial:
            temp.data = temp.data.groupby(
                [pd.Grouper(level='time', freq=freq)]).mean()

        # Round
        temp.data = temp.data.round(1)

        # Return class instance
        return temp

    def convert(
        self,
        units: dict
    ) -> 'Daily':
        """
        Convert columns to a different unit
        """

        # Create temporal instance
        temp = copy(self)

        # Change data units
        for parameter, unit in units.items():
            if parameter in temp._columns:
                temp.data[parameter] = temp.data[parameter].apply(unit)

        # Return class instance
        return temp

    def coverage(
        self,
        parameter: str = None
    ) -> float:
        """
        Calculate data coverage (overall or by parameter)
        """

        expect = (self.end - self.start).days + 1

        if parameter is None:
            return len(self.data.index) / expect

        return self.data[parameter].count() / expect

    def count(self) -> int:
        """
        Return number of rows in DataFrame
        """

        return len(self.data.index)

    def fetch(self) -> pd.DataFrame:
        """
        Fetch DataFrame
        """

        # Copy DataFrame
        temp = copy(self.data)

        # Remove station index if it's a single station
        if len(self.stations) == 1 and 'station' in temp.index.names:
            temp = temp.reset_index(level='station', drop=True)

        # Return data frame
        return temp
