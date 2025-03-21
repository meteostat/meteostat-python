from typing import Callable
from pandas import Series


def minimum(value: int | float) -> Callable[[Series], Series]:
    """
    Numeric minimum
    """

    def _func(series: Series) -> Series:
        return series >= value

    return _func


def maximum(value: int | float) -> Callable[[Series], Series]:
    """
    Numeric maximum
    """

    def _func(series: Series) -> Series:
        return series <= value

    return _func
