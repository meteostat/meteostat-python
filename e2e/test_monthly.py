"""
E2E Test - Monthly Class

The code is licensed under the MIT license.
"""

import unittest
from datetime import datetime
from meteostat import Monthly


class TestMonthly(unittest.TestCase):

    """
    Monthly class tests
    """

    def test_normalize(self):
        """
        Test: normalize() method
        """

        # Get 2018 monthly data for Frankfurt Airport
        data = Monthly(
            ['10637'], start=datetime(
                2018, 1, 1), end=datetime(
                2018, 12, 31))
        count = data.normalize().count()

        # Check if count matches 12
        self.assertEqual(
            count,
            12,
            'Normalized daily data returns count of ' +
            str(count) +
            ', should be 12')

    def test_aggregate(self):
        """
        Test: aggregate() method
        """

        # Get 2018 monthly data for Frankfurt Airport
        data = Monthly(
            ['10637'], start=datetime(
                2018, 1, 1), end=datetime(
                2018, 12, 31))
        count = data.normalize().aggregate('1Y').count()

        # Check if count matches 53
        self.assertEqual(
            count,
            1,
            'Aggregated daily data returns count of ' +
            str(count) +
            ', should be 1')

    def test_coverage(self):
        """
        Test: coverage() method
        """

        # Get 2018 monthly data for Frankfurt Airport
        data = Monthly(
            ['10637'], start=datetime(
                2018, 1, 1), end=datetime(
                2018, 12, 31))
        coverage = data.normalize().coverage()

        # Check if coverage is 100%
        self.assertEqual(
            coverage,
            1,
            'Normalized daily data returns coverage of ' +
            str(coverage) +
            ', should be 1')


if __name__ == '__main__':
    unittest.main()
