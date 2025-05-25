import pandas as pd

from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries


def nearest_neighbor(df: pd.DataFrame, ts: TimeSeries, _point: Point) -> pd.DataFrame:
    """
    Get nearest neighbor value for each record in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be adjusted.
    ts : TimeSeries
        TimeSeries object containing the target data.
    _point : Point
        Point object representing the target location.

    Returns
    -------
    pd.DataFrame
        DataFrame with nearest neighbor values for each record.
    """
    df = (
        df.sort_values("distance")
        .groupby(pd.Grouper(level="time", freq=ts.freq))
        .agg("first")
    )

    return df
