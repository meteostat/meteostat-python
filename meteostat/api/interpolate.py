from typing import List, Optional
import numpy as np
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.enumerations import Parameter
from meteostat.utils.helpers import get_distance


def apply_lapse_rate(
    df: pd.DataFrame,
    elevation: int,
    lapse_rate: float = 6.5,
    columns: List[Parameter] = [
        Parameter.TEMP,
        Parameter.DWPT,
        Parameter.TMIN,
        Parameter.TMAX,
    ],
) -> pd.DataFrame:
    """
    Calculate approximate temperature at target elevation
    """
    for col in columns:
        if col in df.columns:
            df.loc[df[col] != np.NaN, col] = round(
                df[col] + ((lapse_rate / 1000) * (df["elevation"] - elevation)), 1
            )

    return df


def nearest_neighbor(df: pd.DataFrame, freq: str, point: Point) -> pd.DataFrame:
    """
    Get nearest neighbor value for each record
    """
    df = (
        df.sort_values("distance")
        .groupby(pd.Grouper(level="time", freq=freq))
        .agg("first")
    )

    return df


def interpolate(ts: TimeSeries, point: Point, lapse_rate=6.5) -> Optional[pd.DataFrame]:
    """ """
    df = ts.fetch(fill=True, location=True)

    if df is None:
        return None

    if lapse_rate and point.elevation:
        df = apply_lapse_rate(df, point.elevation, lapse_rate)

    # Add distance column
    df["distance"] = get_distance(
        point.latitude, point.longitude, df["latitude"], df["longitude"]
    )

    # Interpolate
    df = nearest_neighbor(df, ts.freq, point)

    # Drop location-related columns & return
    return df.drop(["latitude", "longitude", "elevation", "distance"], axis=1)
