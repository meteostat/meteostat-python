"""
Utilities - Aggregation Methods

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

import numpy as np
import pandas as pd


def weighted_average(step: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weighted average from grouped data
    """

    data = np.ma.masked_array(step, np.isnan(step))
    data = np.ma.average(data, axis=0, weights=data[:, -2])
    data = data.filled(np.nan)

    return pd.DataFrame(data=[data], columns=step.columns)


def degree_mean(data: pd.Series) -> float:
    """
    Return the mean of a list of degrees
    """

    if data.isnull().all():
        return np.nan

    rads = np.deg2rad(data)
    sums = np.arctan2(np.sum(np.sin(rads)), np.sum(np.cos(rads)))
    return (np.rad2deg(sums) + 360) % 360
