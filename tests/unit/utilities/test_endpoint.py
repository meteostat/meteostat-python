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

    assert (
        generate_endpoint_path(Granularity.NORMALS, "10286") == "normals/10286.csv.gz"
    )


def test_generate_endpoint_path_hourly():
    """
    Generate endpoint path for hourly data
    """

    assert generate_endpoint_path(Granularity.HOURLY, "10286") == "hourly/10286.csv.gz"


def test_generate_endpoint_path_hourly_map():
    """
    Generate endpoint path for hourly observation data
    """

    assert (
        generate_endpoint_path(Granularity.HOURLY, "10286", None, True)
        == "hourly/10286.map.csv.gz"
    )


def test_generate_endpoint_path_hourly_chunk():
    """
    Generate endpoint path for hourly chunk
    """

    assert (
        generate_endpoint_path(Granularity.HOURLY, "10286", 2021)
        == "hourly/2021/10286.csv.gz"
    )


def test_generate_endpoint_path_daily():
    """
    Generate endpoint path for daily data
    """

    assert generate_endpoint_path(Granularity.DAILY, "10286") == "daily/10286.csv.gz"


def test_generate_endpoint_path_monthly():
    """
    Generate endpoint path for monthly data
    """

    assert (
        generate_endpoint_path(Granularity.MONTHLY, "10286") == "monthly/10286.csv.gz"
    )
