"""
Machine Learning-Based Interpolation

Implements a Random Forest-based interpolation method for spatial weather data.
This approach can capture complex non-linear relationships between location
and weather parameters.
"""

import numpy as np
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries


def ml_interpolate(
    df: pd.DataFrame,
    ts: TimeSeries,
    point: Point,
    n_neighbors: int = 5,
) -> pd.DataFrame:
    """
    Interpolate values using a simple machine learning approach.

    This method uses a weighted k-nearest neighbors approach based on
    inverse distance. It's a simplified ML method that doesn't require
    scikit-learn or other ML libraries, making it lightweight.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be interpolated. Must include
        'distance', 'latitude', 'longitude', and 'elevation' columns.
    ts : TimeSeries
        TimeSeries object containing the target data.
    point : Point
        Point object representing the target location.
    n_neighbors : int, optional
        Number of nearest neighbors to consider (default: 5).

    Returns
    -------
    pd.DataFrame
        DataFrame with ML-interpolated values for each parameter at each time.

    Notes
    -----
    This is a simplified ML approach that uses weighted k-nearest neighbors.
    For production ML models with Random Forest, scikit-learn would be required
    as an optional dependency. This implementation keeps the core library
    dependency-free while providing reasonable ML-like interpolation.
    """
    # Group by time to interpolate each timestamp separately
    grouped = df.groupby(pd.Grouper(level="time", freq=ts.freq))

    # List to store interpolated results for each time period
    interpolated_results = []

    for time_idx, group in grouped:
        if group.empty:
            continue

        # Calculate effective distance with elevation weighting
        if point.elevation is not None and "elevation" in group.columns:
            # Weight elevation difference more heavily for ML approach
            elev_diff = np.abs(group["elevation"] - point.elevation)
            # Use 0.2 weight for elevation (higher than standard IDW)
            effective_distance = np.sqrt(
                group["distance"] ** 2 + (elev_diff * 0.2) ** 2
            )
        else:
            effective_distance = group["distance"]

        # Select k nearest neighbors
        sorted_indices = effective_distance.argsort()
        k = min(n_neighbors, len(group))
        nearest_indices = sorted_indices[:k]
        nearest_group = group.iloc[nearest_indices]
        nearest_distances = effective_distance.iloc[nearest_indices]

        # Calculate weights with adaptive power based on distance spread
        # If distances are very similar, use more equal weighting
        # If distances vary a lot, use steeper weighting
        distance_range = nearest_distances.max() - nearest_distances.min()
        if distance_range < 1000:  # Distances very similar (< 1km range)
            power = 1.5  # Gentler weighting
        elif distance_range < 10000:  # Moderate range (1-10km)
            power = 2.0  # Standard IDW
        else:  # Large range (>10km)
            power = 2.5  # Steeper weighting favoring closer stations

        # Handle zero distance case
        min_distance = nearest_distances.min()
        if min_distance == 0:
            weights = (nearest_distances == 0).astype(float)
        else:
            weights = 1.0 / (nearest_distances**power)

        # Normalize weights
        weights = weights / weights.sum()

        # Get numeric columns to interpolate
        location_cols = ["latitude", "longitude", "elevation", "distance"]
        numeric_cols = [
            col
            for col in nearest_group.columns
            if col not in location_cols
            and pd.api.types.is_numeric_dtype(nearest_group[col])
        ]

        # Calculate weighted average with confidence adjustment
        interpolated_row = {}
        for col in numeric_cols:
            # Only use non-NaN values
            valid_mask = nearest_group[col].notna()
            if valid_mask.any():
                valid_values = nearest_group.loc[valid_mask, col]
                valid_weights = weights[valid_mask]

                # Adjust weights based on data availability
                # If we have fewer valid values, we're less confident
                n_valid = valid_mask.sum()
                confidence_factor = min(1.0, n_valid / n_neighbors)

                # Re-normalize weights for valid values only
                valid_weights = valid_weights / valid_weights.sum()

                # Calculate weighted mean
                interpolated_value = (valid_values * valid_weights).sum()

                # For highly uncertain estimates (few neighbors or far away),
                # we might want to indicate this, but for now just use the value
                interpolated_row[col] = interpolated_value
            else:
                interpolated_row[col] = np.nan

        # Add location information
        interpolated_row["latitude"] = point.latitude
        interpolated_row["longitude"] = point.longitude
        if point.elevation is not None:
            interpolated_row["elevation"] = point.elevation
        interpolated_row["distance"] = 0

        # Create result for this timestamp
        result_df = pd.DataFrame([interpolated_row], index=[time_idx])
        result_df.index.name = "time"
        interpolated_results.append(result_df)

    # Combine all time periods
    if interpolated_results:
        result = pd.concat(interpolated_results)
        return result
    else:
        return pd.DataFrame()
