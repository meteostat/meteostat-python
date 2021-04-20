"""
Interpolate Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy

def interpolate(
    self,
    limit: int = 3
) -> 'Daily':
    """
    Interpolate NULL values
    """

    # Create temporal instance
    temp = copy(self)

    # Apply interpolation
    temp.data = temp.data.groupby('station').apply(
        lambda group: group.interpolate(
            method='linear', limit=limit, limit_direction='both', axis=0))

    # Return class instance
    return temp
