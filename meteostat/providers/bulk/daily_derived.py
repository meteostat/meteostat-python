from typing import Optional

import pandas as pd
from meteostat.settings import settings
from meteostat.enumerations import Parameter, Provider
from meteostat.timeseries.hourly import hourly
from meteostat.typing import QueryDict
from meteostat.utils.mutations import reshape_by_source


# Available parameters with source column and aggregation method
PARAMETER_AGGS = {
    Parameter.TAVG: (Parameter.TEMP, "mean"),
    Parameter.TMIN: (Parameter.TEMP, "min"),
    Parameter.TMAX: (Parameter.TEMP, "max"),
    Parameter.RHUM: (Parameter.TEMP, "mean"),
    Parameter.DWPT: (Parameter.DWPT, "mean"),
    Parameter.PRCP: (Parameter.PRCP, "sum"),
    Parameter.SNWD: (Parameter.SNWD, "max"),
    Parameter.WSPD: (Parameter.WSPD, "mean"),
    Parameter.WPGT: (Parameter.WPGT, "max"),
    Parameter.PRES: (Parameter.PRES, "mean"),
    Parameter.TSUN: (Parameter.TSUN, "sum"),
    Parameter.CLDC: (Parameter.CLDC, "mean"),
    Parameter.VSBY: (Parameter.VSBY, "mean"),
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
    df_hourly = ts_hourly.fetch()
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
    df.index = df.index.date
    df["station"] = query["station"]["id"]
    df.index.name = "time"
    # Update data sources if desired
    if settings.bulk_load_sources:
        df_sources = ts_hourly.sourcemap
        # Add missing columns
        for key, value in PARAMETER_AGGS.items():
            if key in query["parameters"]:
                df_sources[key] = df_sources[value[0]]
        # Remove duplicates
        df_sources = df_sources.groupby(pd.Grouper(level="time", freq="1D")).agg(
            lambda x: "|".join(set(x))
        )
        df = reshape_by_source(df, df_sources)
    # Return final DataFrame
    return df
