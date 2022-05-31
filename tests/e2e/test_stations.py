"""
E2E Test - Stations Class

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Stations, units


def test_nearby():
    """
    Test: Nearby stations
    """

    # Selecting closest weather station to Frankfurt Airport
    station = Stations().nearby(50.05, 8.6).fetch(1).to_dict("records")[0]

    # Check if country code matches Germany
    assert station["country"] == "DE"


def test_region():
    """
    Test: Stations by country/region code
    """

    # Select a weather station in Ontario, Canada
    station = Stations().region("CA", "ON").fetch(1).to_dict("records")[0]

    # Check if country code matches Canada
    assert station["country"] == "CA"

    # Check if region code matches Ontario
    assert station["region"] == "ON"


def test_bounds():
    """
    Test: Stations by geographical area
    """

    # Select weather stations in southern hemisphere
    station = Stations().bounds((0, -180), (-90, 180)).fetch(1).to_dict("records")[0]

    # Check if -90 <= latitude <= 0
    assert -90 <= station["latitude"] <= 0


def test_inventory():
    """
    Test: Filter stations by inventory
    """

    # Select weather stations in Germany
    stations = Stations().region("DE")

    # Apply inventory filter
    stations = stations.inventory("daily", datetime(2020, 1, 1))

    # Get count
    count = stations.count()

    # Check if at least one station remains
    assert count > 0


def test_convert():
    """
    Test: Convert distance to feet
    """

    # Get closest weather stations to Seattle, WA
    stations = Stations().nearby(47.6062, -122.3321)

    # Convert distance to feet
    stations = stations.convert({"distance": units.feet})

    # Get three closest weather stations
    stations = stations.fetch(3)

    # Check if three stations are returned
    assert len(stations.index) == 3
