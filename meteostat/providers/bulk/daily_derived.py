from typing import Optional

import numpy as np
import pandas as pd
from meteostat.settings import settings
from meteostat.enumerations import Parameter, Provider
from meteostat.timeseries.hourly import hourly
from meteostat.typing import QueryDict
from meteostat.utils.helpers import aggregate_sources
from meteostat.utils.mutations import reshape_by_source


def daily_mean(group: pd.Series):
    """
    Calculate the daily mean from a series of hourly data
    """
    if group.isna().sum() > 3:
        return np.nan
    return group.interpolate(axis=0).mean()


def daily_min(group: pd.Series):
    """
    Calculate the daily minimum from a series of hourly data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.min()


def daily_max(group: pd.Series):
    """
    Calculate the daily maximum from a series of hourly data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.max()


def daily_sum(group: pd.Series):
    """
    Calculate the daily sum from a series of hourly data
    """
    if group.isna().sum() > 0:
        return np.nan
    return group.sum()


# Available parameters with source column and aggregation method
PARAMETER_AGGS = {
    Parameter.TAVG: (Parameter.TEMP, daily_mean),
    Parameter.TMIN: (Parameter.TEMP, daily_min),
    Parameter.TMAX: (Parameter.TEMP, daily_max),
    Parameter.RHUM: (Parameter.RHUM, daily_mean),
    Parameter.DWPT: (Parameter.DWPT, daily_mean),
    Parameter.PRCP: (Parameter.PRCP, daily_sum),
    Parameter.SNWD: (Parameter.SNWD, daily_max),
    Parameter.WSPD: (Parameter.WSPD, daily_mean),
    Parameter.WPGT: (Parameter.WPGT, daily_max),
    Parameter.PRES: (Parameter.PRES, daily_mean),
    Parameter.TSUN: (Parameter.TSUN, daily_sum),
    Parameter.CLDC: (Parameter.CLDC, daily_mean),
}


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    """
    Fetch hourly weather data from Meteostat's bulk interface and
    aggregate to daily granularity
    """
    # Get all source columns
    source_cols = list(
        dict.fromkeys([PARAMETER_AGGS[p][0] for p in query["parameters"]])
    )
    # Get hourly DataFrame
    ts_hourly = hourly(
        query["station"]["id"],
        query["start"],
        query["end"],
        parameters=source_cols,
        providers=[Provider.BULK_HOURLY],
        timezone=query["station"]["timezone"],
    )
    df_hourly = ts_hourly.fetch(fill=True)
    # If no hourly data is available, exit
    if df_hourly is None:
        return None
    # Create daily aggregations
    df = pd.DataFrame()
    for parameter in query["parameters"]:
        agg = PARAMETER_AGGS[parameter]
        df[parameter] = (
            df_hourly[agg[0]].groupby(pd.Grouper(level="time", freq="1D")).agg(agg[1])
        )
    # Adjust DataFrame and add index
    df = df.round(1)
    df.index = pd.to_datetime(df.index.date)
    df.index.name = "time"
    # Update data sources if desired
    if settings["bulk_load_sources"]:
        df_sources = ts_hourly.sourcemap
        # Add missing columns
        for key, value in PARAMETER_AGGS.items():
            if key in query["parameters"]:
                df_sources[key] = df_sources[value[0]]
        # Remove duplicates
        df_sources = df_sources.groupby(pd.Grouper(level="time", freq="1D")).agg(
            aggregate_sources
        )
        df = reshape_by_source(df, df_sources)
    # Return final DataFrame
    return df
