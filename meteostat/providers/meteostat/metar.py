"""
The code is licensed under the MIT license.
"""

from datetime import datetime
import pandas as pd
from meteostat import Parameter
from meteostat.types import Station


ENDPOINT = "https://raw.meteostat.net/metar/{station}.csv.gz"
COLUMNS = [
    'time',
    Parameter.TEMP.value,
    Parameter.RHUM.value,
    Parameter.WDIR.value,
    Parameter.WSPD.value,
    Parameter.PRES.value,
    Parameter.COCO.value
]


#@cache(60 * 60 * 24, "pickle")
def get_df(station_id: str) -> pd.DataFrame:
    """
    Get CSV file from Meteostat and convert to DataFrame
    """
    df = pd.read_csv(
        ENDPOINT.format(station=station_id),
        sep=",",
        header=None,
        parse_dates=[[0, 1]],
        compression='gzip'
    )

    df.columns = COLUMNS

    return df.set_index("time")


def fetch(
    station: Station, _start: datetime, _end: datetime, _parameters: list[Parameter]
):
    return get_df(station["id"])
