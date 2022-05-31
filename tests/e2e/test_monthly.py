"""
E2E Test - Monthly Class

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Monthly


def test_normalize():
    """
    Test: normalize() method
    """

    # Get 2018 monthly data for Frankfurt Airport
    data = Monthly("72202", start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    count = data.normalize().count()

    # Check if count matches 12
    assert count == 12


def test_aggregate():
    """
    Test: aggregate() method
    """

    # Get 2018 monthly data for Frankfurt Airport
    data = Monthly("72202", start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    count = data.normalize().aggregate("1Y").count()

    # Check if count matches 1
    assert count == 1


def test_coverage():
    """
    Test: coverage() method
    """

    # Get 2018 monthly data for Frankfurt Airport
    data = Monthly("72202", start=datetime(2018, 1, 1), end=datetime(2018, 12, 31))
    coverage = data.normalize().coverage()

    # Check if coverage is 100%
    assert coverage == 1
