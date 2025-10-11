#!/usr/bin/env python
"""
Example: Using Point objects as input to time series functions

This example demonstrates the new feature that allows passing Point objects
directly to ms.hourly, ms.daily, ms.monthly, and ms.normals functions.

Points are automatically converted to "virtual weather stations" with IDs
in the form of $0001, $0002, etc.
"""

from datetime import date
import meteostat as ms

print("=" * 80)
print("Meteostat: Using Point objects as time series input")
print("=" * 80)
print()

# Example 1: Single Point (as shown in the issue)
print("Example 1: Single Point Input")
print("-" * 80)
print("Code:")
print("  point = ms.Point(50.110924, 8.682127, 112)")
print("  # This would normally fetch data:")
print("  # ts = ms.hourly(point, date(2024, 1, 1), date(2024, 1, 1))")
print()

point = ms.Point(50.110924, 8.682127, 112)
# Demonstrate the conversion
from meteostat.utils.parsers import parse_station

stations = parse_station(point)
print(f"Result:")
print(f"  Point converted to virtual station: {stations[0].id}")
print(
    f"  Station location: lat={stations[0].location.latitude}, "
    f"lon={stations[0].location.longitude}, "
    f"elevation={stations[0].location.elevation}"
)
print()

# Example 2: Multiple Points (as shown in the issue)
print("Example 2: Multiple Points Input")
print("-" * 80)
print("Code:")
print("  point1 = ms.Point(50, 8, 100)  # -> $0001")
print("  point2 = ms.Point(51, 8, 100)  # -> $0002")
print("  point3 = ms.Point(52, 8, 100)  # -> $0003")
print("  # This would normally fetch data:")
print("  # ts = ms.hourly([point1, point2, point3], ...)")
print()

point1 = ms.Point(50, 8, 100)
point2 = ms.Point(51, 8, 100)
point3 = ms.Point(52, 8, 100)

stations = parse_station([point1, point2, point3])
print("Result:")
for i, station in enumerate(stations, 1):
    print(
        f"  Point {i} -> Station ID: {station.id}, "
        f"Location: ({station.location.latitude}, {station.location.longitude})"
    )
print()

# Example 3: Mixed Points and Station IDs
print("Example 3: Mixed Points and Station IDs")
print("-" * 80)
print("Code:")
print("  point1 = ms.Point(50, 8, 100)")
print("  point2 = ms.Point(51, 8, 100)")
print("  # Mix with station IDs (this would normally fetch from API):")
print("  # ts = ms.hourly([point1, '10637', point2], ...)")
print()

# Create a mock Station object to demonstrate mixing
mock_station = ms.typing.Station(id="10637", location=ms.Point(52, 8, 100))
stations = parse_station([point1, mock_station, point2])
print("Result:")
for station in stations:
    station_type = "Virtual" if station.id.startswith("$") else "Regular"
    print(f"  {station_type} Station: {station.id}")
print()

# Example 4: All time series functions support Points
print("Example 4: All time series functions support Point input")
print("-" * 80)
print("Supported functions:")
print("  - ms.hourly(point, start, end)")
print("  - ms.daily(point, start, end)")
print("  - ms.monthly(point, start, end)")
print("  - ms.normals(point, start_year, end_year)")
print()
print("Type signatures accept:")
print("  str | Station | Point | List[str | Station | Point] | pd.Index | pd.Series")
print()

# Example 5: Show how Station.location works
print("Example 5: Station.location property")
print("-" * 80)
point = ms.Point(50.110924, 8.682127, 112)
station = ms.typing.Station(
    id="CUSTOM",
    location=point,
    latitude=point.latitude,
    longitude=point.longitude,
    elevation=point.elevation,
)
print("All Station objects now have a 'location' property that is a Point instance:")
print(f"  station.id = {station.id}")
print(
    f"  station.location = Point({station.location.latitude}, "
    f"{station.location.longitude}, {station.location.elevation})"
)
print(f"  station.location.latitude = {station.location.latitude}")
print(f"  station.location.longitude = {station.location.longitude}")
print(f"  station.location.elevation = {station.location.elevation}")
print()

print("=" * 80)
print("Note: This feature is particularly useful for providers that support")
print("data retrieval by geo coordinates (e.g., metno_forecast)")
print("=" * 80)
