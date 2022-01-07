"""
Endpoint Utility Tests

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.enumerations.granularity import Granularity


def test_generate_endpoint_path_normals():
    """
    Generate endpoint path for climate normals
    """

    assert "normals/10286.csv.gz" == generate_endpoint_path(
        Granularity.NORMALS,
        '10286'
    )


def test_generate_endpoint_path_hourly_full():
    """
    Generate endpoint path for full hourly data
    """

    assert "hourly/full/10286.csv.gz" == generate_endpoint_path(
        Granularity.HOURLY,
        '10286',
        True
    )


def test_generate_endpoint_path_hourly_full_obs():
    """
    Generate endpoint path for hourly observation data
    """

    assert "hourly/obs/10286.csv.gz" == generate_endpoint_path(
        Granularity.HOURLY,
        '10286',
        False
    )


def test_generate_endpoint_path_hourly_subset():
    """
    Generate endpoint path for hourly chunk
    """

    assert "hourly/full/2021/10286.csv.gz" == generate_endpoint_path(
        Granularity.HOURLY,
        '10286',
        True,
        2021
    )


def test_generate_endpoint_path_daily_subset():
    """
    Generate endpoint path for full daily data
    """

    assert 'daily/full/10286.csv.gz' == generate_endpoint_path(
        Granularity.DAILY,
        '10286',
        True
    )


def test_generate_endpoint_path_monthly_subset():
    """
    Generate endpoint path for full monthly data
    """

    assert 'monthly/full/10286.csv.gz' == generate_endpoint_path(
        Granularity.MONTHLY,
        '10286',
        True
    )
