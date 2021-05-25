"""
Unit Tests - Stations Class

The code is licensed under the MIT license.
"""

import unittest
from datetime import datetime
from meteostat import Stations, units


class TestStations(unittest.TestCase):

    """
    Stations class tests
    """

    def test_nearby(self):
        """
        Test: Nearby stations
        """

        # Selecting closest weather station to Frankfurt Airport
        station = Stations().nearby(50.05, 8.6).fetch(1).to_dict('records')[0]

        # Check if country code matches Germany
        self.assertEqual(
            station['country'],
            'DE',
            f'Closest weather stations returns country code {station["country"]}, should be DE'
        )

    def test_id(self):
        """
        Test: Stations by identifier
        """

        # Select weather station 'Toronto Pearson Airport'
        station = Stations().id('wmo', '71624').fetch(1).to_dict('records')[0]

        # Check if ICAO ID matches CYYZ
        self.assertEqual(
            station['icao'],
            'CYYZ',
            f'Weather station returns ICAO ID {station["icao"]}, should be CYYZ')

    def test_region(self):
        """
        Test: Stations by country/region code
        """

        # Select a weather station in Ontario, Canada
        station = Stations().region('CA', 'ON').fetch(
            1).to_dict('records')[0]

        # Check if country code matches Canada
        self.assertEqual(
            station['country'],
            'CA',
            f'Weather station returns country code {station["country"]}, should be CA')

        # Check if region code matches Ontario
        self.assertEqual(
            station['region'],
            'ON',
            f'Weather station returns province code {station["region"]}, should be ON'
        )

    def test_bounds(self):
        """
        Test: Stations by geographical area
        """

        # Select weather stations in southern hemisphere
        station = Stations().bounds(
            (0, -180), (-90, 180)).fetch(1).to_dict('records')[0]

        # Check if -90 <= latitude <= 0
        self.assertTrue(
            -90 <= station['latitude'] <= 0,
            'Weather station is not in latitude range'
        )

    def test_inventory(self):
        """
        Test: Filter stations by inventory
        """

        # Select weather stations in Germany
        stations = Stations().region('DE')

        # Apply inventory filter
        stations = stations.inventory('daily', datetime(2020, 1, 1))

        # Get count
        count = stations.count()

        # Check if at least one station remains
        self.assertTrue(
            count > 0,
            'No remaining weather stations'
        )

    def test_convert(self):
        """
        Test: Convert distance to feet
        """

        # Get closest weather stations to Seattle, WA
        stations = Stations().nearby(47.6062, -122.3321)

        # Convert distance to feet
        stations = stations.convert({'distance': units.feet})

        # Get three closest weather stations
        stations = stations.fetch(3)

        # Check if three stations are returned
        self.assertEqual(
            len(stations.index),
            3,
            f'{len(stations.index)} weather stations returned, should be 3'
        )


if __name__ == '__main__':
    unittest.main()
