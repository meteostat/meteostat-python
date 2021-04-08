"""
Hourly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from math import floor
from copy import copy
from datetime import datetime
from typing import Union
import pytz
import numpy as np
import pandas as pd
from meteostat.core import Core
from meteostat.point import Point


class Hourly(Core):

    """
    Retrieve hourly weather observations for one or multiple weather stations
    """

    # The cache subdirectory
    cache_subdir = 'hourly'

    # Specify if the library should use chunks or full dumps
    chunked = True

    # The list of weather Stations
    stations = None

    # The start date
    start = None

    # The end date
    end = None

    # The time zone
    timezone = None

    # Include model data?
    model: bool = True

    # The data frame
    data = pd.DataFrame()

    # Raw data columns
    _columns = [
        'date',
        'hour',
        'temp',
        'dwpt',
        'rhum',
        'prcp',
        'snow',
        'wdir',
        'wspd',
        'wpgt',
        'pres',
        'tsun',
        'coco'
    ]

    # Processed data columns with types
    _types = {
        'temp': 'float64',
        'dwpt': 'float64',
        'rhum': 'float64',
        'prcp': 'float64',
        'snow': 'float64',
        'wdir': 'float64',
        'wspd': 'float64',
        'wpgt': 'float64',
        'pres': 'float64',
        'tsun': 'float64',
        'coco': 'float64'
    }

    # Columns for date parsing
    _parse_dates = {
        'time': [0, 1]
    }

    # Default aggregation functions
    _aggregations = {
        'temp': 'mean',
        'dwpt': 'mean',
        'rhum': 'mean',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': Core._degree_mean,
        'wspd': 'mean',
        'wpgt': 'max',
        'pres': 'mean',
        'tsun': 'sum',
        'coco': 'max'
    }

    def _set_time(
        self,
        start: datetime = None,
        end: datetime = None,
        timezone: str = None
    ) -> None:
        """
        Set & adapt the period's time zone
        """

        if timezone:

            # Save timezone
            self.timezone = timezone

            if start and end:

                # Initialize time zone
                timezone = pytz.timezone(self.timezone)

                # Set start date
                self.start = timezone.localize(
                    start, is_dst=None).astimezone(
                    pytz.utc)

                # Set end date
                self.end = timezone.localize(
                    end, is_dst=None).astimezone(
                    pytz.utc)

        else:

            # Set start date
            self.start = start

            # Set end date
            self.end = end

    def _load(
        self,
        station: str,
        year: str = None
    ) -> None:
        """
        Load file from Meteostat
        """

        # File name
        file = 'stations' + os.sep + 'hourly' + os.sep + \
            ('full' if self.model else 'observation') + os.sep + \
            (year + os.sep if year else '') + station + '.csv.gz'

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

        # Localize time column
        if self.timezone is not None and len(df.index) > 0:
            df = df.tz_localize(
                'UTC', level='time').tz_convert(
                self.timezone, level='time')

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

                if self.chunked and self.start and self.end:

                    for year in range(self.start.year, self.end.year + 1):
                        datasets.append((
                            str(station),
                            str(year)
                        ))

                else:

                    datasets.append((
                        str(station),
                        None
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
                pd.Grouper(level='time', freq='1H')).agg('first')

        else:

            # Join score and elevation of involved weather stations
            data = self.data.join(
                stations[['score', 'elevation']], on='station')

            # Adapt temperature-like data based on altitude
            if adapt_temp:
                data.loc[data['temp'] != np.NaN, 'temp'] = data['temp'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))
                data.loc[data['dwpt'] != np.NaN, 'dwpt'] = data['dwpt'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))

            # Exclude non-mean data & perform aggregation
            excluded = data[['wdir', 'coco']]
            excluded = excluded.groupby(
                pd.Grouper(level='time', freq='1H')).agg('first')

            # Aggregate mean data
            data = data.groupby(
                pd.Grouper(level='time', freq='1H')).apply(self._weighted_average)

            # Drop RangeIndex
            data.index = data.index.droplevel(1)

            # Merge excluded fields
            data[['wdir', 'coco']] = excluded

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
        timezone: str = None,
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

        # Set time zone and adapt period
        self._set_time(start, end, timezone)

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

    def normalize(self) -> 'Hourly':
        """
        Normalize the DataFrame
        """

        # Create temporal instance
        temp = copy(self)

        # Create result DataFrame
        result = pd.DataFrame(columns=temp._columns[2:])

        # Go through list of weather stations
        for station in temp.stations:
            # Create data frame
            df = pd.DataFrame(columns=temp._columns[2:])
            # Create date range
            if temp.timezone is not None:
                # Make start and end date timezone-aware
                timezone = pytz.timezone(temp.timezone)
                start = temp.start.astimezone(timezone)
                end = temp.end.astimezone(timezone)
                # Add time series
                df['time'] = pd.date_range(
                    start, end, freq='1H', tz=temp.timezone)
            else:
                df['time'] = pd.date_range(temp.start, temp.end, freq='1H')
            # Add station ID
            df['station'] = station
            # Add columns
            for column in temp._columns[2:]:
                # Add column to DataFrame
                df[column] = np.NaN

            result = pd.concat([result, df], axis=0)

        # Set index
        result = result.set_index(['station', 'time'])

        # Merge data
        temp.data = pd.concat([temp.data, result], axis=0).groupby(
            ['station', 'time'], as_index=True).first()

        # None -> NaN
        temp.data = temp.data.fillna(np.NaN)

        # Return class instance
        return temp

    def interpolate(
        self,
        limit: int = 3
    ) -> 'Hourly':
        """
        Interpolate NULL values
        """

        # Create temporal instance
        temp = copy(self)

        # Apply interpolation
        temp.data = temp.data.groupby(
            level='station').apply(
            lambda group: group.interpolate(
                method='linear',
                limit=limit,
                limit_direction='both',
                axis=0))

        # Return class instance
        return temp

    def aggregate(
        self,
        freq: str = '1H',
        spatial: bool = False
    ) -> 'Hourly':
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
                [pd.Grouper(key='time', freq=freq)]).mean()

        # Round
        temp.data = temp.data.round(1)

        # Return class instance
        return temp

    def convert(
        self,
        units: dict
    ) -> 'Hourly':
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

        expect = floor((self.end - self.start).total_seconds() / 3600) + 1

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
