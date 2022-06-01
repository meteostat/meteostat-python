"""
Cache Tests

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from meteostat.core.cache import get_local_file_path


EXPECTED_FILE_PATH = "cache/hourly/6dfc35c47756e962ef055d1049f1f8ec"


def test_get_local_file_path():
    """
    Test local file path
    """

    assert get_local_file_path("cache", "hourly", "10101") == EXPECTED_FILE_PATH


def test_get_local_file_path_chunked():
    """
    Test local file path II
    """

    assert get_local_file_path("cache", "hourly", "10101_2022") != EXPECTED_FILE_PATH
