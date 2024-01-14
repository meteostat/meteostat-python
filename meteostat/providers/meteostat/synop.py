"""
The code is licensed under the MIT license.
"""

from datetime import datetime
from urllib.error import HTTPError
import pandas as pd
from meteostat import Parameter
from meteostat.utils.decorators import cache
from meteostat.core.logger import logger
from meteostat.typing import Station


ENDPOINT = "https://raw.meteostat.net/synop/{year}/{station}.csv.gz"


@cache(60 * 60 * 24, "pickle")
def get_df(station_id: str, year: int) -> pd.DataFrame:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT.format(station=station_id, year=str(year))
    try:
        df = pd.read_csv(file_url, sep=",", parse_dates=[[0, 1]], compression="gzip")

        return df.rename(columns={"date_hour": "time"}).set_index("time")
    except HTTPError as error:
        if error.status == 404:
            logger.info(f"File not found: {file_url}")
        else:
            logger.error(f"Couldn't load {file_url} (status: {error.status})")
        return pd.DataFrame()


def fetch(
    station: Station, start: datetime, end: datetime, _parameters: list[Parameter]
):
    years = range(start.year, end.year + 1)
    data = [get_df(station["id"], year) for year in years]
    return pd.concat(data) if len(data) else pd.DataFrame()
