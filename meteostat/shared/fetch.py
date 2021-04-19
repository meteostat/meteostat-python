"""
Fetch Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
import pandas as pd

def fetch(self) -> pd.DataFrame:
    """
    Fetch DataFrame
    """

    # Copy DataFrame
    temp = copy(self.data)

    # Remove station index if it's a single station
    if len(self.stations) == 1 and 'station' in temp.index.names:
        temp = temp.reset_index(level='station', drop=True)

    # Return data frame
    return temp
