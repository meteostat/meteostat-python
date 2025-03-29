from functools import cache
import pandas as pd
from meteostat.api.point import Point
from meteostat.api.timeseries import TimeSeries
from meteostat.utils.helpers import get_freq, stations_to_df, get_distance
from meteostat.utils.mutations import apply_lapse_rate


def idw(ts: TimeSeries, point: Point, lapse_rate=False) -> pd.DataFrame:
    """
    Interpolate a time series using random forest regression (RFR)
    """
    # Fetch filled DataFrame
    df = ts.fetch(fill=True)
    # Return if DataFrame is missing
    if df is None:
        return None
    # Get DataFrame of weather stations
    stations = stations_to_df(ts.stations)
    df = df.join(stations, on="station")
    print(df)
    exit()
