"""
Daily Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from math import nan
from copy import copy
import pandas as pd
from meteostat.core import Core


class Daily(Core):

    """
    Retrieve daily weather observations for one or multiple weather stations
    """

    # The cache subdirectory
    cache_subdir = 'daily'

    # The list of weather Stations
    _stations = None

    # The start date
    _start = None

    # The end date
    _end = None

    # The data frame
    _data = pd.DataFrame()

    # Columns
    _columns = [
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
    _types = {
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
    _parse_dates = {'time': [0]}

    # Default aggregation functions
    _aggregations = {
        'tavg': 'mean',
        'tmin': 'min',
        'tmax': 'max',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': 'mean',
        'wspd': 'mean',
        'wpgt': 'max',
        'pres': 'mean',
        'tsun': 'sum'
    }

    def _get_data(self, stations=None):

        if len(stations) > 0:

            paths = []

            for index in stations:
                paths.append('daily/' + str(index) + '.csv.gz')

            files = self._load(paths)

            if len(files) > 0:

                for file in files:

                    if os.path.isfile(
                            file['path']) and os.path.getsize(
                            file['path']) > 0:

                        df = pd.read_parquet(file['path'])

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
        end=None
    ):

        # Set list of weather stations
        if isinstance(stations, pd.DataFrame):
            self._stations = stations.index
        else:
            if not isinstance(stations, list):
                stations = [stations]

            self._stations = pd.Index(stations)

        # Set start date
        self._start = start

        # Set end date
        self._end = end

        # Get data
        try:
            self._get_data(self._stations)
        except BaseException as read_error:
            raise Exception('Cannot read daily data') from read_error

        # Clear cache
        self.clear_cache()

    def normalize(self):

        """
        Normalize the DataFrame
        """

        # Create temporal instance
        temp = copy(self)

        # Create result DataFrame
        result = pd.DataFrame(columns=temp._columns[1:])

        # Go through list of weather stations
        for station in temp._stations:
            # Create data frame
            df = pd.DataFrame(columns=temp._columns[1:])
            # Add time series
            df['time'] = pd.date_range(temp._start, temp._end, freq='1D')
            # Add station ID
            df['station'] = station
            # Add columns
            for column in temp._columns[1:]:
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
        temp._data = temp._data.groupby('station').apply(
            lambda group: group.interpolate(
                method='linear', limit=limit, limit_direction='both', axis=0))

        # Return class instance
        return temp

    def aggregate(self, freq='1D', spatial=False):

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
                [pd.Grouper(level='time', freq=freq)]).mean()

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

        expect = (self._end - self._start).days + 1

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
