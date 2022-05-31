"""
Utilities - Validations

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import pandas as pd


def validate_series(df: pd.DataFrame, station: str) -> pd.DataFrame:
    """
    Make sure a series is formatted correctly
    """

    # Add missing column(s)
    if "time" not in df.columns:
        df["time"] = None

    # Add weather station ID
    df["station"] = station

    # Set index
    df = df.set_index(["station", "time"])

    # Return DataFrame
    return df
