"""
The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Optional
from urllib.error import HTTPError
import pandas as pd
from meteostat.settings import settings
from meteostat.logger import logger
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache
from meteostat.utils.mutations import reshape_by_source


ENDPOINT = "https://data.meteostat.net/daily/{year}/{station}"
ENDPOINT_DATA = f"{ENDPOINT}.csv.gz"
ENDPOINT_MAP = f"{ENDPOINT}.map.csv.gz"


def get_ttl(_station: str, year: int) -> int:
    """
    Get TTL based on year

    Current + previous year = one day
    Else = 30 days
    """
    current_year = datetime.now().year
    return 60 * 60 * 24 if current_year - year < 2 else 60 * 60 * 24 * 30


@cache(get_ttl, "pickle")
def get_df(station: str, year: int) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT_DATA.format(station=station, year=str(year))

    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")
        time_cols = df.columns[0:3]
        df["time"] = pd.to_datetime(df[time_cols])
        return df.drop(time_cols, axis=1).set_index("time")

    except HTTPError as error:
        logger.info(
            f"Couldn't load daily data file {file_url} (status: {error.status})"
        )
        return None

    except Exception as error:
        logger.warning(error)
        return None


@cache(get_ttl, "pickle")
def get_source_df(station: str, year: int) -> Optional[pd.DataFrame]:
    """
    Get source map CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT_MAP.format(station=station, year=str(year))

    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")
        time_cols = df.columns[0:3]
        df["time"] = pd.to_datetime(df[time_cols])
        return df.drop(time_cols, axis=1).set_index("time")

    except HTTPError as error:
        logger.info(
            f"Couldn't load daily source map file {file_url} (status: {error.status})"
        )
        return None

    except Exception as error:
        logger.warning(error)
        return None


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch daily weather data from Meteostat's central data repository
    """
    # Get a list of relevant years
    years = range(query["start"].year, query["end"].year + 1)
    # Get list of annual DataFrames
    df_yearly = [get_df(query["station"]["id"], year) for year in years]
    # Concatenate into a single DataFrame
    df = (
        pd.concat(df_yearly)
        if len(df_yearly) and not all(d is None for d in df_yearly)
        else None
    )
    # Update data sources if desired
    if settings["load_sources"]:
        df_sources_yearly = [
            get_source_df(query["station"]["id"], year) for year in years
        ]
        df_sources = (
            pd.concat(df_sources_yearly)
            if len(df_sources_yearly) and not all(d is None for d in df_sources_yearly)
            else None
        )
        df = reshape_by_source(df, df_sources)
    return df
