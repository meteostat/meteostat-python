"""
DataFrame Filters

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Set, Tuple, Union
import pandas as pd
from meteostat.enumerations import Parameter
from meteostat.typing import SequenceInput


def filter_time(
    df: pd.DataFrame,
    start: Union[datetime, None] = None,
    end: Union[datetime, None] = None,
) -> pd.DataFrame:
    """
    Filter time series data based on start and end date
    """

    # Get time index
    time = df.index.get_level_values("time")

    # Filter & return
    return df.loc[(time >= start) & (time <= end)] if start and end else df


def filter_parameters(
    df: pd.DataFrame, parameters: Tuple[Parameter, ...]
) -> pd.DataFrame:
    """
    Filter DataFrame based on requested parameters
    """
    # Remove obsolete columns
    [
        df.drop(col, axis=1, inplace=True) if col not in parameters else None
        for col in df.columns
    ]
    # Add missing columns
    for col in parameters:
        if col not in df:
            df[col] = None
    return df
