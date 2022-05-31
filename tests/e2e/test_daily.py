"""
E2E Test - Daily Class

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Daily


def test_flags():
    """
    Test request with flags
    """

    # Get 2018 daily data for Frankfurt Airport
    df = Daily(
        ["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 12, 31), flags=True
    ).fetch()

    assert len(df.columns) == 20


def test_normalize():
    """
    Test: normalize() method
    """

    # Get 2018 daily data for Frankfurt Airport
    data = Daily(["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    count = data.normalize().count()

    # Check if count matches 365
    assert count == 365


def test_aggregate():
    """
    Test: aggregate() method
    """

    # Get 2018 daily data for Frankfurt Airport
    data = Daily(["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    count = data.normalize().aggregate("1W").count()

    # Check if count matches 53
    assert count == 53


def test_coverage():
    """
    Test: coverage() method
    """

    # Get 2018 daily data for Frankfurt Airport
    data = Daily(["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    coverage = data.normalize().coverage()

    # Check if coverage is 100%
    assert coverage == 1
