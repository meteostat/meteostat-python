"""
Monthly time series data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import List

import numpy as np
import pandas as pd
from meteostat.enumerations import Parameter, Provider, Granularity
from meteostat.schema import NORMALS_SCHEMA
from meteostat.api.monthly import DEFAULT_PARAMETERS, monthly
from meteostat.api.timeseries import TimeSeries
from meteostat.utils.helpers import aggregate_sources
from meteostat.utils.mutations import reshape_by_source
from meteostat.utils.parsers import (
    get_schema,
    parse_year,
)


def normals(
    station: str | List[str] | pd.Index | pd.Series,
    start: int = 1961,
    end: int = 1990,
    parameters: List[Parameter | str] = DEFAULT_PARAMETERS,
    providers: List[Provider | str] = [Provider.MONTHLY],
    max_missing: int = 3,
):
    """
    Retrieve climate normals data
    """

    schema = get_schema(NORMALS_SCHEMA, parameters)

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

    df = ts.fetch()
    sources = ts.sources.fetch()

    df["month"] = df.index.get_level_values("time").month
    sources["month"] = df.index.get_level_values("time").month

    df = df.groupby(["station", "month"]).agg(_mean)
    sources = sources.groupby(["station", "month"]).agg(aggregate_sources)

    df = df.rename_axis(index={"month": "time"})
    sources = sources.rename_axis(index={"month": "time"})

    df = schema.format(df)

    df_fragments = []

    for s in df.index.get_level_values("station").unique():
        fragment = reshape_by_source(df.loc[s], sources.loc[s])
        fragment = pd.concat([fragment], keys=[s], names=["station"])
        df_fragments.append(fragment)

    return TimeSeries(
        granularity=Granularity.NORMALS,
        schema=schema,
        providers=ts.providers,
        stations=ts.stations,
        df=pd.concat(df_fragments),
        start=ts.start,
        end=ts.end,
    )
