"""
Aggregate Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
import pandas as pd


def aggregate(
    self,
    freq: str = None,
    spatial: bool = False
) -> 'Daily':
    """
    Aggregate observations
    """

    # Create temporal instance
    temp = copy(self)

    # Set default frequency if not set
    if freq is None:
        freq = self._freq

    # Time aggregation
    temp._data = temp._data.groupby(['station', pd.Grouper(
        level='time', freq=freq)]).agg(temp.aggregations)

    # Spatial aggregation
    if spatial:
        temp._data = temp._data.groupby(
            [pd.Grouper(level='time', freq=freq)]).mean()

    # Round
    temp._data = temp._data.round(1)

    # Return class instance
    return temp
