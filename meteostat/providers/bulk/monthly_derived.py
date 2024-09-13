from typing import Optional

import numpy as np
import pandas as pd
from meteostat.settings import settings
from meteostat.enumerations import Parameter, Provider
from meteostat.timeseries.daily import daily
from meteostat.typing import QueryDict
from meteostat.utils.helpers import aggregate_sources
from meteostat.utils.mutations import reshape_by_source
from meteostat.utils.parsers import parse_month


def monthly_mean(group: pd.Series):
    """
    Calculate the monthly mean from a series of daily data
    """
    if group.isna().sum() > 3:
        return np.nan
    return group.interpolate(axis=0).mean()


def monthly_sum(group: pd.Series):
    """
    Calculate the monthly sum from a series of daily data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.sum()


def monthly_min(group: pd.Series):
    """
    Calculate the absolute minimum from a series of daily data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.interpolate(axis=0).min()


def monthly_max(group: pd.Series):
    """
    Calculate the absolute maximum from a series of daily data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.interpolate(axis=0).max()


# Available parameters with source column and aggregation method
PARAMETER_AGGS = {
    Parameter.TAVG: monthly_mean,
    Parameter.TAMN: monthly_min,
    Parameter.TAMX: monthly_max,
    Parameter.TMIN: monthly_mean,
    Parameter.TMAX: monthly_mean,
    Parameter.PRCP: monthly_sum,
    Parameter.PRES: monthly_mean,
    Parameter.TSUN: monthly_sum,
}


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch daily weather data from Meteostat's bulk interface and
    aggregate to monthly granularity
    """
    # Get daily DataFrame
    ts_daily = daily(
        query["station"]["id"],
        parse_month(query["start"]),
        parse_month(query["end"], is_end=True),
        parameters=query["parameters"],
        providers=[Provider.BULK_DAILY],
    )
    df_daily = ts_daily.fetch(fill=True)
    # If no daily data is available, exit
    if df_daily is None:
        return None
    # Create monthly aggregations
    df = pd.DataFrame()
    for parameter in query["parameters"]:
        agg = PARAMETER_AGGS[parameter]
        df[parameter] = (
            df_daily[parameter].groupby(pd.Grouper(level="time", freq="MS")).agg(agg)
        )
    # Adjust DataFrame and add index
    df = df.round(1)
    df.index = pd.to_datetime(df.index.date)
    df.index.name = "time"
    # Update data sources if desired
    if settings["bulk_load_sources"]:
        df_sources = ts_daily.sourcemap
        # Remove duplicates
        df_sources = df_sources.groupby(pd.Grouper(level="time", freq="MS")).agg(
            aggregate_sources
        )
        df = reshape_by_source(df, df_sources)
    # Return final DataFrame
    return df
