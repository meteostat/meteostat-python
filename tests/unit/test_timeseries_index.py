"""
Test TimeSeries index behavior for single vs multiple stations

The code is licensed under the MIT license.
"""

import pandas as pd
from datetime import datetime
from meteostat.api.timeseries import TimeSeries
from meteostat.core.data import data_service
from meteostat.enumerations import Granularity
from meteostat.typing import Station


def test_single_station_no_station_index():
    """
    Test that single station DataFrame does not include station in index
    """
    # Create mock data with proper multi-index (station, time, source)
    dates = pd.date_range("2025-01-01", periods=3, freq="h")
    data = {"temp": [10, 11, 12], "rhum": [80, 81, 82]}

    df = pd.DataFrame(data, index=dates)
    df.index.name = "time"
    df["source"] = "test_provider"
    df = df.set_index("source", append=True)
    df = pd.concat([df], keys=["$0001"], names=["station"])

    station = Station(id="$0001", latitude=50.0, longitude=8.0, elevation=100)
    ts = TimeSeries(
        granularity=Granularity.HOURLY,
        stations=data_service._stations_to_df([station]),  # Single station, not provided as list
        df=df,
        start=datetime(2025, 1, 1),
        end=datetime(2025, 1, 1, 2),
        multi_station=False,  # Single station should not be multi_station
    )

    result = ts.fetch()

    assert "station" not in result.index.names
    assert "time" in result.index.names
    assert result.index.name == "time"
    assert len(result) == 3


def test_multiple_stations_keep_station_index():
    """
    Test that multiple stations DataFrame keeps station in index
    """
    # Create mock data for two stations
    dates = pd.date_range("2025-01-01", periods=3, freq="h")
    data = {"temp": [10, 11, 12], "rhum": [80, 81, 82]}

    df1 = pd.DataFrame(data, index=dates)
    df1.index.name = "time"
    df1["source"] = "test_provider"
    df1 = df1.set_index("source", append=True)

    df2 = pd.DataFrame(data, index=dates)
    df2.index.name = "time"
    df2["source"] = "test_provider"
    df2 = df2.set_index("source", append=True)

    df = pd.concat([df1, df2], keys=["$0001", "$0002"], names=["station"])

    station1 = Station(id="$0001", latitude=50.0, longitude=8.0, elevation=100)
    station2 = Station(id="$0002", latitude=51.0, longitude=9.0, elevation=200)

    ts = TimeSeries(
        granularity=Granularity.HOURLY,
        stations=data_service._stations_to_df(
            [station1, station2]
        ),  # Multiple stations or list input
        df=df,
        start=datetime(2025, 1, 1),
        end=datetime(2025, 1, 1, 2),
        multi_station=True,  # Multiple stations should be multi_station
    )

    result = ts.fetch()

    assert "station" in result.index.names
    assert "time" in result.index.names
    assert len(result) == 6


def test_single_station_list_keeps_station_index():
    """
    Test that single station provided as list keeps station in index
    """
    # Create mock data with proper multi-index (station, time, source)
    dates = pd.date_range("2025-01-01", periods=3, freq="h")
    data = {"temp": [10, 11, 12], "rhum": [80, 81, 82]}

    df = pd.DataFrame(data, index=dates)
    df.index.name = "time"
    df["source"] = "test_provider"
    df = df.set_index("source", append=True)
    df = pd.concat([df], keys=["$0001"], names=["station"])

    station = Station(id="$0001", latitude=50.0, longitude=8.0, elevation=100)
    ts = TimeSeries(
        granularity=Granularity.HOURLY,
        stations=data_service._stations_to_df([station]),  # Provided as list
        df=df,
        start=datetime(2025, 1, 1),
        end=datetime(2025, 1, 1, 2),
        multi_station=True,  # Provided as list should be multi_station
    )

    result = ts.fetch()

    assert "station" in result.index.names
    assert "time" in result.index.names
    assert len(result) == 3


def test_single_station_no_data():
    """
    Test that single station with no data returns None gracefully
    """
    station = Station(id="$0001", latitude=50.0, longitude=8.0, elevation=100)
    ts = TimeSeries(
        granularity=Granularity.HOURLY,
        stations=data_service._stations_to_df([station]),
        df=None,
        start=datetime(2025, 1, 1),
        end=datetime(2025, 1, 1, 2),
        multi_station=False,  # Single station should not be multi_station
    )

    result = ts.fetch()
    assert result is None
