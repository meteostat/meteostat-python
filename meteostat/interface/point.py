"""
Point Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
import pandas as pd
from meteostat.interface.stations import Stations


class Point:
    """
    Automatically select weather stations by geographic location
    """

    # The interpolation method (weighted or nearest)
    method: str = "nearest"

    # Maximum radius for nearby stations
    radius: int = 35000

    # Maximum difference in altitude
    alt_range: int = 350

    # Maximum number of stations
    max_count: int = 4

    # Adapt temperature data based on altitude
    adapt_temp: bool = True

    # Distance Weight
    weight_dist: float = 0.6

    # Altitude Weight
    weight_alt: float = 0.4

    # The list of weather stations
    _stations: pd.Index = None

    # The latitude
    _lat: float = None

    # The longitude
    _lon: float = None

    # The altitude
    _alt: int = None

    def __init__(self, lat: float, lon: float, alt: int = None) -> None:
        self._lat = lat
        self._lon = lon
        self._alt = alt

        if alt is None:
            self.adapt_temp = False

    def get_stations(
        self,
        freq: str = None,
        start: datetime = None,
        end: datetime = None,
        model: bool = True,
    ) -> pd.DataFrame:
        """
        Get list of nearby weather stations
        """

        # Get nearby weather stations
        stations = Stations()
        stations = stations.nearby(self._lat, self._lon, self.radius)

        # Guess altitude if not set
        if self._alt is None:
            self._alt = stations.fetch().head(self.max_count)["elevation"].mean()

        # Captue unfiltered weather stations
        unfiltered = stations.fetch()
        if self.alt_range:
            unfiltered = unfiltered[
                abs(self._alt - unfiltered["elevation"]) <= self.alt_range
            ]

        # Apply inventory filter
        if freq and start and end:
            age = (datetime.now() - end).days
            if model is False or age > 180:
                stations = stations.inventory(freq, (start, end))

        # Apply altitude filter
        stations = stations.fetch()
        if self.alt_range:
            stations = stations[
                abs(self._alt - stations["elevation"]) <= self.alt_range
            ]

        # Fill up stations
        selected: int = len(stations.index)
        if selected < self.max_count:
            # Remove already included stations from unfiltered
            unfiltered = unfiltered.loc[~unfiltered.index.isin(stations.index)]
            # Append to existing DataFrame
            stations = pd.concat((stations, unfiltered.head(self.max_count - selected)))

        # Score values
        if self.radius:
            # Calculate score values
            stations["score"] = (
                (1 - (stations["distance"] / self.radius)) * self.weight_dist
            ) + (
                (1 - (abs(self._alt - stations["elevation"]) / self.alt_range))
                * self.weight_alt
            )

            # Sort by score (descending)
            stations = stations.sort_values("score", ascending=False)

        # Capture result
        self._stations = stations.index[: self.max_count]

        return stations.head(self.max_count)

    @property
    def alt(self) -> int:
        """
        Returns the point's altitude
        """

        # Return altitude
        return self._alt

    @property
    def stations(self) -> pd.Index:
        """
        Returns the point's weather stations
        """

        # Return weather stations
        return self._stations
