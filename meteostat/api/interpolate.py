from typing import Callable, Optional, Union
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.interpolation.lapserate import apply_lapse_rate
from meteostat.interpolation.nearest import nearest_neighbor
from meteostat.interpolation.idw import idw
from meteostat.interpolation.auto import auto_interpolate
from meteostat.utils.helpers import get_distance

# Mapping of method names to functions
# Note: RFR is loaded dynamically to avoid requiring sklearn as a dependency
METHOD_MAP = {
    "nearest": nearest_neighbor,
    "idw": idw,
    "auto": auto_interpolate,
}


def _get_rfr_interpolate():
    """
    Dynamically import and return the RFR interpolation function.
    This allows sklearn to be an optional dependency.
    """
    from meteostat.interpolation.rfr import rfr_interpolate

    return rfr_interpolate


def interpolate(
    ts: TimeSeries,
    point: Point,
    method: Union[
        str, Callable[[pd.DataFrame, TimeSeries, Point], Optional[pd.DataFrame]]
    ] = "auto",
    lapse_rate: float = 6.5,
) -> Optional[pd.DataFrame]:
    """
    Interpolate time series data spatially to a specific point.

    Parameters
    ----------
    ts : TimeSeries
        The time series to interpolate.
    point : Point
        The point to interpolate the data for.
    method : str or callable, optional
        Interpolation method to use. Can be a string name or a custom function.
        Built-in methods:
        - "auto" (default): Automatically select between nearest and IDW based on
          spatial context. Uses nearest neighbor if closest station is within 5km
          and 50m elevation difference, otherwise uses IDW.
        - "nearest": Use the value from the nearest weather station.
        - "idw": Inverse Distance Weighting - weighted average based on distance.
        - "rfr": Random Forest Regression - machine learning-based interpolation
          using scikit-learn (requires: pip install scikit-learn).
        Custom functions should have signature:
        func(df: pd.DataFrame, ts: TimeSeries, point: Point) -> pd.DataFrame
    lapse_rate : float, optional
        The lapse rate (temperature gradient) in degrees Celsius per
        1000 meters of elevation gain. Default is 6.5.
        Set to 0 or None to disable lapse rate adjustment.

    Returns
    -------
    pd.DataFrame or None
        A DataFrame containing the interpolated data for the specified point,
        or None if no data is available.

    Examples
    --------
    >>> from datetime import datetime
    >>> import meteostat as ms
    >>> point = ms.Point(50.1155, 8.6842, 113)
    >>> stations = ms.stations.nearby(point, limit=5)
    >>> ts = ms.hourly(stations, datetime(2020, 1, 1, 6), datetime(2020, 1, 1, 18))
    >>> df = ms.interpolate(ts, point, method="auto")

    >>> # Using IDW method
    >>> df = ms.interpolate(ts, point, method="idw")

    >>> # Using custom interpolation function
    >>> def custom_method(df, ts, point):
    ...     return df.groupby(pd.Grouper(level="time", freq=ts.freq)).mean()
    >>> df = ms.interpolate(ts, point, method=custom_method)
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

    # Resolve method to a callable
    method_func: Callable[[pd.DataFrame, TimeSeries, Point], Optional[pd.DataFrame]]
    if isinstance(method, str):
        method_lower = method.lower()

        # Handle RFR separately with dynamic import
        if method_lower == "rfr":
            method_func = _get_rfr_interpolate()  # type: ignore[assignment]
        else:
            resolved = METHOD_MAP.get(method_lower)
            if resolved is None:
                valid_methods = list(METHOD_MAP.keys()) + ["rfr"]
                raise ValueError(
                    f"Unknown method '{method}'. "
                    f"Valid methods are: {', '.join(valid_methods)}"
                )
            method_func = resolved  # type: ignore[assignment]
    else:
        method_func = method  # type: ignore[assignment]

    # Interpolate
    result = method_func(df, ts, point)

    # If no data is returned, return None
    if result is None or result.empty:
        return None

    # Drop location-related columns & return
    return result.drop(["latitude", "longitude", "elevation", "distance"], axis=1)
