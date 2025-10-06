"""
E2E Test - Point Class with Long Period

Tests that Point data retrieval works correctly over long periods
where some stations may have missing data.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Point, Hourly


def test_point_long_period():
    """
    Test: Point data retrieval over long period (1990-2023)
    
    This test verifies that the KeyError is not raised when trying to get
    hourly data from a point over a long time period where some stations
    may have missing data for certain years.
    
    Issue: https://github.com/meteostat/meteostat-python/issues/XXX
    """
    
    # Create Point (coordinates from the original issue)
    location = Point(52.9, 11.5, 23)
    start = datetime(1990, 1, 1)
    end = datetime(2023, 12, 31)
    
    # This should not raise a KeyError
    data = Hourly(location, start, end)
    result = data.fetch()
    
    # Verify that we get some data (may be empty or have data, but shouldn't crash)
    assert result is not None
    assert isinstance(result.index.name, str) or result.index.name is None
