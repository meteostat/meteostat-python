"""
Normals Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from typing import Union
from datetime import datetime
import numpy as np
import pandas as pd
from meteostat.core.cache import get_file_path, file_in_cache
from meteostat.core.loader import processing_handler, load_handler
from meteostat.utilities.aggregations import weighted_average
from meteostat.interface.base import Base
from meteostat.interface.point import Point


class Normals(Base):

    """
    Retrieve climate normals for one or multiple weather stations or
    a single geographical point
    """

    # The cache subdirectory
    cache_subdir: str = 'normals'

    # The list of weather Stations
    _stations: pd.Index = None

    # The period
    _period: Union[int, str] = 'auto'

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    # Columns
    _columns: list = [
        'start',
        'end',
        'month',
        'tmin',
        'tmax',
        'prcp',
        'wspd',
        'pres',
        'tsun'
    ]

    # Index of first meteorological column
    _first_met_col = 3

    # Data types
    _types: dict = {
        'tmin': 'float64',
        'tmax': 'float64',
        'prcp': 'float64',
        'wspd': 'float64',
        'pres': 'float64',
        'tsun': 'float64'
    }

    def _load(
        self,
        station: str
    ) -> None:
        """
        Load file from Meteostat
        """

        # File name
        file = f'normals/{station}.csv.gz'

        # Get local file path
        path = get_file_path(self.cache_dir, self.cache_subdir, file)

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
                None)

            if df.index.size > 0:

                # Add weather station ID
                df['station'] = station

                # Set index
                df = df.set_index(['station', 'start', 'end', 'month'])

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Filter time period and append to DataFrame
        if df.index.size > 0 and self._period not in ['auto', 'all']:

            # Get time index
            end = df.index.get_level_values('end')

            # Filter & append
            self._data = self._data.append(
                df.loc[end == self._period])

        else:

            # Append
            if self._data.index.size == 0:
                self._data = df
            else:
                self._data = self._data.append(df)

    def _get_data(self) -> None:
        """
        Get all required data
        """

        if len(self._stations) > 0:

            # List of datasets
            datasets = []

            for station in self._stations:
                datasets.append((
                    str(station),
                ))

            # Data Processing
            processing_handler(datasets, self._load, self.max_threads)

        else:

            # Empty DataFrame
            self._data = pd.DataFrame(columns=[*self._types])

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

            self._data = self._data.groupby(level=[
                'start',
                'end',
                'month'
            ]).agg('first')

        else:

            data = self._data.join(
                stations[['score', 'elevation']], on='station')

            # Adapt temperature-like data based on altitude
            if adapt_temp:
                data.loc[data['tmin'] != np.NaN, 'tmin'] = data['tmin'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))
                data.loc[data['tmax'] != np.NaN, 'tmax'] = data['tmax'] + \
                    ((2 / 3) * ((data['elevation'] - alt) / 100))

            # Aggregate mean data
            data = data.groupby(level=[
                'start',
                'end',
                'month'
            ]).apply(weighted_average)

            # Remove obsolete index column
            try:
                data = data.reset_index(level=3, drop=True)
            except IndexError:
                pass

            # Drop score and elevation
            self._data = data.drop(['score', 'elevation'], axis=1).round(1)

        # Set placeholder station ID
        self._data['station'] = 'XXXXX'
        self._data = self._data.set_index('station', append=True)
        self._stations = pd.Index(['XXXXX'])

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        period: Union[tuple, str] = 'auto'
    ) -> None:

        # Set list of weather stations
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index

        elif isinstance(loc, Point):
            if isinstance(period, tuple):
                start = datetime(period[0], 1, 1)
                end = datetime(period[1], 12, 31)
                stations = loc.get_stations('monthly', start, end)
            else:
                stations = loc.get_stations()

            self._stations = stations.index

        else:
            if not isinstance(loc, list):
                loc = [loc]

            self._stations = pd.Index(loc)

        # The reference period
        self._period = period[1] if isinstance(period, tuple) else period

        # Get data for all weather stations
        self._get_data()

        # Interpolate data
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Aggregate if period is auto
        if self._period == 'auto':
            self._data = self._data.groupby(
                level=['station', 'month']).agg('last')

        # Clear cache
        if self.max_age > 0:
            self.clear_cache()

    def fetch(self) -> pd.DataFrame:
        """
        Fetch DataFrame
        """

        # Copy DataFrame
        temp = copy(self._data)

        # Add avg. temperature column
        temp.insert(0, 'tavg', temp[['tmin', 'tmax']].mean(
            axis=1).round(1))

        # Remove station index if it's a single station
        if len(self._stations) == 1 and 'station' in temp.index.names:
            temp = temp.reset_index(level='station', drop=True)

        # Remove start & end year if period is set
        if isinstance(self._period, int) and 'start' in temp.index.names:
            temp = temp.reset_index(level='start', drop=True)
            temp = temp.reset_index(level='end', drop=True)

        # Return data frame
        return temp

    # Import methods
    from meteostat.series.convert import convert
    from meteostat.series.count import count
    from meteostat.core.cache import clear_cache
