from functools import cache
import pandas as pd
from meteostat.point import Point
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.utils.helpers import get_freq, get_distance
from meteostat.utils.mutations import apply_lapse_rate


def nearest(ts: TimeSeries, point: Point, lapse_rate=False) -> pd.DataFrame:
    """
    Get nearest value for each record
    """
    # Fetch filled DataFrame
    df = ts.fetch(fill=True)
    # Apply lapse rate
    if lapse_rate and point.elevation:
        # Add station elevation column
        @cache
        def _elevation(id: str) -> int:
            station = next(station for station in ts.stations if station["id"] == id)
            return station["location"]["elevation"]

        df["elevation"] = df.index.get_level_values("station").map(_elevation)
        # Adjust temperature data
        df = apply_lapse_rate(df, point.elevation)
        # Drop needless columns
        df.drop("elevation", axis=1, inplace=True)

    # Add distance column
    @cache
    def _distance(id: str) -> int:
        station = next(station for station in ts.stations if station["id"] == id)
        return get_distance(
            station["location"]["latitude"],
            station["location"]["longitude"],
            point.latitude,
            point.longitude,
        )

    df["distance"] = df.index.get_level_values("station").map(_distance)
    # Get frequency by granularity
    freq = get_freq(ts.granularity)
    # Group by time
    df = (
        df.sort_values("distance")
        .groupby(pd.Grouper(level="time", freq=freq))
        .agg("first")
    )
    # Drop needless columns
    df.drop("distance", axis=1, inplace=True)
    # Return interpolated DataFrame
    return df
