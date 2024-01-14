"""
DataFrame mutations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import numpy as np
import pandas as pd
from meteostat.core.providers import get_provider
from meteostat.enumerations import Parameter, Priority


def _get_provider_prio(id: str) -> Priority:
    provider = get_provider(id)
    return provider["priority"] if provider else Priority.LOWEST


def squash_df(df: pd.DataFrame) -> pd.DataFrame:
    df["source_prio"] = df.index.get_level_values("source").map(_get_provider_prio)

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


def apply_lapse_rate(
    df: pd.DataFrame,
    target_elevation: int,
    columns: list[Parameter] = [
        Parameter.TEMP,
        Parameter.DWPT,
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
    ],
) -> pd.DataFrame:
    """
    Calculate approximate temperature at target elevation
    """
    # Standard lapse rate in degrees Celsius per meter
    LAPSE_RATE = 0.0065

    for col in columns:
        if col in df.columns:
            df.loc[df[col] != np.NaN, col] = round(
                df[col] + (LAPSE_RATE * (df["elevation"] - target_elevation)), 1
            )

    return df
