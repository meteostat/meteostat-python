"""
Example: Point data interpolation using different methods

This example demonstrates how to interpolate weather data for a specific
geographic point using various interpolation methods.
"""

from datetime import datetime
import meteostat as ms

# Define the point of interest: Frankfurt, Germany
point = ms.Point(50.1155, 8.6842, 113)

# Get nearby weather stations
stations = ms.stations.nearby(point, limit=5)
print(f"Found {len(stations)} nearby stations")

# Fetch hourly data for a specific time range
ts = ms.hourly(stations, datetime(2020, 1, 1, 6), datetime(2020, 1, 1, 18))

# Method 1: Auto (default) - Intelligently selects between nearest and IDW
print("\n=== Auto Method (Default) ===")
df_auto = ms.interpolate(ts, point, method="auto")
print(df_auto.head())

# Method 2: Nearest Neighbor - Uses closest station
print("\n=== Nearest Neighbor Method ===")
df_nearest = ms.interpolate(ts, point, method="nearest")
print(df_nearest.head())

# Method 3: Inverse Distance Weighting (IDW) - Weighted average
print("\n=== IDW Method ===")
df_idw = ms.interpolate(ts, point, method="idw")
print(df_idw.head())

# Method 4: Machine Learning - Adaptive weighted approach
print("\n=== ML Method ===")
df_ml = ms.interpolate(ts, point, method="ml")
print(df_ml.head())

# Compare temperature values from different methods
print("\n=== Temperature Comparison ===")
if "temp" in df_auto.columns:
    print(f"Auto:    {df_auto['temp'].mean():.2f}°C")
    print(f"Nearest: {df_nearest['temp'].mean():.2f}°C")
    print(f"IDW:     {df_idw['temp'].mean():.2f}°C")
    print(f"ML:      {df_ml['temp'].mean():.2f}°C")

