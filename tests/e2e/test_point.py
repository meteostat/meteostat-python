"""
E2E Test - Point Class

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Point


def test_point():
    """
    Test: Point Data
    """

    # Create Point for Vancouver, BC
    point = Point(49.2497, -123.1193, 70)

    # Get count of weather stations
    stations = point.get_stations("daily", datetime(2020, 1, 1), datetime(2020, 1, 31))

    # Check if three stations are returned
    assert len(stations.index) == 4
