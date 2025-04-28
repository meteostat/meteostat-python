"""
Interpolate Data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
import numpy as np
from meteostat.core.warn import warn


def interpolate(self, limit: int = 3):
    """
    Interpolate NULL values
    """

    if self.count() > 0 and not self._data.isnull().values.all():
        temp = copy(self)

        def _interpolate_numeric(group):
            numeric_cols = group.select_dtypes(include=[np.number])
            interpolated = numeric_cols.interpolate(
                method="linear", limit=limit, limit_direction="both", axis=0
            )
            group[numeric_cols.columns] = interpolated
            return group

        temp._data = temp._data.groupby("station", group_keys=False).apply(_interpolate_numeric)

        return temp

    warn("Skipping interpolation on empty DataFrame")
    return self