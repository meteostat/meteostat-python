import pandas as pd
import numpy as np


def idw_interpolation(df, target_lat, target_lon, target_elevation, power=2):
    result_df = pd.DataFrame(
        columns=["temp", "latitude", "longitude", "elevation", "time"]
    )

    # Group by time
    grouped = df.groupby(level="time")

    for time, group_data in grouped:
        # Extract necessary columns for each time group
        latitudes = group_data["latitude"].values
        longitudes = group_data["longitude"].values
        elevations = group_data["elevation"].values
        temperatures = group_data["temp"].values

        # Calculate distances to target point for each time group
        distances = np.sqrt(
            ((latitudes - target_lat) * (110.574) * np.cos(target_lat * np.pi / 180))
            ** 2
            + ((longitudes - target_lon) * (111.32)) ** 2
            + ((elevations - target_elevation) * 0.001) ** 2
        )

        # Avoid division by zero and calculate weights for each time group
        weights = 1 / (distances + 1e-10) ** power

        # Perform the weighted interpolation for each time group
        interpolated_temp = np.sum(temperatures * weights) / np.sum(weights)

        # Create a DataFrame with the interpolated temperature for this time
        result_row = pd.DataFrame(
            {
                "temp": [interpolated_temp],
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

result = idw_interpolation(
    original_df, target_latitude, target_longitude, target_elevation
)
print(result)
