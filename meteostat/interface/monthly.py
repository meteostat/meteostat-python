"""
Monthly Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Union
import numpy as np
import pandas as pd
from meteostat.core.cache import get_file_path, file_in_cache
from meteostat.core.loader import processing_handler, load_handler
from meteostat.utilities.validations import validate_series
from meteostat.utilities.aggregations import degree_mean, weighted_average
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
    _stations: pd.Index = None

    # The start date
    _start: datetime = None

    # The end date
    _end: datetime = None

    # Include model data?
    _model: bool = True

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    # Default frequency
    _freq: str = '1MS'

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

    # Index of first meteorological column
    _first_met_col = 2

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
    aggregations: dict = {
        'tavg': 'mean',
        'tmin': 'min',
        'tmax': 'max',
        'prcp': 'sum',
        'snow': 'mean',
        'wdir': degree_mean,
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
        file = 'monthly/' + ('full' if self._model else 'obs') + \
            '/' + station + '.csv.gz'

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
                self._parse_dates)

            # Validate Series
            df = validate_series(df, station)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Filter time period and append to DataFrame
        if self._start and self._end:

            # Get time index
            time = df.index.get_level_values('time')

            # Filter & append
            self._data = self._data.append(
                df.loc[(time >= self._start) & (time <= self._end)])

        else:

            # Append
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

            self._data = self._data.groupby(
                pd.Grouper(level='time', freq=self._freq)).agg('first')

        else:

            # Join score and elevation of involved weather stations
            data = self._data.join(
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

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        start: datetime = None,
        end: datetime = None,
        model: bool = True
    ) -> None:

        # Set list of weather stations
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index
        elif isinstance(loc, Point):
            stations = loc.get_stations('hourly', start, end)
            self._stations = stations.index
        else:
            if not isinstance(loc, list):
                loc = [loc]

            self._stations = pd.Index(loc)

        # Set start date
        if start is not None:
            self._start = start.replace(day=1)

        # Set end date
        self._end = end

        # Set model
        self._model = model

        # Get data for all weather stations
        self._get_data()

        # Interpolate data
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Clear cache
        if self.max_age > 0:
            self.clear_cache()

    def expected_rows(self) -> int:
        """
        Return the number of rows expected for the defined date range
        """

        return ((self._end.year - self._start.year) * 12 +
                self._end.month - self._start.month) + 1

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
