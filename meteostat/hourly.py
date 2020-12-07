"""
Hourly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from math import floor, nan
from copy import copy
import pytz
import pandas as pd
from meteostat.core import Core

class Hourly(Core):

    """
    Retrieve hourly weather observations for one or multiple weather stations
    """

    # The cache subdirectory
    cache_subdir = 'hourly'

    # Specify if the library should use chunks or full dumps
    chunked = True

    # The list of weather Stations
    _stations = None

    # The start date
    _start = None

    # The end date
    _end = None

    # The time zone
    _timezone = None

    # The data frame
    _data = pd.DataFrame()

    # Columns
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

    # Data tapes
    _types = {
        'temp': 'float64',
        'dwpt': 'float64',
        'rhum': 'float64',
        'prcp': 'float64',
        'snow': 'float64',
        'wdir': 'float64',
        'wspd': 'float64',
        'wpgt': 'float64',
        'tsun': 'float64',
        'coco': 'float64'
    }

    # Columns for date parsing
    _parse_dates = {'time': [0, 1]}

    # Default aggregation functions
    _aggregations = {
        'temp': 'mean',
        'dwpt': 'mean',
        'rhum': 'mean',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': 'mean',
        'wspd': 'mean',
        'wpgt': 'max',
        'pres': 'mean',
        'tsun': 'sum',
        'coco': 'max'
    }

    def _get_data(self, stations=None):

        if len(stations) > 0:

            paths = []

            for station in stations:
                if self.chunked and self._start and self._end:
                    for year in range(self._start.year, self._end.year + 1):
                        paths.append(
                            'hourly/' + str(year) + '/' + str(station) + '.csv.gz')
                else:
                    paths.append('hourly/' + str(station) + '.csv.gz')

            files = self._load(paths)

            if len(files) > 0:

                for file in files:

                    if os.path.isfile(
                            file['path']) and os.path.getsize(
                            file['path']) > 0:

                        df = pd.read_parquet(file['path'])

                        if self._timezone is not None:
                            df = df.tz_localize(
                                'UTC', level='time').tz_convert(
                                self._timezone, level='time')

                        if self._start and self._end:
                            time = df.index.get_level_values('time')
                            self._data = self._data.append(
                                df.loc[(time >= self._start) & (time <= self._end)])
                        else:
                            self._data = self._data.append(df)

    def __init__(
        self,
        stations,
        start=None,
        end=None,
        timezone=None
    ):

        # Set list of weather stations
        if isinstance(stations, pd.DataFrame):
            self._stations = stations.index
        else:
            if not isinstance(stations, list):
                stations = [stations]

            self._stations = pd.Index(stations)

        # Set time zone and adapt period
        if timezone:
            self._timezone = timezone

            if start and end:
                # Initialize time zone
                timezone = pytz.timezone(self._timezone)
                # Set start date
                self._start = timezone.localize(start, is_dst=None).astimezone(pytz.utc)
                # Set end date
                self._end = timezone.localize(end, is_dst=None).astimezone(pytz.utc)
        else:
            # Set start date
            self._start = start
            # Set end date
            self._end = end

        # Get data
        try:
            self._get_data(self._stations)
        except BaseException as read_error:
            raise Exception('Cannot read hourly data') from read_error

        # Clear cache
        self.clear_cache()

    def normalize(self):

        """
        Normalize the DataFrame
        """

        # Create temporal instance
        temp = copy(self)

        # Create result DataFrame
        result = pd.DataFrame(columns=temp._columns[2:])

        # Go through list of weather stations
        for station in temp._stations:
            # Create data frame
            df = pd.DataFrame(columns=temp._columns[2:])
            # Add time series
            df['time'] = pd.date_range(temp._start, temp._end, freq='1H')
            # Add station ID
            df['station'] = station
            # Add columns
            for column in temp._columns[2:]:
                # Add column to DataFrame
                df[column] = nan

            result = pd.concat([result, df], axis=0)

        # Set index
        result = result.set_index(['station', 'time'])

        # Merge data
        temp._data = pd.concat([temp._data, result], axis=0).groupby(
            ['station', 'time'], as_index=True).first()

        # Return class instance
        return temp

    def interpolate(self, limit=3):

        """
        Interpolate NULL values
        """

        # Create temporal instance
        temp = copy(self)

        # Apply interpolation
        temp._data = temp._data.groupby(
            level='station').apply(
            lambda group: group.interpolate(
                method='linear',
                limit=limit,
                limit_direction='both',
                axis=0))

        # Return class instance
        return temp

    def aggregate(self, freq='1H', spatial=False):

        """
        Aggregate observations
        """

        # Create temporal instance
        temp = copy(self)

        # Time aggregation
        temp._data = temp._data.groupby(['station', pd.Grouper(
            level='time', freq=freq)]).agg(temp._aggregations)

        # Spatial aggregation
        if spatial:
            temp._data = temp._data.groupby(
                [pd.Grouper(key='time', freq=freq)]).mean()

        # Return class instance
        return temp

    def convert(self, units):

        """
        Convert columns to a different unit
        """

        # Create temporal instance
        temp = copy(self)

        # Change data units
        for parameter, unit in units.items():
            if parameter in temp._columns:
                temp._data[parameter] = temp._data[parameter].apply(unit)

        # Return class instance
        return temp

    def coverage(self, parameter=None):

        """
        Calculate data coverage (overall or by parameter)
        """

        expect = floor((self._end - self._start).total_seconds() / 3600) + 1

        if parameter is None:
            return len(self._data.index) / expect

        return self._data[parameter].count() / expect

    def count(self):

        """
        Return number of rows in DataFrame
        """

        return len(self._data.index)

    def fetch(self):

        """
        Fetch DataFrame
        """

        # Copy DataFrame
        temp = copy(self._data)

        # Remove station index if it's a single station
        if len(self._stations) == 1 and 'station' in temp.index.names:
            temp = temp.reset_index(level='station', drop=True)

        # Return data frame
        return temp
