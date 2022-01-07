"""
Core Class - Data Loader

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from urllib.error import HTTPError
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from typing import Callable
import pandas as pd
from meteostat.core.warn import warn


def processing_handler(
    datasets: list,
    load: Callable[[dict], None],
    cores: int,
    threads: int
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
    filtered = list(filter(lambda df: df.index.size > 0, output))

    return pd.concat(filtered) if len(filtered) > 0 else output[0]


def load_handler(
    endpoint: str,
    path: str,
    columns: list,
    types: dict,
    parse_dates: list,
    coerce_dates: bool = False
) -> pd.DataFrame:
    """
    Load a single CSV file into a DataFrame
    """

    try:

        # Read CSV file from Meteostat endpoint
        df = pd.read_csv(
            endpoint + path,
            compression='gzip',
            names=columns,
            dtype=types,
            parse_dates=parse_dates)

        # Force datetime conversion
        if coerce_dates:
            df.iloc[:, parse_dates] = df.iloc[:, parse_dates].apply(
                pd.to_datetime, errors='coerce')

    except (FileNotFoundError, HTTPError):

        # Create empty DataFrane
        df = pd.DataFrame(columns=[*types])

        # Display warning
        warn(f'Cannot load {path} from {endpoint}')

    # Return DataFrame
    return df
