"""
TimeSeries Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Optional, Union
import pandas as pd
from meteostat.core.cache import file_in_cache, get_local_file_path
from meteostat.core.loader import load_handler
from meteostat.enumerations.granularity import Granularity
from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.utilities.mutations import filter_time, localize
from meteostat.utilities.validations import validate_series
from meteostat.utilities.helpers import get_flag_from_source_factory, with_suffix
from meteostat.interface.point import Point
from meteostat.interface.meteodata import MeteoData


class TimeSeries(MeteoData):
    """
    TimeSeries class which provides features which are
    used across all time series classes
    """

    # Base URL of the Meteostat bulk data interface
    endpoint = "https://data.meteostat.net/"

    # The list of origin weather Stations
    _origin_stations: Optional[pd.Index] = None

    # The start date
    _start: Optional[datetime] = None

    # The end date
    _end: Optional[datetime] = None

    # Include model data?
    _model = True

    # Fetch source flags?
    _flags = False

    def _load_data(self, station: str, year: Optional[int] = None) -> None:
        """
        Load file for a single station from Meteostat
        """
        # File name
        file = generate_endpoint_path(self.granularity, station, year)

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
                default_df=pd.DataFrame(
                    columns=self._raw_columns
                    + with_suffix(self._raw_columns, "_source")
                ),
            )

            # Add time column and drop original columns
            if len(self._parse_dates) < 3:
                df["day"] = 1

            df["time"] = pd.to_datetime(
                df[
                    (
                        self._parse_dates
                        if len(self._parse_dates) > 2
                        else self._parse_dates + ["day"]
                    )
                ]
            )
            df = df.drop(self._parse_dates, axis=1)

            # Validate and prepare data for further processing
            df = validate_series(df, station)

            # Rename columns
            df = df.rename(columns=self._renamed_columns, errors="ignore")

            # Convert sources to flags
            for col in df.columns:
                basecol = col[:-7] if col.endswith("_source") else col

                if basecol not in self._processed_columns:
                    df.drop(col, axis=1, inplace=True)
                    continue

                if basecol == col:
                    df[col] = df[col].astype("Float64")

                if col.endswith("_source"):
                    flagcol = f"{basecol}_flag"
                    df[flagcol] = pd.NA
                    df[flagcol] = df[flagcol].astype("string")
                    mask = df[col].notna()
                    df.loc[mask, flagcol] = df.loc[mask, col].apply(
                        get_flag_from_source_factory(
                            self._source_mappings, self._model_flag
                        )
                    )
                    df.drop(col, axis=1, inplace=True)

            # Process virtual columns
            for key, value in self._virtual_columns.items():
                df = value(df, key)

            # Save as Pickle
            if self.max_age > 0:
                df.to_pickle(path)

        # Localize time column
        if (
            self.granularity == Granularity.HOURLY
            and self._timezone is not None
            and len(df.index) > 0
        ):
            df = localize(df, self._timezone)

        # Filter time period and append to DataFrame
        df = filter_time(df, self._start, self._end)

        # Return
        return df

    def _filter_model(self) -> None:
        """
        Remove model data from time series
        """

        for col_name in self._processed_columns:
            self._data.loc[
                (pd.isna(self._data[f"{col_name}_flag"]))
                | (self._data[f"{col_name}_flag"].str.contains(self._model_flag)),
                col_name,
            ] = pd.NA

        # Drop nan-only rows
        self._data.dropna(how="all", subset=self._processed_columns, inplace=True)

    def _init_time_series(
        self,
        loc: Union[pd.DataFrame, Point, list, str],  # Station(s) or geo point
        start: datetime = None,
        end: datetime = None,
        model=True,  # Include model data?
        flags=False,  # Load source flags?
    ) -> None:
        """
        Common initialization for all time series, regardless
        of its granularity
        """

        # Set list of weather stations based on user
        # input or retrieve list of stations programatically
        # if location is a geographical point
        if isinstance(loc, pd.DataFrame):
            self._stations = loc.index
        elif isinstance(loc, Point):
            stations = loc.get_stations("daily", start, end, model)
            self._stations = stations.index
        else:
            if not isinstance(loc, list):
                loc = [loc]
            self._stations = pd.Index(loc)

        # Preserve settings
        self._start = start if self._start is None else self._start
        self._end = end if self._end is None else self._end
        self._model = model
        self._flags = flags

        # Get data for all weather stations
        self._data = self._get_data()

        # Fill columns if they don't exist
        for col in self._processed_columns:
            if col not in self._data.columns:
                self._data[col] = pd.NA
                self._data[col] = self._data[col].astype("Float64")
                self._data[f"{col}_flag"] = pd.NA
                self._data[f"{col}_flag"] = self._data[f"{col}_flag"].astype("string")

        # Reorder the DataFrame
        self._data = self._data[
            self._processed_columns + with_suffix(self._processed_columns, "_flag")
        ]

        # Remove model data from DataFrame
        if not model:
            self._filter_model()

        # Conditionally, remove flags from DataFrame
        if not self._flags:
            self._data.drop(
                with_suffix(self._processed_columns, "_flag"),
                axis=1,
                errors="ignore",
                inplace=True,
            )

        # Interpolate data spatially if requested
        # location is a geographical point
        if isinstance(loc, Point):
            self._resolve_point(loc.method, stations, loc.alt, loc.adapt_temp)

        # Clear cache if auto cleaning is enabled
        if self.max_age > 0 and self.autoclean:
            self.clear_cache()

    # Import methods
    from meteostat.series.normalize import normalize
    from meteostat.series.interpolate import interpolate
    from meteostat.series.aggregate import aggregate
    from meteostat.series.convert import convert
    from meteostat.series.coverage import coverage
    from meteostat.series.count import count
    from meteostat.series.fetch import fetch
    from meteostat.series.stations import stations
    from meteostat.core.cache import clear_cache
