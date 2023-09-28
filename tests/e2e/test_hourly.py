"""
E2E Test - Hourly Class

The code is licensed under the MIT license.
"""

from datetime import datetime, timedelta
from meteostat import Hourly


def test_model_disabled():
    """
    Test request with disabled model data
    """

    today = datetime.today()
    start = today + timedelta(days=2)
    end = today + timedelta(days=3)
    data = Hourly("10637", start, end, model=False)

    assert data.count() == 0


def test_normalize():
    """
    Test: normalize() method
    """

    # Get data for some day at Frankfurt Airport
    data = Hourly(
        ["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 1, 1, 23, 59)
    )
    count = data.normalize().count()

    # Check if count matches 24
    assert count == 24


def test_aggregate():
    """
    Test: aggregate() method
    """

    # Get data for some days at Frankfurt Airport
    data = Hourly(
        ["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 1, 3, 23, 59)
    )
    count = data.normalize().aggregate("1D").count()

    # Check if count matches 3
    assert count == 3


def test_interpolate():
    """
    Test: interpolate() method
    """

    # Get data for one day at Frankfurt Airport
    data = Hourly(
        ["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 1, 1, 23, 59)
    )
    count = data.normalize().interpolate().count()

    # Check if count matches 24
    assert count == 24


def test_coverage():
    """
    Test: coverage() method
    """

    # Get data for some day at Frankfurt Airport
    data = Hourly(
        ["10637"], start=datetime(2018, 1, 1), end=datetime(2018, 1, 1, 23, 59)
    )
    coverage = data.normalize().coverage()

    # Check if coverage is 100%
    assert coverage == 1
