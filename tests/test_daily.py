"""
Unit Tests - Daily Class

The code is licensed under the MIT license.
"""

import unittest
from meteostat import Daily
from datetime import datetime

class TestDaily(unittest.TestCase):

    def test_normalize(self):

        # Get 2018 daily data for Frankfurt Airport
        data = Daily(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
        count = data.normalize().count()

        # Check if count matches 365
        self.assertEqual(
            count,
            365,
            'Normalized daily data returns count of ' + str(count) + ', should be 365'
        )

    def test_aggregate(self):

        # Get 2018 daily data for Frankfurt Airport
        data = Daily(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
        count = data.normalize().aggregate(freq = '1W').count()

        # Check if count matches 53
        self.assertEqual(
            count,
            53,
            'Aggregated daily data returns count of ' + str(count) + ', should be 53'
        )

    def test_coverage(self):

        # Get 2018 daily data for Frankfurt Airport
        data = Daily(['10637'], start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
        coverage = data.normalize().coverage()

        # Check if coverage is 100%
        self.assertEqual(
            coverage,
            1,
            'Normalized daily data returns coverage of ' + str(coverage) + ', should be 1'
        )

if __name__ == '__main__':
    unittest.main()
