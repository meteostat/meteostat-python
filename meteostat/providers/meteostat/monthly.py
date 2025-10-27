"""
The code is licensed under the MIT license.
"""

from typing import Optional
import pandas as pd
from meteostat.core.config import config
from meteostat.enumerations import TTL
from meteostat.providers.meteostat.shared import handle_exceptions
from meteostat.typing import Query
from meteostat.core.cache import cache_service
from meteostat.utils.mutations import reshape_by_source

ENDPOINT = config.meteostat_monthly_endpoint


@cache_service.cache(TTL.MONTH, "pickle")
@handle_exceptions
def get_df(station: str) -> Optional[pd.DataFrame]:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    file_url = ENDPOINT.format(station=station)

    df = pd.read_csv(file_url, sep=",", compression="gzip")

    time_cols = df.columns[0:2]
    df["date"] = (
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
    )
    df["time"] = pd.to_datetime(df["date"])
    df = df.drop(time_cols, axis=1).drop("date", axis=1).set_index("time")

    return reshape_by_source(df)


def fetch(query: Query) -> Optional[pd.DataFrame]:
    """
    Fetch monthly weather data from Meteostat's central data repository
    """
    df = get_df(query.station.id)
    return df
