from functools import cache
import pandas as pd
from meteostat.point import Point
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.utils.helpers import get_freq, stations_to_df, get_distance
from meteostat.utils.mutations import apply_lapse_rate


def idw(ts: TimeSeries, point: Point, lapse_rate=False) -> pd.DataFrame:
    """
    Interpolate a time series using random forest regression (RFR)
    """
    # Fetch filled DataFrame
    df = ts.fetch(fill=True)
    # Get DataFrame of weather stations
    stations = stations_to_df(ts.stations)
    df = df.join(stations, on="station")
    print(df)
    exit()
