from functools import cache
import pandas as pd
from meteostat.point import Point
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.utils.helpers import get_freq, stations_to_df, get_distance
from meteostat.utils.mutations import apply_lapse_rate


def idw(ts: TimeSeries, point: Point, lapse_rate=False) -> pd.DataFrame:
    """
    Interpolate a time series using Inverse Distance Weighted (IDW)
    """
    # Fetch filled DataFrame
    df = ts.fetch(fill=True)
    df = df.join(ts.stations, on="station")
    print(df)
    exit()
