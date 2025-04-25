"""
Stations Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from copy import copy
from datetime import datetime, timedelta
from typing import Union
import pandas as pd
from meteostat.core.cache import get_local_file_path, file_in_cache
from meteostat.core.loader import load_handler
from meteostat.interface.base import Base
from meteostat.utilities.helpers import get_distance


class Stations(Base):
    """
    Select weather stations from the full list of stations
    """

    # The cache subdirectory
    cache_subdir: str = "stations"

    # The list of selected weather Stations
    _data: pd.DataFrame = None

    # Raw data columns
    _columns: list = [
        "id",
        "name",
        "country",
        "region",
        "wmo",
        "icao",
        "latitude",
        "longitude",
        "elevation",
        "timezone",
        "hourly_start",
        "hourly_end",
        "daily_start",
        "daily_end",
        "monthly_start",
        "monthly_end",
    ]

    # Processed data columns with types
    _types: dict = {
        "id": "string",
        "name": "object",
        "country": "string",
        "region": "string",
        "wmo": "string",
        "icao": "string",
        "latitude": "float64",
        "longitude": "float64",
        "elevation": "float64",
        "timezone": "string",
    }

    # Columns for date parsing
    _parse_dates: list = [10, 11, 12, 13, 14, 15]

    def _load(self) -> None:
        """
        Load file from Meteostat
        """

        # File name
        file = "stations/slim.csv.gz"

        # Get local file path
        path = get_local_file_path(self.cache_dir, self.cache_subdir, file)

        # Check if file in cache
        if self.max_age > 0 and file_in_cache(path, self.max_age):
            # Read cached data
            df = pd.read_pickle(path)

        else:
            # Get data from Meteostat
            df = load_handler(
                self.endpoint,
                file,
                self.proxy,
                self._columns,
                self._types,
                self._parse_dates,
            )

            # Add index
            df = df.set_index("id")

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Set data
        self._data = df

    def __init__(self) -> None:
        # Get all weather stations
        self._load()

    def nearby(self, lat: float, lon: float, radius: int = None) -> "Stations":
        """
        Sort/filter weather stations by physical distance
        """

        # Create temporal instance
        temp = copy(self)

        # Get distance for each station
        temp._data["distance"] = get_distance(
            lat, lon, temp._data["latitude"], temp._data["longitude"]
        )

        # Filter by radius
        if radius:
            temp._data = temp._data[temp._data["distance"] <= radius]

        # Sort stations by distance
        temp._data.columns.str.strip()
        temp._data = temp._data.sort_values("distance")

        # Return self
        return temp

    def region(self, country: str, state: str = None) -> "Stations":
        """
        Filter weather stations by country/region code
        """

        # Create temporal instance
        temp = copy(self)

        # Country code
        temp._data = temp._data[temp._data["country"] == country]

        # State code
        if state is not None:
            temp._data = temp._data[temp._data["region"] == state]

        # Return self
        return temp

    def bounds(self, top_left: tuple, bottom_right: tuple) -> "Stations":
        """
        Filter weather stations by geographical bounds
        """

        # Create temporal instance
        temp = copy(self)

        # Return stations in boundaries
        temp._data = temp._data[
            (temp._data["latitude"] <= top_left[0])
            & (temp._data["latitude"] >= bottom_right[0])
            & (temp._data["longitude"] <= bottom_right[1])
            & (temp._data["longitude"] >= top_left[1])
        ]

        # Return self
        return temp

    def inventory(
        self, freq: str, required: Union[datetime, tuple, bool] = True
    ) -> "Stations":
        """
        Filter weather stations by inventory data
        """

        # Create temporal instance
        temp = copy(self)

        if required is True:
            # Make sure data exists at all
            temp._data = temp._data[~pd.isna(temp._data[f"{freq}_start"])]

        elif isinstance(required, tuple):
            # Make sure data exists across period
            temp._data = temp._data[
                (~pd.isna(temp._data[f"{freq}_start"]))
                & (temp._data[freq + "_start"] <= required[0])
                & (
                    temp._data[freq + "_end"] + timedelta(seconds=temp.max_age)
                    >= required[1]
                )
            ]

        else:
            # Make sure data exists on a certain day
            temp._data = temp._data[
                (~pd.isna(temp._data[f"{freq}_start"]))
                & (temp._data[freq + "_start"] <= required)
                & (
                    temp._data[freq + "_end"] + timedelta(seconds=temp.max_age)
                    >= required
                )
            ]

        return temp

    def convert(self, units: dict) -> "Stations":
        """
        Convert columns to a different unit
        """

        # Create temporal instance
        temp = copy(self)

        # Change data units
        for parameter, unit in units.items():
            if parameter in temp._data.columns.values:
                temp._data[parameter] = temp._data[parameter].apply(unit)

        # Return class instance
        return temp

    def count(self) -> int:
        """
        Return number of weather stations in current selection
        """

        return len(self._data.index)

    def fetch(self, limit: int = None, sample: bool = False) -> pd.DataFrame:
        """
        Fetch all weather stations or a (sampled) subset
        """

        # Copy DataFrame
        temp = copy(self._data)

        # Return limited number of sampled entries
        if sample and limit:
            return temp.sample(limit)

        # Return limited number of entries
        if limit:
            return temp.head(limit)

        # Return all entries
        return temp

    # Import additional methods
    from meteostat.core.cache import clear_cache
