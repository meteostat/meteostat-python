"""
DataFrame Filters

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from typing import Iterator, List, Optional, TypeGuard, Union
import pandas as pd
from meteostat.enumerations import Granularity, Parameter, Provider
from meteostat.typing import ProviderSpec


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
    try:
        return df.loc[(time >= start) & (time <= end)] if start and end else df
    except TypeError:
        return (
            df.loc[(time >= start.date()) & (time <= end.date())]
            if start and end
            else df
        )


def filter_parameters(df: pd.DataFrame, parameters: List[Parameter]) -> pd.DataFrame:
    """
    Filter DataFrame based on requested parameters
    """
    # Remove obsolete columns
    for col in df.columns:
        if col not in parameters:
            df.drop(col, axis=1, inplace=True)
    # Add missing columns
    for col in parameters:
        if col not in df:
            df[col] = None
    return df


def filter_providers(
    granularity: Granularity,
    parameters: List[Parameter],
    providers: Iterator[ProviderSpec],
    country: str,
    start: Optional[datetime],
    end: Optional[datetime],
) -> Iterator[ProviderSpec]:
    """
    Get a filtered list of providers
    """

    def _filter(provider: ProviderSpec) -> TypeGuard[Provider]:
        if provider.granularity is not granularity:
            return False
        if set(provider.parameters).isdisjoint(parameters):
            return False
        if provider.countries and country not in provider.countries:
            return False
        if end and end < datetime.combine(provider.start, datetime.min.time()):
            return False
        if (
            provider.end is not None
            and start is not None
            and start > datetime.combine(provider.end, datetime.max.time())
        ):
            return False
        return True

    return filter(_filter, providers)
