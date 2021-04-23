"""
Normals Interface Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Union
import pandas as pd
from meteostat.utilities.aggregations import degree_mean
from meteostat.interface.base import Base
from meteostat.interface.point import Point
from meteostat.interface.monthly import Monthly


class Normals(Base):

    """
    Retrieve climate normals for one or multiple weather stations or
    a single geographical point
    """

    # The list of weather Stations
    _stations: pd.Index = None

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    # Default aggregation functions
    aggregations: dict = {
        'tavg': 'mean',
        'tmin': 'mean',
        'tmax': 'mean',
        'prcp': 'mean',
        'snow': 'mean',
        'wdir': degree_mean,
        'wspd': 'mean',
        'wpgt': 'mean',
        'pres': 'mean',
        'tsun': 'mean'
    }

    def __init__(
        self,
        loc: Union[pd.DataFrame, Point, list, str],
        start: datetime = None,
        end: datetime = None,
        model: bool = True
    ) -> None:

        # Get monthly data
        raw = Monthly(loc, start, end, model)

        # Get list of weather stations
        self._stations = raw.stations

        # Get DataFrame
        self._data = raw._data

        # Aggregate
        self._data = self._data.groupby(['station', self._data.index.get_level_values(
            'time').month]).agg(self.aggregations)

    # Import methods
    from meteostat.series.convert import convert
    from meteostat.series.fetch import fetch
