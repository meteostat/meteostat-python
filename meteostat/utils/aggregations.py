import numpy as np
import pandas as pd


def degree_mean(data: pd.Series) -> float:
    """
    Return the mean of a list of degrees
    """

    if data.isnull().all():
        return np.NaN

    rads = np.deg2rad(data)
    sums = np.arctan2(np.sum(np.sin(rads)), np.sum(np.cos(rads)))
    return (np.rad2deg(sums) + 360) % 360
