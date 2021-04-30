"""
Interpolate Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from meteostat.core.warn import warn


def interpolate(
    self,
    limit: int = 3
):
    """
    Interpolate NULL values
    """

    if self.count() > 0 and not self._data.isnull().values.all():

        # Create temporal instance
        temp = copy(self)

        # Apply interpolation
        temp._data = temp._data.groupby('station').apply(
            lambda group: group.interpolate(
                method='linear', limit=limit, limit_direction='both', axis=0))

        # Return class instance
        return temp

    # Show warning & return self
    warn('Skipping interpolation on empty DataFrame')
    return self
