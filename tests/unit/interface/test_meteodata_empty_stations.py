"""
Unit Test - MeteoData with no stations

Tests the fix for the issue where an AttributeError occurs
when no weather stations are found near a location.

The code is licensed under the MIT license.
"""

import pandas as pd
from datetime import datetime
from meteostat import Monthly, Hourly, Daily, Normals
from meteostat.interface.point import Point


def test_monthly_no_stations():
    """
    Test: Monthly class with no stations found (simulated via empty station list)
    """
    # Create an empty DataFrame with station columns
    empty_stations = pd.DataFrame(columns=["id", "latitude", "longitude", "elevation"])
    empty_stations = empty_stations.set_index("id")
    
    # This should not raise AttributeError: 'Monthly' object has no attribute '_types'
    try:
        data = Monthly(empty_stations, start=datetime(2024, 1, 1), end=datetime(2024, 12, 31))
        df = data.fetch()
        # Should return an empty DataFrame with the correct columns
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    except AttributeError as e:
        if "'Monthly' object has no attribute '_types'" in str(e):
            raise AssertionError(f"Bug still present: {e}")
        raise


def test_hourly_no_stations():
    """
    Test: Hourly class with no stations found
    """
    empty_stations = pd.DataFrame(columns=["id", "latitude", "longitude", "elevation"])
    empty_stations = empty_stations.set_index("id")
    
    try:
        data = Hourly(empty_stations, start=datetime(2024, 1, 1, 0), end=datetime(2024, 1, 1, 23))
        df = data.fetch()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    except AttributeError as e:
        if "'Hourly' object has no attribute '_types'" in str(e):
            raise AssertionError(f"Bug still present: {e}")
        raise


def test_daily_no_stations():
    """
    Test: Daily class with no stations found
    """
    empty_stations = pd.DataFrame(columns=["id", "latitude", "longitude", "elevation"])
    empty_stations = empty_stations.set_index("id")
    
    try:
        data = Daily(empty_stations, start=datetime(2024, 1, 1), end=datetime(2024, 1, 31))
        df = data.fetch()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    except AttributeError as e:
        if "'Daily' object has no attribute '_types'" in str(e):
            raise AssertionError(f"Bug still present: {e}")
        raise


def test_normals_no_stations():
    """
    Test: Normals class with no stations found
    """
    empty_stations = pd.DataFrame(columns=["id", "latitude", "longitude", "elevation"])
    empty_stations = empty_stations.set_index("id")
    
    try:
        # The main bug fix: creating a Normals object with no stations should not raise AttributeError
        data = Normals(empty_stations, start=1991, end=2020)
        # Check that data object was created successfully
        assert isinstance(data, Normals)
        assert len(data._stations) == 0
        assert data.count() == 0
    except AttributeError as e:
        if "'Normals' object has no attribute '_types'" in str(e):
            raise AssertionError(f"Bug still present: {e}")
        raise
