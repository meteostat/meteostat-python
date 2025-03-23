"""
Climate Normals

Access climate normals data for one or multiple weather stations.
"""

from typing import List

import numpy as np
import pandas as pd
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.core.schema import schema_service
from meteostat.api.monthly import DEFAULT_PARAMETERS, monthly
from meteostat.api.timeseries import TimeSeries
from meteostat.typing import Station
from meteostat.utils.mutations import reshape_by_source
from meteostat.utils.parsers import parse_year


def normals(
    station: str | Station | List[str | Station] | pd.Index | pd.Series,
    start: int = 1961,
    end: int = 1990,
    parameters: List[Parameter] = DEFAULT_PARAMETERS,
    providers: List[Provider] = [Provider.MONTHLY],
    max_missing: int = 3,
):
    """
    Access climate normals data
    """

    def _mean(group: pd.Series):
        """
        Calculate the monthly mean from multiple years of monthly data
        """
        if group.isna().sum() > max_missing:
            return np.nan
        return group.mean()

    ts = monthly(
        station, parse_year(start), parse_year(end, True), parameters, providers
    )

    df = ts.fetch(sources=True)

    df["month"] = df.index.get_level_values("time").month
    df = df.groupby(["station", "month"]).agg(_mean)
    df = df.rename_axis(index={"month": "time"})

    df = schema_service.format(df, Granularity.NORMALS, parameters)

    df_fragments = []

    for s in df.index.get_level_values("station").unique():
        fragment = reshape_by_source(df)
        fragment = pd.concat([fragment], keys=[s], names=["station"])
        df_fragments.append(fragment)

    return TimeSeries(
        granularity=Granularity.NORMALS,
        stations=ts.stations,
        df=pd.concat(df_fragments),
        start=ts.start,
        end=ts.end,
    )
