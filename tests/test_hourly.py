"""
Unit Tests - Hourly Class

The code is licensed under the MIT license.
"""

import unittest
from meteostat import Hourly
from datetime import datetime

class TestHourly(unittest.TestCase):

    def test_normalize(self):

        # Get data for some day at Frankfurt Airport
        data = Hourly(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 1, 1, 23, 59))
        count = data.normalize().count()

        # Check if count matches 24
        self.assertEqual(
            count,
            24,
            'Normalized hourly data returns count of ' + str(count) + ', should be 24'
        )

    def test_aggregate(self):

        # Get data for some days at Frankfurt Airport
        data = Hourly(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 1, 3, 23, 59))
        count = data.normalize().aggregate(freq = '1D').count()

        # Check if count matches 3
        self.assertEqual(
            count,
            3,
            'Aggregated hourly data returns count of ' + str(count) + ', should be 3'
        )

    def test_coverage(self):

        # Get data for some day at Frankfurt Airport
        data = Hourly(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 1, 1, 23, 59))
        coverage = data.normalize().coverage()

        # Check if coverage is 100%
        self.assertEqual(
            coverage,
            1,
            'Normalized hourly data returns coverage of ' + str(coverage) + ', should be 1'
        )

if __name__ == '__main__':
    unittest.main()
