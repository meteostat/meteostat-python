"""
Auto Interpolation Method

Intelligently selects between nearest neighbor and IDW based on spatial context.
This provides a good default that adapts to the specific situation.
"""

import numpy as np
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.interpolation.nearest import nearest_neighbor
from meteostat.interpolation.idw import inverse_distance_weighting


def combined(
    distance_threshold: float = 5000,
    elevation_threshold: float = 50,
) -> pd.DataFrame:
    """
    Automatically select the best interpolation method based on spatial context.

    Uses nearest neighbor if a very close station at similar elevation exists,
    otherwise uses IDW for better accuracy across multiple stations.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be interpolated. Must include
        'distance', 'latitude', 'longitude', and 'elevation' columns.
    ts : TimeSeries
        TimeSeries object containing the target data.
    point : Point
        Point object representing the target location.
    distance_threshold : float, optional
        Maximum distance (in meters) to use nearest neighbor (default: 5000).
        Beyond this, IDW is used.
    elevation_threshold : float, optional
        Maximum elevation difference (in meters) to use nearest neighbor (default: 50).
        Beyond this, IDW is used even if distance is within threshold.

    Returns
    -------
    pd.DataFrame
        DataFrame with auto-interpolated values using the selected method.

    Notes
    -----
    Decision logic:
    - If nearest station is within distance_threshold AND elevation_threshold:
      Use nearest neighbor (most accurate for very close stations)
    - Otherwise: Use IDW (better for distributed or distant stations)
    """
    def _get_df(
        df: pd.DataFrame,
        ts: TimeSeries,
        point: Point
    ) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()

        # Find the minimum distance across all time periods
        min_distance = df["distance"].min()

        # Check elevation difference if available
        use_nearest = min_distance <= distance_threshold

        if use_nearest and point.elevation is not None and "elevation" in df.columns:
            # Calculate minimum elevation difference
            min_elev_diff = np.abs(df["elevation"] - point.elevation).min()
            use_nearest = min_elev_diff <= elevation_threshold

        # Select method based on decision
        if use_nearest:
            # Use nearest neighbor for very close stations
            return nearest_neighbor(df, ts, point)
        else:
            # Use IDW for better averaging across stations
            return inverse_distance_weighting()(df, ts, point)

    return _get_df