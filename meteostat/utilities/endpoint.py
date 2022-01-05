""" util functions to generate endpoints to the API """
from typing import Union
from datetime import datetime
from meteostat.enumerations.granularity import Granularity

def generate_endpoint_path(
        dt_start: Union[datetime, int],
        dt_end: Union[datetime, int],
        granularity: Granularity,
        station: str,
        model: bool = False,
) -> str:
    """ api endpoint path generation function """

    if granularity == Granularity.NORMALS:
        data_subset = ''
    elif model:
        data_subset = 'obs/'
    elif dt_start.year == dt_end.year and granularity == Granularity.HOURLY:
        data_subset = f"{dt_start.year}/"
    else:
        data_subset = 'full/'

    return f"{granularity.value}/{data_subset}{station}.csv.gz"