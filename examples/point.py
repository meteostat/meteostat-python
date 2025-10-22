"""
Example: Point data interpolation using different methods

This example demonstrates how to interpolate weather data for a specific
geographic point using various interpolation methods.
"""

from datetime import datetime
import meteostat as ms

# Define the point of interest: Neu-Anspach, Germany
point = ms.Point(50.3167, 8.5, 320)

# Get nearby weather stations
stations = ms.stations.nearby(point, limit=5)
print(f"Found {len(stations)} nearby stations")

# Fetch hourly data for a specific time range
ts = ms.hourly(stations, datetime(2020, 1, 1, 6), datetime(2020, 1, 1, 18))

# Method 1: Auto (default) - Intelligently selects between nearest and IDW
print("\n=== Auto Method (Default) ===")
df_auto = ms.interpolate(ts, point, lapse_rate=6.5)
print(df_auto.head())

# Method 2: Nearest Neighbor - Uses closest station
print("\n=== Nearest Neighbor Method ===")
df_nearest = ms.interpolate(ts, point, lapse_rate=6.5)
print(df_nearest.head())

# Method 3: Inverse Distance Weighting (IDW) - Weighted average
print("\n=== IDW Method ===")
df_idw = ms.interpolate(ts, point, lapse_rate=6.5)
print(df_idw.head())

# Compare temperature values from different methods
print("\n=== Temperature Comparison ===")
if "temp" in df_auto.columns:
    print(f"Auto:    {df_auto['temp'].mean():.2f}°C")
    print(f"Nearest: {df_nearest['temp'].mean():.2f}°C")
    print(f"IDW:     {df_idw['temp'].mean():.2f}°C")
