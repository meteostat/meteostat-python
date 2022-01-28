"""
E2E Test - Normals Class

The code is licensed under the MIT license.
"""

import unittest
from meteostat import Normals


class TestNormals(unittest.TestCase):

    """
    Normals class tests
    """

    def test_normals(self):
        """
        Test: Fetch climate normals
        """

        # Get normals for Frankfurt Airport
        data = Normals('10637', (1961, 1990))

        # Count rows
        count = data.count()

        # Check if count matches 48
        self.assertEqual(
            count,
            48,
            'Normals returns count of ' +
            str(count) +
            ', should be 48')


if __name__ == '__main__':
    unittest.main()
