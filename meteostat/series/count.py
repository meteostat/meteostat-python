"""
Get Number Of Rows

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""


def count(self) -> int:
    """
    Return number of rows in DataFrame
    """

    return len(self._data.index)
