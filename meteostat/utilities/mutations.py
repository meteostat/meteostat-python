"""
Utilities - DataFrame Mutations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import numpy as np
import pandas as pd


def localize(df: pd.DataFrame, timezone: str) -> pd.DataFrame:
    """
    Convert time data to any time zone
    """

    return df.tz_localize("UTC", level="time").tz_convert(timezone, level="time")


def filter_time(df: pd.DataFrame, start: datetime, end: datetime) -> pd.DataFrame:
    """
    Filter time series data based on start and end date
    """

    # Get time index
    time = df.index.get_level_values("time")

    # Filter & return
    return df.loc[(time >= start) & (time <= end)]


def adjust_temp(df: pd.DataFrame, alt: int):
    """
    Adjust temperature-like data based on altitude
    """

    # Default temperature difference by 100 meters
    temp_diff = 0.6

    # Temperature-like columns
    temp_like = ("temp", "dwpt", "tavg", "tmin", "tmax")

    # Adjust values for all temperature-like data
    for col_name in temp_like:
        if col_name in df.columns:
            df.loc[df[col_name] != np.NaN, col_name] = df[col_name] + (
                temp_diff * ((df["elevation"] - alt) / 100)
            )

    return df
