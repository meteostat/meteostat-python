from typing import Callable, Optional
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.interpolation.lapserate import apply_lapse_rate
from meteostat.interpolation.nearest import nearest_neighbor
from meteostat.utils.helpers import get_distance


def interpolate(
    ts: TimeSeries,
    point: Point,
    method: Callable[
        [pd.DataFrame, TimeSeries, Point], Optional[pd.DataFrame]
    ] = nearest_neighbor,
    lapse_rate=6.5,
) -> Optional[pd.DataFrame]:
    """
    Interpolate time series data spatially to a specific point.

    Parameters
    ----------
    ts : TimeSeries
        The time series to interpolate.
    point : Point
        The point to interpolate the data for.
    lapse_rate : float, optional
        The lapse rate (temperature gradient) in degrees Celsius per
        1000 meters of elevation gain. Default is 6.5.

    Returns
    -------
    pd.DataFrame or None
        A DataFrame containing the interpolated data for the specified point,
        or None if no data is available.
    """
    # Fetch DataFrame, filling missing values and adding location data
    df = ts.fetch(fill=True, location=True)

    # If no data is returned, return None
    if df is None:
        return None

    # Apply lapse rate if specified and elevation is available
    if lapse_rate and point.elevation:
        df = apply_lapse_rate(df, point.elevation, lapse_rate)

    # Add distance column
    df["distance"] = get_distance(
        point.latitude, point.longitude, df["latitude"], df["longitude"]
    )

    # Interpolate
    df = method(df, ts, point)

    # If no data is returned, return None
    if df is None:
        return None

    # Drop location-related columns & return
    return df.drop(["latitude", "longitude", "elevation", "distance"], axis=1)
