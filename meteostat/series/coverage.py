"""
Calculate Data Coverage

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""


def coverage(self, parameter: str = None) -> float:
    """
    Calculate data coverage (overall or by parameter)
    """

    if parameter is None:
        return len(self._data.index) / self.expected_rows()

    return round(self._data[parameter].count() / self.expected_rows(), 2)
