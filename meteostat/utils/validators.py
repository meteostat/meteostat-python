"""
Validators Module

Provides validator functions for data validation.
"""

from pandas import Series

from meteostat.core.validator import Validator


def minimum(value: int | float) -> Validator:
    """
    Numeric minimum
    """

    def _func(series: Series) -> Series:
        return series >= value

    return Validator(_func)


def maximum(value: int | float) -> Validator:
    """
    Numeric maximum
    """

    def _func(series: Series) -> Series:
        return series <= value

    return Validator(_func)
