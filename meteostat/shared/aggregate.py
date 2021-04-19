"""
Aggregate Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from numpy import NaN
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
        freq = self.freq

    # Time aggregation
    temp.data = temp.data.groupby(['station', pd.Grouper(
        level='time', freq=freq)]).agg(temp._aggregations)

    # Spatial aggregation
    if spatial:
        temp.data = temp.data.groupby(
            [pd.Grouper(level='time', freq=freq)]).mean()

    # Round
    temp.data = temp.data.round(1)

    # Return class instance
    return temp
