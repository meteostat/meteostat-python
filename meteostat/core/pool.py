from typing import Any, Callable, Iterator
from math import floor
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from meteostat import config, framework

def allocate_workers(max_workers: int) -> tuple[int]:
    """
    Get the maximum number of workers for a Pool
    along with the number of remaining workers
    """
    worker_count = min(max_workers, config.max_workers)
    return (worker_count, config.max_workers - worker_count)

class MockFuture:
    _result: Any

    def __init__(self, result) -> None:
        self._result = result

    def result(self) -> Any:
        return self._result

class Pool:
    _executor: ThreadPoolExecutor | None = None

    def __init__(self, max_workers: int) -> None:
        framework.logger.info(f'Creating a Pool with {max_workers} out of {config.max_workers} workers')
        if max_workers > 1:
            self._executor = ThreadPoolExecutor(max_workers)

    def map(self, func: Callable, iterables, timeout=None) -> Iterator[Any]:
        """
        Run a single function with a set of input parameters in parallel.

        Example:

        pool.map(stations.meta, ['10637', '10635', '10729'])
        """
        if self._executor:
            return self._executor.map(func, iterables, timeout=timeout)
        return map(func, iterables)
    
    def submit(self, func: Callable) -> Future:
        if self._executor:
            return self._executor.submit(func)
        return MockFuture(func())
    
    def run(self, *args) -> Iterator[Any]:
        """
        Run multiple functions in parallel.

        Example:

        pool.run(
            lambda: stations.meta('10637'),
            lambda: stations.meta('10635'),
            lambda: stations.meta('10729'),
            lambda: stations.meta('71508'),
            lambda: stations.meta('71624'),
            lambda: stations.meta('71265'),
            lambda: stations.meta('71639')
        )
        """
        if self._executor:
            return [arg.result() for arg in [self._executor.submit(arg) for arg in args]]
        return [arg() for arg in args]
    
    def shutdown(self, wait = True) -> None:
        if self._executor:
            self._executor.shutdown(wait)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb) -> None:
        self.shutdown()

# def create_pool() -> ThreadPoolExecutor | None:
#     if config.max_workers > 1:
#         return ThreadPoolExecutor(config.max_workers)
#     return None


# class PoolManager:
#     _allocated_workers = 0

#     def allocate(n: int) -> int:


# class MockFuture:
#     _result: Any

#     def __init__(self, result: Any) -> None:
#         self._result = result

#     def result(self) -> Any:
#         return self._result


# class Pool:
#     _executor: ThreadPoolExecutor | None = None
#     max_workers: int

#     def __init__(self, max_workers: int) -> None:
#         self.max_workers = max_workers
#         self._executor = ThreadPoolExecutor(self.max_workers)

#     def map(self, func: Callable, *iterables, timeout=None) -> Iterator[Any]:
#         if self._executor:
#             return self._executor.map(func, iterables, timeout=timeout)
#         return map(func, iterables)
    
#     def submit(self, func: Callable, args, kwargs) -> Future | MockFuture:
#         if self._executor:
#             return self._executor.submit(func, args, kwargs)
#         return MockFuture(func(*args, **kwargs))
    
#     def run(self, *args) -> Iterator[Future]:
#         result = []
#         for arg in args:
#             result.append(self.submit(*arg))
#         return as_completed(result)


# def create_pool(max_workers: int, split = 1) -> ThreadPoolExecutor:
#     """
#     Create a new ThreadPoolExecutor which respects the user-defined worker limits
#     """
#     max_workers = max(min(floor(config.max_threads / split), max_workers), 1)
#     framework.logger.info(f'Creating new ThreadPoolExecutor with max_workers={max_workers}')
#     return ThreadPoolExecutor()

# def map_async(pool: ThreadPoolExecutor, func: Callable, args) -> Iterator[Future]:
#     result = []
#     for arg in args:
#         result.append(pool.submit(func, arg))
#     return as_completed(result)

# from typing import Callable, Iterator, Any
# from math
# from concurrent.futures import Future, ThreadPoolExecutor, as_completed
# from meteostat import config

# class _PoolManager:
#     _active_workers = 0

#     @classmethod
#     def reserve(cls, n: int) -> int:
#         count = max(min(config.max_threads - cls._active_workers, n), 1)
#         cls._active_workers += count
#         return count
    
#     @classmethod
#     def free(cls, n: int) -> None:
#         cls._active_workers -= n

# class Pool(ThreadPoolExecutor):

#     def __init__(self, max_workers) -> None:
#         max_workers = _PoolManager.reserve(max_workers)
#         super().__init__(max_workers)
    
#     def shutdown(self) -> None:
#         super().shutdown()
#         _PoolManager.free(self._max_workers)

# class MockFuture:
#     _result: Any = None

#     def result(self) -> Any:
#         return self._result

# class Pool:
#     _executor: ThreadPoolExecutor | None = None

#     def get_executor(self) -> ThreadPoolExecutor:
#         if not self._executor:
#             self._executor = ThreadPoolExecutor(config.max_threads)
#         return self._executor
    
#     def submit(self, func: Callable, args, kwargs) -> Future:
#         try:
#             return self.get_executor().submit(func, args, kwargs)
#         except 
    
#     def map(self, func: Callable, *iterables, timeout=None) -> Iterator[Future]:
#         return self.get_executor().map(func, iterables, timeout=timeout)
    
#     def map_async(self, func, iterables) -> Iterator[Future]:
#         result = []
#         for args in iterables:
#             result.append(self.submit(func, args))
#         return as_completed(result)
    
#     def shutdown(self, wait = True, cancel_futures = False) -> None:
#         self.get_executor().shutdown(wait=wait, cancel_futures=cancel_futures)
#         self._executor = None

# def create_pool(max_workers: int, split = 1) -> ThreadPoolExecutor:
#     """
#     Create a new ThreadPoolExecutor which respects the user-defined worker limits
#     """
#     return ThreadPoolExecutor(max(min(floor(config.max_threads / split), max_workers), 1))

# def map_async(pool: ThreadPoolExecutor, func: Callable, args) -> Iterator[Future]:
#     result = []
#     for arg in args:
#         result.append(pool.submit(func, arg))
#     return as_completed(result)