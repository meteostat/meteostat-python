from functools import wraps
from typing import Callable, Any
from meteostat import settings
from meteostat.core.cache import from_func, purge
from meteostat.core.logger import logger


def cache(ttl: int | Callable[[Any], int] = 60 * 60 * 24, format: str = "json"):
    """
    A simple decorator which caches a function's return value
    based on its payload.

    All data is persisted in either JSON or Pickle.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if settings.cache_purge:
                purge()
            if not settings.cache_enable:
                logger.info(
                    f"Ommitting cache for {func.__name__} from module {func.__module__} with args={args} and kwargs={kwargs}"
                )
                return func(*args, **kwargs)
            return from_func(
                func,
                args,
                kwargs,
                ttl if isinstance(ttl, int) else ttl(args, kwargs),
                format,
            )

        return wrapper

    return decorator


def purge_cache(max_age: int | None = None) -> None:
    """
    Remove stale files from disk cache
    """
    purge(max_age)
