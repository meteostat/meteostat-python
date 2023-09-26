from time import perf_counter
import logging
from meteostat import config


class _Logger():
    """
    Log info messages, warnings and errors while keeping track of performance.

    This class is not meant to be consumed directly.
    Please use the class instance "log" instead.
    """
    _logger: logging.Logger | None = None
    _start_time = perf_counter()
    _formatter = logging.Formatter('%(levelname)s:%(message)s')

    def _get_time(self) -> str:
        return str(round(perf_counter() - self._start_time, 5))
    
    def _format_message(self, message: str) -> str:
        return f'{message} ({self._get_time()} s)'
    
    def get_logger(self):
        if not self._logger:
            self._logger = logging.getLogger('meteostat')
            self._logger.setLevel(logging.DEBUG)

            if config.debug:
                file_handler = logging.FileHandler(config.log_file, 'w')
                file_handler.setFormatter(self._formatter)
                self._logger.addHandler(file_handler)

        return self._logger

    def info(self, message: str) -> None:
        self.get_logger().info(self._format_message(message))

    def warning(self, message: str) -> None:
        self.get_logger().warning(self._format_message(message))

    def error(self,message: str) -> None:
        self.get_logger().error(self._format_message(message))

logger = _Logger()