"""
E2E Test - Point Class

The code is licensed under the MIT license.
"""

import unittest
from datetime import datetime
from meteostat import Point


class TestPoint(unittest.TestCase):

    """
    Point class tests
    """

    def test_point(self):
        """
        Test: Point Data
        """

        # Create Point for Vancouver, BC
        point = Point(49.2497, -123.1193, 70)

        # Get count of weather stations
        stations = point.get_stations(
            'daily', datetime(
                2020, 1, 1), datetime(
                2020, 1, 31))

        # Check if three stations are returned
        self.assertEqual(
            len(stations.index),
            4,
            f'{len(stations.index)} weather stations returned, should be 4'
        )


if __name__ == '__main__':
    unittest.main()
