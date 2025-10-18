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
    result = parse_station(point)

    # Verify that a single Station was created (not a list)
    assert isinstance(result, ms.typing.Station)
    assert result.id == "$0001"
    assert result.latitude == 50.110924
    assert result.longitude == 8.682127
    assert result.elevation == 112


def test_daily_point_conversion():
    """
    Test that Point is properly converted when passed to daily function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    result = parse_station(point)

    # Verify that a single Station was created
    assert isinstance(result, ms.typing.Station)
    assert result.id == "$0001"
    assert result.latitude == 50.110924
    assert result.longitude == 8.682127


def test_monthly_point_conversion():
    """
    Test that Point is properly converted when passed to monthly function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    result = parse_station(point)

    # Verify that a single Station was created
    assert isinstance(result, ms.typing.Station)
    assert result.id == "$0001"
    assert result.latitude == 50.110924
    assert result.longitude == 8.682127


def test_normals_point_conversion():
    """
    Test that Point is properly converted when passed to normals function
    """
    point = ms.Point(50.110924, 8.682127, 112)
    result = parse_station(point)

    # Verify that a single Station was created
    assert isinstance(result, ms.typing.Station)
    assert result.id == "$0001"
    assert result.latitude == 50.110924
    assert result.longitude == 8.682127


def test_multiple_points_conversion():
    """
    Test that multiple Points are properly converted with sequential IDs
    """
    point1 = ms.Point(50.0, 8.0, 100)
    point2 = ms.Point(51.0, 9.0, 200)
    point3 = ms.Point(52.0, 10.0, 300)

    result = parse_station([point1, point2, point3])

    # Verify that a list of stations was created
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0].id == "$0001"
    assert result[1].id == "$0002"
    assert result[2].id == "$0003"
    assert result[0].latitude == 50.0
    assert result[1].latitude == 51.0
    assert result[2].latitude == 52.0


def test_mixed_stations_and_points_conversion():
    """
    Test that mixed Station objects and Points are handled correctly
    """
    point1 = ms.Point(50.0, 8.0, 100)
    # Create a Station object
    station1 = ms.typing.Station(
        id="TEST01", latitude=51.0, longitude=9.0, elevation=200
    )
    point2 = ms.Point(52.0, 10.0, 300)

    result = parse_station([point1, station1, point2])

    # Verify that a list was returned with Points converted to virtual stations
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0].id == "$0001"
    assert result[0].latitude == 50.0
    assert result[1].id == "TEST01"
    assert result[2].id == "$0002"
    assert result[2].latitude == 52.0
