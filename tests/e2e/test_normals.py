"""
E2E Test - Normals Class

The code is licensed under the MIT license.
"""

from meteostat import Normals


def test_normals():
    """
    Test: Fetch climate normals
    """

    # Get normals for Frankfurt Airport
    data = Normals("10637", 1961, 1990)

    # Count rows
    count = data.count()

    # Check if count matches 12
    assert count == 12
