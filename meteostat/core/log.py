from os import sep
from functools import cache
from time import perf_counter
import logging
from meteostat.framework import config


class _Logger():
    """
    Log info messages, warnings and errors while keeping track of performance.

    This class is not meant to be consumed directly.
    Please use the class instance "log" instead.
    """
    logger = logging.getLogger('meteostat')
    start_time = perf_counter()
    formatter = logging.Formatter('%(levelname)s:%(message)s')

    def __init__(self) -> None:
        self.logger.setLevel(logging.DEBUG)

        if config().debug:
            file_handler = logging.FileHandler(config().log_file, 'w')
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

    def _get_time(self) -> str:
        return str(round(perf_counter() - self.start_time, 5))
    
    def _format_message(self, message: str) -> str:
        return f'{message} ({self._get_time()} s)'

    def info(self, message: str) -> None:
        self.logger.info(self._format_message(message))

    def warning(self, message: str) -> None:
        self.logger.warning(self._format_message(message))

    def error(self,message: str) -> None:
        self.logger.error(self._format_message(message))

@cache
def logger() -> _Logger:
    return _Logger()