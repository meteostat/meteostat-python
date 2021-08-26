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
from meteostat.core.warn import warn
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

    # The first year of the period
    _start: int = None

    # The last year of the period
    _end: int = None

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
        if df.index.size > 0 and self._end:

            # Get time index
            end = df.index.get_level_values('end')

            # Filter & return
            return df.loc[end == self._end]

        return df

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
            return processing_handler(
                datasets, self._load, self.processes, self.threads)

        # Empty DataFrame
        return pd.DataFrame(columns=[*self._types])

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
        self._data = self._data.reorder_levels(
            ['station', 'start', 'end', 'month'])
        self._stations = pd.Index(['XXXXX'])

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        start: int = None,
        end: int = None
    ) -> None:

        # Set list of weather stations
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index

        elif isinstance(loc, Point):
            if start and end:
                stations = loc.get_stations(
                    'monthly', datetime(
                        start, 1, 1), datetime(
                        end, 12, 31))
            else:
                stations = loc.get_stations()

            self._stations = stations.index

        else:
            if not isinstance(loc, list):
                loc = [loc]

            self._stations = pd.Index(loc)

        # Check period
        if (start and end) and (end - start != 29 or end %
                                10 != 0 or end >= datetime.now().year):
            raise ValueError('Invalid reference period')

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
            warn('Pointless normalization of empty DataFrame')

        # Go through list of weather stations
        for station in temp._stations:
            # The list of periods
            periods: pd.Index = pd.Index([])
            # Get periods
            if self.count() > 0:
                periods = temp._data[temp._data.index.get_level_values(
                    'station') == station].index.unique('end')
            elif periods.size == 0 and self._end:
                periods = pd.Index([self._end])
            # Go through all periods
            for period in periods:
                # Create DataFrame
                df = pd.DataFrame(
                    columns=temp._columns[temp._first_met_col:])
                # Populate index columns
                df['month'] = range(1, 13)
                df['station'] = station
                df['start'] = period - 29
                df['end'] = period
                # Set index
                df.set_index(
                    ['station', 'start', 'end', 'month'], inplace=True)
                # Merge data
                temp._data = pd.concat([temp._data, df], axis=0).groupby(
                    [
                        'station',
                        'start',
                        'end',
                        'month'
                    ], as_index=True).first() if temp._data.index.size > 0 else df

        # None -> NaN
        temp._data = temp._data.fillna(np.NaN)

        # Return class instance
        return temp

    def fetch(self) -> pd.DataFrame:
        """
        Fetch DataFrame
        """

        # Copy DataFrame
        temp = copy(self._data)

        # Add avg. temperature column
        temp.insert(0, 'tavg', temp[['tmin', 'tmax']].dropna(how='any').mean(
            axis=1).round(1))

        # Remove station index if it's a single station
        if len(self._stations) == 1 and 'station' in temp.index.names:
            temp = temp.reset_index(level='station', drop=True)

        # Remove start & end year if period is set
        if self._start and self._end and self.count() > 0:
            temp = temp.reset_index(level='start', drop=True)
            temp = temp.reset_index(level='end', drop=True)

        # Return data frame
        return temp

    # Import methods
    from meteostat.series.convert import convert
    from meteostat.series.count import count
    from meteostat.core.cache import clear_cache
