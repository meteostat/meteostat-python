import functools
from urllib.error import HTTPError
from typing import Optional, Callable, TypeVar

from meteostat.core.logger import logger

T = TypeVar("T")


def _get_station_year_info(args: tuple) -> str:
    """
    Get station and year info
    """
    station = args[0] if len(args) > 0 else None
    year = args[1] if len(args) > 1 else None

    info = "no station or year info"

    if station is not None:
        info = f'station "{station}"'
    if year is not None:
        info += f' and year "{year}"'

    return info


def handle_exceptions(func: Callable[..., Optional[T]]) -> Callable[..., Optional[T]]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Optional[T]:
        try:
            return func(*args, **kwargs)
        except HTTPError as error:
            if error.code == 404:
                logger.info(
                    f"Data file for {_get_station_year_info(args)} was not found"
                )
            else:
                logger.warning(
                    f"HTTP error while loading data file for {_get_station_year_info(args)} (status: {error.code})",
                    exc_info=True,
                )
        except Exception:
            logger.warning(
                f"Could not load data file for {_get_station_year_info(args)}",
                exc_info=True,
            )
        return None

    return wrapper
