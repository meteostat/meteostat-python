"""
The code is licensed under the MIT license.
"""

from typing import Optional
from urllib.error import HTTPError
import pandas as pd
from meteostat.core.logger import logger
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache


ENDPOINT = "https://raw.meteostat.net/mosmix/{year}/{station}.csv.gz"


@cache(60 * 60 * 24, "pickle")
def get_df(station_id: str, year: int) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT.format(station=station_id, year=str(year))
    try:
        df = pd.read_csv(file_url, sep=",", parse_dates=[[0, 1]], compression="gzip")

        return df.rename(columns={"date_hour": "time"}).set_index("time")
    except HTTPError as error:
        if error.status == 404:
            logger.info(f"MOSMIX file not found: {file_url}")
        else:
            logger.error(
                f"Couldn't load MOSMIX file {file_url} (status: {error.status})"
            )
        return None
    except Exception as error:
        logger.error(error)
        return None


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    years = range(query["start"].year, query["end"].year + 1)
    data = [get_df(query["station"]["id"], year) for year in years]
    return pd.concat(data) if len(data) and not all(d is None for d in data) else None
