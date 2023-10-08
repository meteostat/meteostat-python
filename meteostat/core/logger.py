"""
Log info messages, warnings and errors while keeping track of performance.

This class is not meant to be consumed directly.
Please use the class instance "logger" instead.
"""

from time import perf_counter
import logging
from meteostat import settings
from functools import cache

def info(message: str) -> None:
    _get_logger().info(_format_message(message))

def warning(message: str) -> None:
    _get_logger().warning(_format_message(message))

def error(message: str) -> None:
    _get_logger().error(_format_message(message))

_start_time = perf_counter()
_formatter = logging.Formatter('%(levelname)s:%(message)s')

def _get_time() -> str:
    return str(round(perf_counter() - _start_time, 5))

def _format_message(message: str) -> str:
    return f'{message} ({_get_time()} s)'

@cache
def _get_logger():
    logger = logging.getLogger('meteostat')
    logger.setLevel(logging.DEBUG)

    if settings.debug:
        file_handler = logging.FileHandler(settings.log_file, 'w')
        file_handler.setFormatter(_formatter)
        logger.addHandler(file_handler)

    return logger