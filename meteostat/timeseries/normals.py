"""
Monthly time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import List

import pandas as pd
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.model import PARAMETER_DECIMALS
from meteostat.timeseries.monthly import DEFAULT_PARAMETERS, monthly
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.utils.parsers import (
    parse_year,
)



def normals(
    station: str | List[str] | pd.Index | pd.Series,
    start: int = 1961,
    end: int = 1990,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = [Provider.BULK_MONTHLY],
):
    """
    Retrieve climate normals data
    """
    ts = monthly(
        station,
        parse_year(start),
        parse_year(end, True),
        parameters,
        providers
    )

    df = ts.fetch()

    df['month'] = df.index.get_level_values('time').month
    df = df.groupby(['station', 'month']).mean()

    for col in df.columns:
        if col in PARAMETER_DECIMALS:
            df[col] = df[col].round(PARAMETER_DECIMALS[col])

    return TimeSeries(
        Granularity.NORMALS,
        ts.providers,
        ts.stations,
        df,
        ts.start,
        ts.end,
    )
