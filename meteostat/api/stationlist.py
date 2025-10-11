from typing import List

import pandas as pd

from meteostat.typing import AbstractStation, Station


class StationList:
    """
    A list of stations.

    This class is used to represent a list of stations, which can be filtered by various parameters.
    """

    _stations: List[Station | AbstractStation]
    _validated = False  # Indicates whether the station list has been validated

    def __init__(self, stations: List[Station | AbstractStation]):
        self._stations = stations

    def fetch(self) -> List[Station]:
        """
        Fetch the list of stations.

        Returns:
            List[Station]: A list of Station objects.
        """
        return self._stations

    def count(self) -> int:
        """
        Get the number of stations in the list.

        Returns:
            int: The number of stations.
        """
        return len(self._stations)

    def df(self) -> pd.DataFrame:
        """
        Get included weather stations as DataFrame
        """
        return (
            pd.DataFrame.from_records(
                [
                    {
                        "id": station.id,
                        "name": station.name,
                        "country": station.country,
                        "latitude": station.latitude,
                        "longitude": station.longitude,
                        "elevation": station.elevation,
                        "timezone": station.timezone,
                    }
                    for station in self.fetch()
                ],
                index="id",
            )
            if self.count()
            else []
        )
