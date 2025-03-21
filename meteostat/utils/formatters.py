from typing import Callable
from pandas import Series


def decimals(digits: int) -> Callable[[Series], Series]:
    """
    Round a series to the specified number of fractional digits
    """

    def _func(series: Series) -> Series:
        return series.round(digits)

    return _func
