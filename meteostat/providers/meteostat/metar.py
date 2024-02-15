"""
The code is licensed under the MIT license.
"""

from typing import Optional
from urllib.error import HTTPError
import pandas as pd
from meteostat.core.logger import logger
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache


ENDPOINT = "https://raw.meteostat.net/metar/{year}/{station}.csv.gz"


@cache(60 * 60 * 24, "pickle")
def get_df(station_id: str, year: int) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT.format(station=station_id, year=str(year))
    try:
        df = pd.read_csv(file_url, sep=",", compression="gzip")

        time_cols = df.columns[0:4]
        df['time'] = pd.to_datetime(df[time_cols])

        return df.drop(time_cols, axis=1).set_index("time")
    except HTTPError as error:
        logger.warn(
            f"Couldn't load METAR file {file_url} (status: {error.status})"
        )
        return None
    except Exception as error:
        logger.error(error)
        return None


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    years = range(query["start"].year, query["end"].year + 1)
    data = [get_df(query["station"]["id"], year) for year in years]
    return pd.concat(data) if len(data) and not all(d is None for d in data) else None
