import numpy as np
import pandas as pd

from meteostat.core.config import config
from meteostat.enumerations import Parameter


def apply_lapse_rate(
    df: pd.DataFrame, elevation: int, lapse_rate: float
) -> pd.DataFrame:
    """
    Calculate approximate temperature at target elevation
    using a given lapse rate.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be adjusted.
    elevation : int
        Target elevation in meters.
    lapse_rate : float
        Lapse rate (temperature gradient) in degrees Celsius per kilometer.

    Returns
    -------
    pd.DataFrame
        DataFrame with adjusted temperature values.
    """
    columns = config.get(
        "interpolation.lapse_rate.cols",
        [
            Parameter.TEMP,
            Parameter.TMIN,
            Parameter.TMAX,
        ],
    )

    for col in columns:
        if col in df.columns:
            df.loc[df[col] != np.nan, col] = round(
                df[col] + ((lapse_rate / 1000) * (df["elevation"] - elevation)), 1
            )

    return df
