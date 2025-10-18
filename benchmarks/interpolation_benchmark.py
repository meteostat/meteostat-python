"""
Benchmark script for interpolation methods

This script compares the performance of different interpolation methods
using real-world data from multiple locations.
"""

import time
from datetime import datetime, date
import pandas as pd
import meteostat as ms


def benchmark_location(point, location_name, start, end):
    """Benchmark interpolation methods for a specific location"""
    print(f"\n{'=' * 60}")
    print(f"Benchmarking: {location_name}")
    print(f"Point: Lat {point.latitude}, Lon {point.longitude}, Elev {point.elevation}m")
    print(f"Period: {start} to {end}")
    print(f"{'=' * 60}")

    # Get nearby stations
    stations = ms.stations.nearby(point, limit=10)
    print(f"\nFound {len(stations)} nearby stations")
    if len(stations) > 0:
        print(f"Closest station: {stations.iloc[0]['distance']:.0f}m away")

    # Fetch time series data
    ts = ms.hourly(stations, start, end)
    print(f"Time series data points: {len(ts)}")

    if len(ts) == 0:
        print("⚠️  No data available for this location/period")
        return None

    methods = {
        "nearest": "Nearest Neighbor",
        "idw": "Inverse Distance Weighting",
        "ml": "Machine Learning",
        "auto": "Auto (Hybrid)",
    }

    results = {}

    for method_key, method_name in methods.items():
        print(f"\n{method_name}:")
        try:
            # Measure execution time
            start_time = time.time()
            df = ms.interpolate(ts, point, method=method_key)
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

            if df is not None and not df.empty:
                # Calculate some statistics
                temp_data = df["temp"] if "temp" in df.columns else None
                prcp_data = df["prcp"] if "prcp" in df.columns else None

                results[method_key] = {
                    "execution_time": execution_time,
                    "data_points": len(df),
                    "temp_mean": temp_data.mean() if temp_data is not None else None,
                    "temp_std": temp_data.std() if temp_data is not None else None,
                    "prcp_sum": prcp_data.sum() if prcp_data is not None else None,
                }

                print(f"  ✓ Execution time: {execution_time:.2f} ms")
                print(f"  ✓ Data points: {len(df)}")
                if temp_data is not None:
                    print(
                        f"  ✓ Temp: mean={temp_data.mean():.1f}°C, std={temp_data.std():.1f}°C"
                    )
                if prcp_data is not None:
                    print(f"  ✓ Precipitation sum: {prcp_data.sum():.1f}mm")
            else:
                print("  ✗ No data returned")
                results[method_key] = None

        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[method_key] = None

    return results


def compare_methods(results):
    """Compare results from different methods"""
    print(f"\n{'=' * 60}")
    print("Method Comparison")
    print(f"{'=' * 60}")

    # Filter out methods that returned no results
    valid_results = {k: v for k, v in results.items() if v is not None}

    if not valid_results:
        print("No valid results to compare")
        return

    # Performance comparison
    print("\n📊 Performance (Execution Time):")
    times = [(k, v["execution_time"]) for k, v in valid_results.items()]
    times.sort(key=lambda x: x[1])
    for method, time_ms in times:
        print(f"  {method:15s}: {time_ms:6.2f} ms")

    # Temperature comparison (if available)
    temp_results = {k: v for k, v in valid_results.items() if v["temp_mean"] is not None}
    if temp_results:
        print("\n🌡️  Temperature Comparison:")
        for method, data in temp_results.items():
            print(f"  {method:15s}: mean={data['temp_mean']:6.2f}°C, std={data['temp_std']:5.2f}°C")

        # Calculate variance between methods
        temp_means = [v["temp_mean"] for v in temp_results.values()]
        temp_variance = pd.Series(temp_means).std()
        print(f"  Variance between methods: {temp_variance:.2f}°C")


def main():
    """Run benchmarks for multiple locations"""
    print("=" * 60)
    print("Meteostat Interpolation Methods Benchmark")
    print("=" * 60)

    # Test locations with different characteristics
    test_cases = [
        {
            "name": "Frankfurt, Germany (Flat terrain)",
            "point": ms.Point(50.1155, 8.6842, 113),
            "start": datetime(2020, 1, 1),
            "end": datetime(2020, 1, 2),
        },
        {
            "name": "Denver, USA (Mountainous)",
            "point": ms.Point(39.7392, -104.9903, 1609),
            "start": datetime(2020, 6, 1),
            "end": datetime(2020, 6, 2),
        },
        {
            "name": "Singapore (Tropical coastal)",
            "point": ms.Point(1.3521, 103.8198, 15),
            "start": datetime(2020, 7, 1),
            "end": datetime(2020, 7, 2),
        },
    ]

    all_results = {}

    for test_case in test_cases:
        results = benchmark_location(
            test_case["point"],
            test_case["name"],
            test_case["start"],
            test_case["end"],
        )

        if results:
            all_results[test_case["name"]] = results
            compare_methods(results)

    # Overall summary
    print(f"\n{'=' * 60}")
    print("Overall Summary")
    print(f"{'=' * 60}")

    # Average execution times across all locations
    methods = ["nearest", "idw", "ml", "auto"]
    avg_times = {}

    for method in methods:
        times = [
            results[method]["execution_time"]
            for results in all_results.values()
            if results.get(method) is not None
        ]
        if times:
            avg_times[method] = sum(times) / len(times)

    if avg_times:
        print("\n📈 Average Execution Time Across All Locations:")
        sorted_avg = sorted(avg_times.items(), key=lambda x: x[1])
        for method, avg_time in sorted_avg:
            print(f"  {method:15s}: {avg_time:6.2f} ms")

    print("\n✅ Benchmark complete!")


if __name__ == "__main__":
    main()
