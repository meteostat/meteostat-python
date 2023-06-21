from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Iterable, Callable

from meteostat.core.config import config

def pool(*args: Callable | tuple) -> Iterable[Future]:
    """
    Execute multiple operations asynchronously
    """
    with ThreadPoolExecutor(config().get_max_threads(len(args))) as executor:
        return executor.map(lambda func, args = None: func(*args) if args else func(), args)