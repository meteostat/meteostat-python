"""
Normalize Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from numpy import NaN
import pandas as pd
import pytz
from meteostat.core.warn import warn


def normalize(self):
    """
    Normalize the DataFrame
    """

    if self.count() == 0:
        warn('Pointless normalization of empty DataFrame')

    # Create temporal instance
    temp = copy(self)

    # Create result DataFrame
    result = pd.DataFrame(columns=temp._columns[temp._first_met_col:])

    # Handle tz-aware date ranges
    if hasattr(temp, '_timezone') and temp._timezone is not None:
        timezone = pytz.timezone(temp._timezone)
        start = temp._start.astimezone(timezone)
        end = temp._end.astimezone(timezone)
    else:
        start = temp._start
        end = temp._end

    # Go through list of weather stations
    for station in temp._stations:
        # Create data frame
        df = pd.DataFrame(columns=temp._columns[temp._first_met_col:])
        # Add time series
        df['time'] = pd.date_range(
            start,
            end,
            freq=self._freq,
            tz=temp._timezone if hasattr(temp, '_timezone') else None)
        # Add station ID
        df['station'] = station
        # Add columns
        for column in temp._columns[temp._first_met_col:]:
            # Add column to DataFrame
            df[column] = NaN

        result = pd.concat([result, df], axis=0)

    # Set index
    result = result.set_index(['station', 'time'])

    # Merge data
    temp._data = pd.concat([temp._data, result], axis=0).groupby(
        ['station', 'time'], as_index=True).first()

    # None -> NaN
    temp._data = temp._data.fillna(NaN)

    # Return class instance
    return temp
