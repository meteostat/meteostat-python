"""
Get Weather Stations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
import pandas as pd


@property
def stations(self) -> pd.Index:
    """
    Fetch Weather Stations
    """

    # Return index of weather stations
    return copy(self._stations)
