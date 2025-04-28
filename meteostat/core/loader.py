"""
Core Class - Data Loader

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from io import BytesIO
from gzip import GzipFile
from urllib.request import Request, ProxyHandler, build_opener
from urllib.error import HTTPError
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from typing import Callable, List, Optional
import pandas as pd
from meteostat.core.warn import warn


def processing_handler(
    datasets: List, load: Callable[[dict], None], cores: int, threads: int
) -> None:
    """
    Load multiple datasets (simultaneously)
    """

    # Data output
    output = []

    # Multi-core processing
    if cores > 1 and len(datasets) > 1:
        # Create process pool
        with Pool(cores) as pool:
            # Process datasets in pool
            output = pool.starmap(load, datasets)

            # Wait for Pool to finish
            pool.close()
            pool.join()

    # Multi-thread processing
    elif threads > 1 and len(datasets) > 1:
        # Create process pool
        with ThreadPool(threads) as pool:
            # Process datasets in pool
            output = pool.starmap(load, datasets)

            # Wait for Pool to finish
            pool.close()
            pool.join()

    # Single-thread processing
    else:
        for dataset in datasets:
            output.append(load(*dataset))

    # Remove empty DataFrames
    filtered = list(filter(lambda df: not df.empty, output))

    return pd.concat(filtered) if len(filtered) > 0 else output[0]


def load_handler(
    endpoint: str,
    path: str,
    proxy: Optional[str] = None,
    names: Optional[List] = None,
    dtype: Optional[dict] = None,
    parse_dates: Optional[List] = None,
    default_df: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Load a single CSV file into a DataFrame
    """

    try:
        handlers = []

        # Set a proxy
        if proxy:
            handlers.append(ProxyHandler({"http": proxy, "https": proxy}))

        # Read CSV file from Meteostat endpoint
        with build_opener(*handlers).open(Request(endpoint + path)) as response:
            # Decompress the content
            with GzipFile(fileobj=BytesIO(response.read()), mode="rb") as file:
                df = pd.read_csv(
                    file,
                    names=names,
                    dtype=dtype,
                    parse_dates=parse_dates,
                )

    except (FileNotFoundError, HTTPError):
        df = default_df if default_df is not None else pd.DataFrame(columns=names)

        # Display warning
        warn(f"Cannot load {path} from {endpoint}")

    # Return DataFrame
    return df
