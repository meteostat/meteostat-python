"""
Meteorological Data Class

A parent class for both time series and
climate normals data

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from collections.abc import Callable
from typing import Dict, List, Union
import pandas as pd
from meteostat.enumerations.granularity import Granularity
from meteostat.core.loader import processing_handler
from meteostat.utilities.mutations import adjust_temp
from meteostat.utilities.aggregations import weighted_average
from meteostat.interface.base import Base


class MeteoData(Base):
    """
    A parent class for both time series and
    climate normals data
    """

    # The list of weather Stations
    _stations: Union[pd.Index, None] = None

    # The data frame
    _data: pd.DataFrame = pd.DataFrame()

    @property
    def _raw_columns(self) -> List[str]:
        """
        Get the list of raw data columns, excluding any dicts with callable values
        """
        return [
            list(col.values())[0] if isinstance(col, dict) else col
            for col in self._columns
            if not (
                isinstance(col, dict)
                and (
                    isinstance(list(col.values())[0], Callable)
                    or list(col.values())[0] is None
                )
            )
        ]

    @property
    def _processed_columns(self) -> List[str]:
        """
        Get the list of processed data columns, excluding any dicts with callable values
        """
        return [
            list(col.keys())[0] if isinstance(col, dict) else col
            for col in self._columns[self._first_met_col :]
        ]

    @property
    def _renamed_columns(self) -> Dict[str, str]:
        """
        Get the dict of renamed data columns, including `_source` suffixes
        """
        return {
            new_key: new_val
            for d in self._columns
            if isinstance(d, dict)
            for k, v in d.items()
            if not isinstance(v, Callable)
            for new_key, new_val in ((v, k), (f"{v}_source", f"{k}_source"))
        }

    @property
    def _virtual_columns(self) -> Dict[str, str]:
        """
        Get the dict of virtual data columns
        """
        return {
            k: v
            for d in self._columns
            if isinstance(d, dict)
            for k, v in d.items()
            if isinstance(v, Callable)
        }

    def _get_datasets(self) -> list:
        """
        Get list of datasets
        """

        if self.granularity in (Granularity.HOURLY, Granularity.DAILY):
            datasets = [
                (str(station), year)
                for station in self._stations
                for year in self._annual_steps
            ]
        else:
            datasets = [(str(station),) for station in self._stations]

        return datasets

    def _get_data(self) -> None:
        """
        Get all required data dumps
        """

        if len(self._stations) > 0:
            # Get list of datasets
            datasets = self._get_datasets()

            # Data Processings
            return processing_handler(
                datasets, self._load_data, self.processes, self.threads
            )

        # Empty DataFrame
        return pd.DataFrame(columns=[*self._types])

    # pylint: disable=too-many-branches
    def _resolve_point(
        self, method: str, stations: pd.DataFrame, alt: int, adapt_temp: bool
    ) -> None:
        """
        Project weather station data onto a single point
        """

        if self._stations.size == 0 or self._data.size == 0:
            return

        if method == "nearest":
            if adapt_temp:
                # Join elevation of involved weather stations
                data = self._data.join(stations["elevation"], on="station")

                # Adapt temperature-like data based on altitude
                data = adjust_temp(data, alt)

                # Drop elevation & round
                data = data.drop("elevation", axis=1).round(1)

            else:
                data = self._data

            if self.granularity == Granularity.NORMALS:
                self._data = data.groupby(level=["start", "end", "month"]).agg("first")

            else:
                self._data = data.groupby(
                    pd.Grouper(level="time", freq=self._freq)
                ).agg("first")

        else:
            # Join score and elevation of involved weather stations
            data = self._data.join(stations[["score", "elevation"]], on="station")

            # Adapt temperature-like data based on altitude
            if adapt_temp:
                data = adjust_temp(data, alt)

            # Exclude non-mean data & perform aggregation
            if not self.granularity == Granularity.NORMALS:
                excluded = data["wdir"]
                excluded = excluded.groupby(
                    pd.Grouper(level="time", freq=self._freq)
                ).agg("first")

            # Aggregate mean data
            if self.granularity == Granularity.NORMALS:
                data = data.groupby(level=["start", "end", "month"]).apply(
                    weighted_average
                )

                # Remove obsolete index column
                try:
                    data = data.reset_index(level=3, drop=True)
                except IndexError:
                    pass

            else:
                data = data.groupby(pd.Grouper(level="time", freq=self._freq)).apply(
                    weighted_average
                )

                # Drop RangeIndex
                data.index = data.index.droplevel(1)

                # Merge excluded fields
                data["wdir"] = excluded

            # Drop score and elevation
            self._data = data.drop(["score", "elevation"], axis=1).round(1)

        # Set placeholder station ID
        self._data["station"] = "XXXXX"

        # Set index
        if self.granularity == Granularity.NORMALS:
            self._data = self._data.set_index("station", append=True)
            self._data = self._data.reorder_levels(["station", "start", "end", "month"])
        else:
            self._data = self._data.set_index(
                ["station", self._data.index.get_level_values("time")]
            )

        # Set station index
        self._stations = pd.Index(["XXXXX"])
