"""
The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Optional
from urllib.error import HTTPError
import pandas as pd
from meteostat.enumerations import TTL
from meteostat.utils.decorators import cache
from meteostat.logger import logger
from meteostat.typing import QueryDict


ENDPOINT = "https://raw.meteostat.net/synop/{year}/{station}.csv.gz"


def get_ttl(_station: str, year: int) -> int:
    """
    Get TTL based on year

    Current + previous year = one day
    Else = 30 days
    """
    current_year = datetime.now().year
    return TTL.DAY if current_year - year < 2 else TTL.MONTH


@cache(get_ttl, "pickle")
def get_df(station: str, year: int) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT.format(station=station, year=str(year))

    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")
        time_cols = df.columns[0:4]
        df["time"] = pd.to_datetime(df[time_cols])
        return df.drop(time_cols, axis=1).set_index("time")

    except HTTPError as error:
        logger.info(f"Couldn't load SYNOP file {file_url} (status: {error.status})")
        return None

    except Exception as error:
        logger.warning(error)
        return None


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    years = range(query["start"].year, query["end"].year + 1)
    data = [get_df(query["station"]["id"], year) for year in years]
    return pd.concat(data) if len(data) and not all(d is None for d in data) else None
