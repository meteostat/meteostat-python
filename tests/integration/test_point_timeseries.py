"""
Integration Test - Point as Time Series Input

Tests for using Point objects as input to hourly, daily, monthly, and normals functions.

The code is licensed under the MIT license.
"""

from datetime import datetime, date
import meteostat as ms
from meteostat.utils.parsers import parse_station


def test_hourly_point_conversion():
    """
    Test that Point is properly converted when passed to hourly function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    stations = parse_station(point)

    # Verify that the station was created with ID $0001
    assert len(stations) == 1
    assert stations[0].id == "$0001"
    assert stations[0].location is point
    assert stations[0].latitude == 50.110924
    assert stations[0].longitude == 8.682127
    assert stations[0].elevation == 112


def test_daily_point_conversion():
    """
    Test that Point is properly converted when passed to daily function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    stations = parse_station(point)

    # Verify that the station was created with ID $0001
    assert len(stations) == 1
    assert stations[0].id == "$0001"
    assert stations[0].location is point


def test_monthly_point_conversion():
    """
    Test that Point is properly converted when passed to monthly function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    stations = parse_station(point)

    # Verify that the station was created with ID $0001
    assert len(stations) == 1
    assert stations[0].id == "$0001"
    assert stations[0].location is point


def test_normals_point_conversion():
    """
    Test that Point is properly converted when passed to normals function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    stations = parse_station(point)

    # Verify that the station was created with ID $0001
    assert len(stations) == 1
    assert stations[0].id == "$0001"
    assert stations[0].location is point


def test_multiple_points_conversion():
    """
    Test that multiple Points are properly converted with sequential IDs
    """
    point1 = ms.Point(50.0, 8.0, 100)
    point2 = ms.Point(51.0, 9.0, 200)
    point3 = ms.Point(52.0, 10.0, 300)

    stations = parse_station([point1, point2, point3])

    # Verify that stations were created with IDs $0001, $0002, $0003
    assert len(stations) == 3
    assert stations[0].id == "$0001"
    assert stations[1].id == "$0002"
    assert stations[2].id == "$0003"
    assert stations[0].location is point1
    assert stations[1].location is point2
    assert stations[2].location is point3


def test_mixed_stations_and_points_conversion():
    """
    Test that mixed Station objects and Points are handled correctly
    """
    point1 = ms.Point(50.0, 8.0, 100)
    # Create a Station object with a location
    station1 = ms.typing.Station(id="TEST01", location=ms.Point(51.0, 9.0, 200))
    point2 = ms.Point(52.0, 10.0, 300)

    stations = parse_station([point1, station1, point2])

    # Verify that Points were converted to virtual stations and regular station was preserved
    assert len(stations) == 3
    assert stations[0].id == "$0001"
    assert stations[0].location is point1
    assert stations[1].id == "TEST01"
    assert stations[2].id == "$0002"
    assert stations[2].location is point2
