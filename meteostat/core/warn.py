"""
Core Class - Warnings

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import warnings


def _format(message, category, _filename, _lineno, _line=None) -> str:
    """
    Print warning on a single line
    """

    return f"{category.__name__}: {message}\n"


# Set warning format
warnings.formatwarning = _format


def warn(message: str) -> None:
    """
    Create a warning
    """

    try:
        warnings.warn(message, Warning)
    except TypeError:
        pass
