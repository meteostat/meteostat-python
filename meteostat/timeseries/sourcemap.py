"""
SourceMap Class

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution
4.0 International Public License.

The code is licensed under the MIT license.
"""
from copy import copy
from typing import Optional
import pandas as pd
from meteostat.utils.helpers import get_index, get_provider_priority


class SourceMap:
    """
    Access the data sources of a Meteostat time series
    """

    _df: Optional[pd.DataFrame] = None

    def __init__(
        self,
        df: Optional[pd.DataFrame],
    ) -> None:
        if not df.empty:
            self._df = df

    def fetch(self) -> Optional[pd.DataFrame]:
        """
        Get a DataFrame of squashed source strings
        """
        if self._df is None:
            return None

        df = copy(self._df)

        df["source_prio"] = df.index.get_level_values("source").map(
            get_provider_priority
        )

        df = (
            df.sort_values(by="source_prio", ascending=False)
            .groupby(["station", "time"])
            .agg(lambda s: get_index(pd.Series.first_valid_index(s), 2))
            .drop("source_prio", axis=1)
            .convert_dtypes()
        )

        return df
