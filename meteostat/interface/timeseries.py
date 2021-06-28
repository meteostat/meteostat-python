"""
Timeseries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import pandas as pd
from meteostat.interface.base import Base


class Timeseries(Base):

    """
    Timeseries class which provides features which are used across all time series classes
    """

    # The list of weather Stations
    _stations: pd.Index = None

    # The list of origin weather Stations
    _origin_stations: pd.Index = None

    # The start date
    _start: datetime = None

    # The end date
    _end: datetime = None

    # Include model data?
    _model: bool = True

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

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
