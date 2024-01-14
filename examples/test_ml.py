import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def ml_interpolation(df, target_lat, target_lon, target_elevation):
    result_df = pd.DataFrame(
        columns=["temp", "latitude", "longitude", "elevation", "time"]
    )

    # Group by time
    grouped = df.groupby(level="time")

    # Prepare the data
    features = df[["latitude", "longitude", "elevation"]].values
    target = df["temp"].values

    # Initialize the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    for time, group_data in grouped:
        group_features = group_data[["latitude", "longitude", "elevation"]].values
        group_target = group_data["temp"].values

        # Fit the model for each time
        model.fit(group_features, group_target)

        # Create a DataFrame for the target point
        target_data = np.array([[target_lat, target_lon, target_elevation]])

        # Predict temperature for the target point
        interpolated_temp = model.predict(target_data)

        # Create a DataFrame with the interpolated temperature for this time
        result_row = pd.DataFrame(
            {
                "temp": [interpolated_temp[0]],
                "latitude": [target_lat],
                "longitude": [target_lon],
                "elevation": [target_elevation],
                "time": [time],
            }
        )

        result_df = pd.concat([result_df, result_row], ignore_index=True)

    return result_df


# Example usage
original_df = pd.DataFrame(
    {
        "temp": [-0.4, 0.1, 0.6, 2.4, -0.1, 1.4],
        "latitude": [50.2167, 50.2167, 50.05, 50.05, 49.52, 49.52],
        "longitude": [8.45, 8.45, 8.6, 8.6, 8.55, 8.55],
        "elevation": [805, 805, 111, 111, 96, 96],
    },
    index=pd.MultiIndex.from_tuples(
        [
            (10635, "2020-01-01 10:00:00"),
            (10635, "2020-01-01 11:00:00"),
            (10637, "2020-01-01 10:00:00"),
            (10637, "2020-01-01 11:00:00"),
            (10729, "2020-01-01 10:00:00"),
            (10729, "2020-01-01 11:00:00"),
        ],
        names=["station", "time"],
    ),
)

target_latitude = 49.8  # Replace with your desired latitude
target_longitude = 8.4  # Replace with your desired longitude
target_elevation = 500  # Replace with your desired elevation

result = ml_interpolation(
    original_df, target_latitude, target_longitude, target_elevation
)
print(result)
