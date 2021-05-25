"""
Core Class - Warnings

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import warnings


def _warning_on_one_line(message, category, *args) -> str:  # pylint: disable=unused-argument
    """
    Print warning on a single line
    """
    return '%s: %s\n' % (category.__name__, message)


# Set warning format
warnings.formatwarning = _warning_on_one_line


def warn(message: str) -> None:
    """
    Create a warning
    """
    warnings.warn(message, Warning)
