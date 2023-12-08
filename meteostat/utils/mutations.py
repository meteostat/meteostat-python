from datetime import datetime
from typing import Union
import pandas as pd
from meteostat.core.providers import get_provider
from meteostat.enumerations import Parameter


def filter_time(
    df: pd.DataFrame,
    start: Union[datetime, None] = None,
    end: Union[datetime, None] = None,
) -> pd.DataFrame:
    """
    Filter time series data based on start and end date
    """

    # Get time index
    time = df.index.get_level_values("time")

    # Filter & return
    return df.loc[(time >= start) & (time <= end)] if start and end else df


def filter_parameters(df: pd.DataFrame, parameters: list[Parameter]) -> pd.DataFrame:
    parameters = [parameter.value for parameter in parameters]
    # Remove obsolete columns
    [
        df.drop(col, axis=1, inplace=True) if col not in parameters else None
        for col in df.columns
    ]
    # Add missing columns
    for col in parameters:
        if col not in df:
            df[col] = None
    return df


def squash_df(df: pd.DataFrame) -> pd.DataFrame:
    df["source_prio"] = df.index.get_level_values("source").map(
        lambda s: get_provider(s)["priority"].value
    )

    return (
        df.sort_values(by="source_prio", ascending=False)
        .groupby(["station", "time"])
        .first()
        .drop("source_prio", axis=1)
    )


def fill_df(
    df: pd.DataFrame, start: datetime, end: datetime, freq: str
) -> pd.DataFrame:
    try:
        iterables = [
            df.index.get_level_values("station").unique(),
            pd.date_range(start=start, end=end, freq=freq),
        ]
        names = ["station", "time"]
        if "source" in df.index.names:
            iterables.append(df.index.get_level_values("source").unique())
            names.append("source")
        # Create a new MultiIndex with every hour for each station
        new_index = pd.MultiIndex.from_product(iterables, names=names)

        # Reindex the DataFrame to add missing rows
        df = df.reindex(index=new_index)
        return df
    except KeyError:
        return df


def localize(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
    """
    Convert time data to any time zone
    """

    return df.tz_localize("UTC", level="time").tz_convert(timezone, level="time")
