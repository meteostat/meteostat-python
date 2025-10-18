"""
Random Forest Regression (RFR) Interpolation

Implements Random Forest-based spatial interpolation for weather data.
This method uses scikit-learn's RandomForestRegressor to capture complex
non-linear relationships between location features and weather parameters.

Note: This method requires scikit-learn to be installed. It will be imported
dynamically when the method is called.
"""

import numpy as np
import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries


def rfr_interpolate(
    df: pd.DataFrame,
    ts: TimeSeries,
    point: Point,
    n_estimators: int = 50,
    max_depth: int = 10,
) -> pd.DataFrame:
    """
    Interpolate values using Random Forest Regression.

    This method trains a Random Forest model on nearby station data to predict
    weather values at the target point. It captures complex spatial relationships
    between location features (latitude, longitude, elevation) and weather parameters.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be interpolated. Must include
        'distance', 'latitude', 'longitude', and 'elevation' columns.
    ts : TimeSeries
        TimeSeries object containing the target data.
    point : Point
        Point object representing the target location.
    n_estimators : int, optional
        Number of trees in the random forest (default: 50).
    max_depth : int, optional
        Maximum depth of each tree (default: 10).

    Returns
    -------
    pd.DataFrame
        DataFrame with RFR-interpolated values for each parameter at each time.

    Raises
    ------
    ImportError
        If scikit-learn is not installed.

    Notes
    -----
    This method requires scikit-learn to be installed:
        pip install scikit-learn

    The Random Forest approach is based on:
    - Hengl et al. (2018): "Random forest as a generic framework for predictive
      modeling of spatial and spatio-temporal variables"
    - Sekulić et al. (2020): "Random Forest Spatial Interpolation"

    Reference implementation: https://github.com/AleksandarSekulic/RFSI
    """
    # Import sklearn dynamically
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ImportError as e:
        raise ImportError(
            "Random Forest Regression interpolation requires scikit-learn. "
            "Install it with: pip install scikit-learn"
        ) from e

    # Group by time to interpolate each timestamp separately
    grouped = df.groupby(pd.Grouper(level="time", freq=ts.freq))

    # List to store interpolated results for each time period
    interpolated_results = []

    for time_idx, group in grouped:
        if group.empty:
            continue

        # Prepare feature matrix for training
        # Features: latitude, longitude, elevation
        feature_cols = ["latitude", "longitude"]
        if point.elevation is not None and "elevation" in group.columns:
            feature_cols.append("elevation")

        # Get numeric columns to interpolate (exclude location-related columns)
        location_cols = ["latitude", "longitude", "elevation", "distance"]
        numeric_cols = [
            col
            for col in group.columns
            if col not in location_cols and pd.api.types.is_numeric_dtype(group[col])
        ]

        interpolated_row = {}

        # Train a separate model for each weather parameter
        for col in numeric_cols:
            # Only use rows with non-NaN values for this parameter
            valid_mask = group[col].notna()

            if not valid_mask.any():
                # No valid data for this parameter
                interpolated_row[col] = np.nan
                continue

            # Extract training data
            X_train = group.loc[valid_mask, feature_cols].values
            y_train = group.loc[valid_mask, col].values

            # Check if we have enough training samples
            if len(X_train) < 2:
                # Not enough samples for Random Forest, use simple mean
                interpolated_row[col] = y_train.mean()
                continue

            # Prepare target point features
            X_target = [[point.latitude, point.longitude]]
            if "elevation" in feature_cols:
                X_target[0].append(point.elevation if point.elevation else 0)

            # Train Random Forest model
            try:
                # Adjust n_estimators based on available data
                n_est = min(n_estimators, max(10, len(X_train) * 5))

                model = RandomForestRegressor(
                    n_estimators=n_est,
                    max_depth=max_depth,
                    random_state=42,
                    n_jobs=1,  # Use single core for consistency
                )
                model.fit(X_train, y_train)

                # Predict at target point
                prediction = model.predict(X_target)[0]
                interpolated_row[col] = prediction

            except Exception as e:
                # If model training fails, fall back to weighted average
                # based on inverse distance
                distances = group.loc[valid_mask, "distance"].values
                if distances.min() == 0:
                    # Exact match with a station
                    interpolated_row[col] = y_train[distances.argmin()]
                else:
                    # Inverse distance weighting
                    weights = 1.0 / (distances**2)
                    weights = weights / weights.sum()
                    interpolated_row[col] = (y_train * weights).sum()

        # Add location information
        interpolated_row["latitude"] = point.latitude
        interpolated_row["longitude"] = point.longitude
        if point.elevation is not None:
            interpolated_row["elevation"] = point.elevation
        else:
            interpolated_row["elevation"] = 0
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
