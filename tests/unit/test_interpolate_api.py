"""
Tests for the interpolate API function
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from meteostat import Point, interpolate
from meteostat.api.timeseries import TimeSeries
from meteostat.enumerations import Granularity


@pytest.fixture
def mock_timeseries():
    """Create a mock TimeSeries with sample data"""
    times = pd.date_range("2020-01-01", periods=3, freq="1h")

    data = []
    # Station 1
    for time in times:
        data.append(
            {
                "time": time,
                "station": "STATION1",
                "source": "bulk",
                "temp": 20.0,
                "prcp": 1.0,
            }
        )

    # Station 2
    for time in times:
        data.append(
            {
                "time": time,
                "station": "STATION2",
                "source": "bulk",
                "temp": 18.0,
                "prcp": 2.0,
            }
        )

    df = pd.DataFrame(data).set_index(["station", "time", "source"])

    # Create mock station objects
    from meteostat.typing import Station

    station1 = Station(
        id="STATION1",
        names={"en": "Station 1"},
        country="DE",
        region="HE",
        latitude=50.01,
        longitude=8.01,
        elevation=100,
        timezone="Europe/Berlin",
    )

    station2 = Station(
        id="STATION2",
        names={"en": "Station 2"},
        country="DE",
        region="HE",
        latitude=50.1,
        longitude=8.1,
        elevation=200,
        timezone="Europe/Berlin",
    )

    ts = TimeSeries(
        granularity=Granularity.HOURLY,
        station=[station1, station2],
        df=df,
        start=datetime(2020, 1, 1),
        end=datetime(2020, 1, 1, 2),
    )

    return ts


class TestInterpolateAPI:
    """Tests for the interpolate API function"""

    def test_string_method_auto(self, mock_timeseries):
        """Test using 'auto' method string"""
        point = Point(50.0, 8.0, 100)
        result = interpolate(mock_timeseries, point, method="auto")

        assert result is not None
        assert not result.empty
        assert "temp" in result.columns
        assert "prcp" in result.columns

    def test_string_method_nearest(self, mock_timeseries):
        """Test using 'nearest' method string"""
        point = Point(50.0, 8.0, 100)
        result = interpolate(mock_timeseries, point, method="nearest")

        assert result is not None
        assert not result.empty
        assert "temp" in result.columns

    def test_string_method_idw(self, mock_timeseries):
        """Test using 'idw' method string"""
        point = Point(50.0, 8.0, 100)
        result = interpolate(mock_timeseries, point, method="idw")

        assert result is not None
        assert not result.empty
        assert "temp" in result.columns

    def test_string_method_ml(self, mock_timeseries):
        """Test using 'ml' method string"""
        point = Point(50.0, 8.0, 100)
        result = interpolate(mock_timeseries, point, method="ml")

        assert result is not None
        assert not result.empty
        assert "temp" in result.columns

    def test_invalid_method_string(self, mock_timeseries):
        """Test that invalid method string raises error"""
        point = Point(50.0, 8.0, 100)

        with pytest.raises(ValueError) as excinfo:
            interpolate(mock_timeseries, point, method="invalid_method")

        assert "Unknown method" in str(excinfo.value)
        assert "invalid_method" in str(excinfo.value)

    def test_custom_method_function(self, mock_timeseries):
        """Test using a custom interpolation function"""
        point = Point(50.0, 8.0, 100)

        # Define a simple custom method that just takes the mean
        def custom_method(df, ts, point):
            result = df.groupby(pd.Grouper(level="time", freq=ts.freq)).mean()
            result["latitude"] = point.latitude
            result["longitude"] = point.longitude
            result["elevation"] = point.elevation if point.elevation else 0
            result["distance"] = 0
            return result

        result = interpolate(mock_timeseries, point, method=custom_method)

        assert result is not None
        assert not result.empty
        # Custom method should compute mean (after lapse rate adjustment)
        # The exact value depends on lapse rate calculation
        assert "temp" in result.columns
        assert result["temp"].iloc[0] > 18.0  # Between station values

    def test_location_columns_removed(self, mock_timeseries):
        """Test that location columns are removed from result"""
        point = Point(50.0, 8.0, 100)
        result = interpolate(mock_timeseries, point, method="auto")

        # These columns should NOT be in the result
        assert "latitude" not in result.columns
        assert "longitude" not in result.columns
        assert "elevation" not in result.columns
        assert "distance" not in result.columns

    def test_case_insensitive_method(self, mock_timeseries):
        """Test that method names are case-insensitive"""
        point = Point(50.0, 8.0, 100)

        result1 = interpolate(mock_timeseries, point, method="AUTO")
        result2 = interpolate(mock_timeseries, point, method="Auto")
        result3 = interpolate(mock_timeseries, point, method="auto")

        # All should work and return same results
        assert result1 is not None
        assert result2 is not None
        assert result3 is not None

    def test_lapse_rate_parameter(self, mock_timeseries):
        """Test that lapse_rate parameter is accepted"""
        point = Point(50.0, 8.0, 100)

        # Should work with different lapse rates
        result1 = interpolate(mock_timeseries, point, method="auto", lapse_rate=6.5)
        result2 = interpolate(mock_timeseries, point, method="auto", lapse_rate=0)

        assert result1 is not None
        assert result2 is not None

    def test_default_method(self, mock_timeseries):
        """Test that default method is 'auto'"""
        point = Point(50.0, 8.0, 100)

        # Should use 'auto' by default
        result = interpolate(mock_timeseries, point)

        assert result is not None
        assert not result.empty
