"""
The code is licensed under the MIT license.
"""

from typing import Optional
from urllib.error import HTTPError
import pandas as pd
from meteostat.settings import settings
from meteostat.logger import logger
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache
from meteostat.utils.mutations import reshape_by_source


ENDPOINT = "https://bulk.meteostat.net/monthly/{station}"
ENDPOINT_DATA = f"{ENDPOINT}.csv.gz"
ENDPOINT_MAP = f"{ENDPOINT}.map.csv.gz"


@cache(60 * 60 * 24 * 30, "pickle")
def get_df(station: str) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT_DATA.format(station=station)

    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")
        time_cols = df.columns[0:2]
        df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01'
        df["time"] = pd.to_datetime(df['date'])
        return df.drop(time_cols, axis=1).drop('date', axis=1).set_index("time")

    except HTTPError as error:
        logger.info(
            f"Couldn't load daily data file {file_url} (status: {error.status})"
        )
        return None

    except Exception as error:
        logger.error(error)
        return None


@cache(60 * 60 * 24 * 30, "pickle")
def get_source_df(station: str) -> Optional[pd.DataFrame]:
    """
    Get source map CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT_MAP.format(station=station)

    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")
        time_cols = df.columns[0:2]
        df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2) + '-01'
        df["time"] = pd.to_datetime(df['date'])
        return df.drop(time_cols, axis=1).drop('date', axis=1).set_index("time")

    except HTTPError as error:
        logger.info(
            f"Couldn't load daily source map file {file_url} (status: {error.status})"
        )
        return None

    except Exception as error:
        logger.error(error)
        return None


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch daily weather data from Meteostat's bulk interface
    """
    # Concatenate into a single DataFrame
    df = get_df(query["station"]["id"])
    # Update data sources if desired
    if settings["bulk_load_sources"]:
        df_sources = get_source_df(query["station"]["id"])
        df = reshape_by_source(df, df_sources)
    return df
