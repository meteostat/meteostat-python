from typing import List, Literal, Optional, Union
import numpy as np
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.enumerations import Parameter
from meteostat.interpolation.lapserate import apply_lapse_rate
from meteostat.interpolation.nearest import nearest_neighbor
from meteostat.interpolation.idw import inverse_distance_weighting
from meteostat.utils.helpers import get_distance


def interpolate(
    ts: TimeSeries,
    point: Point,
    distance_threshold: int = 5000,
    elevation_threshold: int = 50,
    elevation_weight: float = 0.1,
    power: float = 2.0,
    lapse_rate: Union[Literal["dynamic"], Literal["static"], None] = "dynamic",
    lapse_rate_threshold: int = 50,
    lapse_rate_parameters: Optional[List[Parameter]] = None,
) -> Optional[pd.DataFrame]:
    """
    Interpolate time series data spatially to a specific point.

    Parameters
    ----------
    ts : TimeSeries
        The time series to interpolate.
    point : Point
        The point to interpolate the data for.
    distance_threshold : int, optional
        Maximum distance (in meters) to use nearest neighbor (default: 5000).
        Beyond this, IDW is used.
    elevation_threshold : int, optional
        Maximum elevation difference (in meters) to use nearest neighbor (default: 50).
        Beyond this, IDW is used even if distance is within threshold.
    elevation_weight : float, optional
        Weight for elevation difference in distance calculation (default: 0.1).
        The effective distance is calculated as:
        sqrt(horizontal_distance^2 + (elevation_diff * elevation_weight)^2)
    power : float, optional
        Power parameter for IDW (default: 2.0). Higher values give more
        weight to closer stations.
    lapse_rate : {'dynamic', 'static', None}, optional
        Apply lapse rate correction based on elevation difference (default: 'dynamic').
        - 'dynamic': Uses actual data to determine lapse rates for a variety of parameters.
        - 'static': Uses a fixed lapse rate of 6.5°C per 1000m (only temperature).
        - None: No lapse rate correction applied.
    lapse_rate_threshold : int, optional
        Elevation difference threshold (in meters) to apply lapse rate correction
        (default: 50). If the elevation difference between the point and stations
        is less than this, no correction is applied.
    lapse_rate_parameters : list of Parameter, optional
        List of parameters to apply lapse rate correction to (default: None,
        which applies to all applicable parameters).

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

    # Check if any stations are close enough for nearest neighbor
    min_distance = df["distance"].min()
    use_nearest = min_distance <= distance_threshold
    if use_nearest and point.elevation is not None and "elevation" in df.columns:
        # Calculate minimum elevation difference
        min_elev_diff = np.abs(df["elevation"] - point.elevation).min()
        use_nearest = min_elev_diff <= elevation_threshold

    # Perform nearest neighbor if applicable
    if use_nearest:
        # Filter applicable stations based on thresholds
        df_filtered = df[
            (df["distance"] <= distance_threshold)
            & (np.abs(df["elevation"] - point.elevation) <= elevation_threshold)
        ]
        df_nearest = nearest_neighbor(df_filtered, ts, point)

    # Check if we need to use IDW
    if not use_nearest or len(df_nearest) == 0 or df_nearest.isna().any().any():
        # Perform IDW interpolation
        idw_func = inverse_distance_weighting(
            power=power, elevation_weight=elevation_weight
        )
        df_idw = idw_func(df, ts, point)

    # Merge DataFrames with priority to nearest neighbor
    if use_nearest and len(df_nearest) > 0:
        # Combine nearest and IDW results, prioritizing nearest values
        result = df_nearest.combine_first(df_idw)
    else:
        result = df_idw

    # If no data is returned, return None
    if result is None or result.empty:
        return None

    # Drop location-related columns & return
    return result.drop(["latitude", "longitude", "elevation", "distance"], axis=1)
