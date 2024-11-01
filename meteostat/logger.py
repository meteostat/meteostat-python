import logging

logger = logging.getLogger("meteostat")

_console_handler = logging.StreamHandler()

_formatter = logging.Formatter("%(levelname)s - %(filename)s:%(lineno)d - %(message)s")

_console_handler.setFormatter(_formatter)

logger.addHandler(_console_handler)
