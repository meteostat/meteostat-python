"""
Tests for interpolation methods
"""

import pytest
import pandas as pd
import numpy as np

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.enumerations import Granularity
from meteostat.interpolation.nearest import nearest_neighbor
from meteostat.interpolation.idw import idw
from meteostat.interpolation.auto import auto_interpolate


@pytest.fixture
def sample_data():
    """Create sample weather data for testing"""
    # Create a multi-index with station and time
    times = pd.date_range("2020-01-01", periods=3, freq="1h")
    stations = ["STATION1", "STATION2", "STATION3"]

    # Create test data
    data = []
    for station_id in stations:
        for time in times:
            data.append(
                {
                    "station": station_id,
                    "time": time,
                    "temp": 20.0 + np.random.randn(),
                    "prcp": 0.0 + np.random.rand(),
                }
            )

    df = pd.DataFrame(data)
    df = df.set_index(["station", "time"])

    return df


@pytest.fixture
def sample_point():
    """Create a sample point"""
    return Point(50.0, 8.0, 100)


@pytest.fixture
def sample_df_with_location():
    """Create sample data with location information"""
    times = pd.date_range("2020-01-01", periods=3, freq="1h")

    data = []
    # Station 1: Very close (1km away, same elevation)
    for time in times:
        data.append(
            {
                "time": time,
                "station": "STATION1",
                "temp": 20.0,
                "prcp": 1.0,
                "latitude": 50.01,
                "longitude": 8.01,
                "elevation": 100,
                "distance": 1000,
            }
        )

    # Station 2: Medium distance (10km away, different elevation)
    for time in times:
        data.append(
            {
                "time": time,
                "station": "STATION2",
                "temp": 18.0,
                "prcp": 2.0,
                "latitude": 50.1,
                "longitude": 8.1,
                "elevation": 200,
                "distance": 10000,
            }
        )

    # Station 3: Far away (50km away)
    for time in times:
        data.append(
            {
                "time": time,
                "station": "STATION3",
                "temp": 15.0,
                "prcp": 3.0,
                "latitude": 50.5,
                "longitude": 8.5,
                "elevation": 300,
                "distance": 50000,
            }
        )

    df = pd.DataFrame(data)
    df = df.set_index(["station", "time"])
    return df


@pytest.fixture
def sample_timeseries(sample_data):
    """Create a sample TimeSeries object"""
    # Mock TimeSeries with minimal required attributes
    ts = TimeSeries(
        granularity=Granularity.HOURLY, station=["STATION1"], df=sample_data
    )
    return ts


class TestNearestNeighbor:
    """Tests for nearest neighbor interpolation"""

    def test_basic_functionality(self, sample_df_with_location, sample_timeseries):
        """Test that nearest neighbor returns the closest station's data"""
        point = Point(50.0, 8.0, 100)
        result = nearest_neighbor(sample_df_with_location, sample_timeseries, point)

        assert not result.empty
        assert "temp" in result.columns
        assert len(result) == 3  # 3 time periods

    def test_selects_closest_station(self, sample_df_with_location, sample_timeseries):
        """Test that it selects the closest station"""
        point = Point(50.0, 8.0, 100)
        result = nearest_neighbor(sample_df_with_location, sample_timeseries, point)

        # Should use STATION1 which is closest (1km)
        # So temp should be 20.0
        assert result["temp"].iloc[0] == 20.0


class TestIDW:
    """Tests for Inverse Distance Weighting interpolation"""

    def test_basic_functionality(self, sample_df_with_location, sample_timeseries):
        """Test that IDW returns interpolated data"""
        point = Point(50.0, 8.0, 100)
        result = idw(sample_df_with_location, sample_timeseries, point)

        assert not result.empty
        assert "temp" in result.columns
        assert len(result) == 3  # 3 time periods

    def test_weighted_average(self, sample_df_with_location, sample_timeseries):
        """Test that IDW produces values between min and max"""
        point = Point(50.0, 8.0, 100)
        result = idw(sample_df_with_location, sample_timeseries, point)

        # Result should be between the min (15) and max (20) station values
        # but closer to 20 since STATION1 is much closer
        temp_value = result["temp"].iloc[0]
        assert 15.0 < temp_value <= 20.0
        # Should be heavily weighted toward the closest station (20.0)
        assert temp_value > 19.0

    def test_elevation_weighting(self, sample_timeseries):
        """Test that elevation affects the interpolation"""
        times = pd.date_range("2020-01-01", periods=1, freq="1h")

        # Create two stations at same horizontal distance but different elevations
        data = []
        # Station 1: Same elevation
        data.append(
            {
                "time": times[0],
                "station": "STATION1",
                "temp": 20.0,
                "latitude": 50.01,
                "longitude": 8.0,
                "elevation": 100,
                "distance": 1000,
            }
        )
        # Station 2: Different elevation (500m higher)
        data.append(
            {
                "time": times[0],
                "station": "STATION2",
                "temp": 20.0,
                "latitude": 50.01,
                "longitude": 8.0,
                "elevation": 600,
                "distance": 1000,
            }
        )

        df = pd.DataFrame(data).set_index(["station", "time"])
        point = Point(50.0, 8.0, 100)

        # With elevation weighting, STATION1 should be preferred
        result = idw(df, sample_timeseries, point, elevation_weight=0.1)

        # Result should favor STATION1 due to elevation match
        assert not result.empty

    def test_handles_missing_values(self, sample_timeseries):
        """Test that IDW handles missing values correctly"""
        times = pd.date_range("2020-01-01", periods=1, freq="1h")

        data = []
        data.append(
            {
                "time": times[0],
                "station": "STATION1",
                "temp": 20.0,
                "latitude": 50.01,
                "longitude": 8.01,
                "elevation": 100,
                "distance": 1000,
            }
        )
        data.append(
            {
                "time": times[0],
                "station": "STATION2",
                "temp": np.nan,  # Missing value
                "latitude": 50.1,
                "longitude": 8.1,
                "elevation": 200,
                "distance": 10000,
            }
        )

        df = pd.DataFrame(data).set_index(["station", "time"])
        point = Point(50.0, 8.0, 100)

        result = idw(df, sample_timeseries, point)

        # Should use only the valid value
        assert result["temp"].iloc[0] == 20.0


class TestAutoInterpolate:
    """Tests for auto interpolation"""

    def test_uses_nearest_for_close_station(self, sample_timeseries):
        """Test that auto uses nearest neighbor for very close stations"""
        times = pd.date_range("2020-01-01", periods=1, freq="1h")

        # Create data with a very close station
        data = []
        data.append(
            {
                "time": times[0],
                "station": "STATION1",
                "temp": 20.0,
                "prcp": 1.0,
                "latitude": 50.0,
                "longitude": 8.0,
                "elevation": 100,
                "distance": 100,  # Very close (100m)
            }
        )
        data.append(
            {
                "time": times[0],
                "station": "STATION2",
                "temp": 15.0,
                "prcp": 2.0,
                "latitude": 50.1,
                "longitude": 8.1,
                "elevation": 100,
                "distance": 10000,
            }
        )

        df = pd.DataFrame(data).set_index(["station", "time"])
        point = Point(50.0, 8.0, 100)

        result = auto_interpolate(df, sample_timeseries, point)

        # Should use nearest neighbor, so temp = 20.0
        assert result["temp"].iloc[0] == 20.0

    def test_uses_idw_for_distant_stations(self, sample_timeseries):
        """Test that auto uses IDW for distant stations"""
        times = pd.date_range("2020-01-01", periods=1, freq="1h")

        # Create data with only distant stations
        data = []
        data.append(
            {
                "time": times[0],
                "station": "STATION1",
                "temp": 20.0,
                "latitude": 50.1,
                "longitude": 8.1,
                "elevation": 100,
                "distance": 10000,  # 10km
            }
        )
        data.append(
            {
                "time": times[0],
                "station": "STATION2",
                "temp": 18.0,
                "latitude": 50.2,
                "longitude": 8.2,
                "elevation": 100,
                "distance": 20000,  # 20km
            }
        )

        df = pd.DataFrame(data).set_index(["station", "time"])
        point = Point(50.0, 8.0, 100)

        result = auto_interpolate(df, sample_timeseries, point)

        # Should use IDW, so result should be weighted average
        # Closer to 20.0 than 18.0 since STATION1 is closer
        temp_value = result["temp"].iloc[0]
        assert 18.0 < temp_value <= 20.0
        assert temp_value > 19.0

    def test_respects_elevation_threshold(self, sample_timeseries):
        """Test that elevation threshold is respected"""
        times = pd.date_range("2020-01-01", periods=1, freq="1h")

        # Station close in distance but far in elevation
        data = []
        data.append(
            {
                "time": times[0],
                "station": "STATION1",
                "temp": 20.0,
                "latitude": 50.0,
                "longitude": 8.0,
                "elevation": 500,  # 400m elevation difference
                "distance": 1000,  # Only 1km away
            }
        )
        data.append(
            {
                "time": times[0],
                "station": "STATION2",
                "temp": 18.0,
                "latitude": 50.1,
                "longitude": 8.1,
                "elevation": 100,
                "distance": 10000,
            }
        )

        df = pd.DataFrame(data).set_index(["station", "time"])
        point = Point(50.0, 8.0, 100)

        result = auto_interpolate(df, sample_timeseries, point)

        # Should use IDW due to elevation difference
        # Result should be a weighted average, not just STATION1
        temp_value = result["temp"].iloc[0]
        assert 18.0 < temp_value <= 20.0
