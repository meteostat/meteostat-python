"""
Useful utilities for validating data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat import Parameter
from meteostat.core.logger import logger


def validate_parameters(supported: list[Parameter], requested: list[Parameter]) -> None:
    """
    Log warning if a requested parameter is not supported
    """
    diff = set(requested).difference(set(supported))
    if len(diff):
        logger.warn(
            f"""Tried to request data for unsupported parameters: {
            ", ".join([p.value for p in diff])
        }"""
        )
