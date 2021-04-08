"""
Stations Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import os
from math import cos, sqrt, radians
from copy import copy
from datetime import datetime, timedelta
from typing import Union
import pandas as pd
from meteostat.core import Core


class Stations(Core):

    """
    Select weather stations from the full list of stations
    """

    # The cache subdirectory
    cache_subdir: str = 'stations'

    # The list of selected weather Stations
    stations = None

    # Raw data columns
    _columns: list = [
        'id',
        'name',
        'country',
        'region',
        'wmo',
        'icao',
        'latitude',
        'longitude',
        'elevation',
        'timezone',
        'hourly_start',
        'hourly_end',
        'daily_start',
        'daily_end'
    ]

    # Processed data columns with types
    _types: dict = {
        'id': 'string',
        'name': 'object',
        'country': 'string',
        'region': 'string',
        'wmo': 'string',
        'icao': 'string',
        'latitude': 'float64',
        'longitude': 'float64',
        'elevation': 'float64',
        'timezone': 'string'
    }

    # Columns for date parsing
    _parse_dates: list = [10, 11, 12, 13]

    def _load(self) -> None:
        """
        Load file from Meteostat
        """

        # File name
        file = 'stations' + os.sep + 'meta' + os.sep + 'lib.csv.gz'

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
                self._parse_dates,
                True)

            # Add index
            df = df.set_index('id')

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Set data
        self.stations = df

    def __init__(self) -> None:

        # Get all weather stations
        self._load()

        # Clear cache
        if self.max_age > 0:
            self.clear_cache()

    def id(
        self,
        organization: str,
        code: str
    ) -> 'Stations':
        """
        Get weather station by identifier
        """

        # Create temporal instance
        temp = copy(self)

        if isinstance(code, str):
            code = [code]

        if organization == 'meteostat':
            temp.stations = temp.stations[temp.stations.index.isin(code)]
        else:
            temp.stations = temp.stations[temp.stations[organization].isin(
                code)]

        # Return self
        return temp

    def nearby(
        self,
        lat: float,
        lon: float,
        radius: int = None
    ) -> 'Stations':
        """
        Sort/filter weather stations by physical distance
        """

        # Create temporal instance
        temp = copy(self)

        # Calculate distance between weather station and geo point
        def distance(station, point) -> float:
            # Earth radius in m
            radius = 6371000

            x = (radians(point[1]) - radians(station['longitude'])) * \
                cos(0.5 * (radians(point[0]) + radians(station['latitude'])))
            y = (radians(point[0]) - radians(station['latitude']))

            return radius * sqrt(x * x + y * y)

        # Get distance for each stationsd
        temp.stations['distance'] = temp.stations.apply(
            lambda station: distance(station, [lat, lon]), axis=1)

        # Filter by radius
        if radius is not None:
            temp.stations = temp.stations[temp.stations['distance'] <= radius]

        # Sort stations by distance
        temp.stations.columns.str.strip()
        temp.stations = temp.stations.sort_values('distance')

        # Return self
        return temp

    def region(
        self,
        country: str,
        state: str = None
    ) -> 'Stations':
        """
        Filter weather stations by country/region code
        """

        # Create temporal instance
        temp = copy(self)

        # Country code
        temp.stations = temp.stations[temp.stations['country'] == country]

        # State code
        if state is not None:
            temp.stations = temp.stations[temp.stations['region'] == state]

        # Return self
        return temp

    def bounds(
        self,
        top_left: tuple,
        bottom_right: tuple
    ) -> 'Stations':
        """
        Filter weather stations by geographical bounds
        """

        # Create temporal instance
        temp = copy(self)

        # Return stations in boundaries
        temp.stations = temp.stations[
            (temp.stations['latitude'] <= top_left[0]) &
            (temp.stations['latitude'] >= bottom_right[0]) &
            (temp.stations['longitude'] <= bottom_right[1]) &
            (temp.stations['longitude'] >= top_left[1])
        ]

        # Return self
        return temp

    def inventory(
        self,
        granularity: str,
        required: Union[bool, datetime, tuple]
    ) -> 'Stations':
        """
        Filter weather stations by inventory data
        """

        # Create temporal instance
        temp = copy(self)

        if required is True:
            # Make sure data exists at all
            temp.stations = temp.stations[
                (pd.isna(temp.stations[granularity + '_start']) == False)
            ]
        elif isinstance(required, tuple):
            # Make sure data exists across period
            temp.stations = temp.stations[
                (pd.isna(temp.stations[granularity + '_start']) == False) &
                (temp.stations[granularity + '_start'] <= required[0]) &
                (
                    temp.stations[granularity + '_end'] +
                    timedelta(seconds=temp.max_age)
                    >= required[1]
                )
            ]
        else:
            # Make sure data exists on a certain day
            temp.stations = temp.stations[
                (pd.isna(temp.stations[granularity + '_start']) == False) &
                (temp.stations[granularity + '_start'] <= required) &
                (
                    temp.stations[granularity + '_end'] +
                    timedelta(seconds=temp.max_age)
                    >= required
                )
            ]

        return temp

    def convert(
        self,
        units: dict
    ) -> 'Stations':
        """
        Convert columns to a different unit
        """

        # Create temporal instance
        temp = copy(self)

        # Change data units
        for parameter, unit in units.items():
            if parameter in temp.stations.columns.values:
                temp.stations[parameter] = temp.stations[parameter].apply(
                    unit)

        # Return class instance
        return temp

    def count(self) -> int:
        """
        Return number of weather stations in current selection
        """

        return len(self.stations.index)

    def fetch(
        self,
        limit: int = None,
        sample: bool = False
    ) -> pd.DataFrame:
        """
        Fetch all weather stations or a (sampled) subset
        """

        # Copy DataFrame
        temp = copy(self.stations)

        # Return limited number of sampled entries
        if sample and limit:
            return temp.sample(limit)

        # Return limited number of entries
        if limit:
            return temp.head(limit)

        # Return all entries
        return temp
