"""
Convert Data Units

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy


def convert(
    self,
    units: dict
):
    """
    Convert columns to a different unit
    """

    # Create temporal instance
    temp = copy(self)

    # Change data units
    for parameter, unit in units.items():
        if parameter in temp._columns:
            temp._data[parameter] = temp._data[parameter].apply(unit)

    # Return class instance
    return temp
