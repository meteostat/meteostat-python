from copy import copy
import pandas as pd
from meteostat.timeseries.timeseries import TimeSeries


def concat(objs: list[TimeSeries]) -> TimeSeries:
    """
    Concatenate multiple Meteostat time series
    """
    if not all(
        obj.granularity == objs[0].granularity
        and obj.start == objs[0].start
        and obj.end == objs[0].end
        and obj.timezone == objs[0].timezone
        for obj in objs
    ):
        raise ValueError(
            "Can't concatenate time series objects with divergent granularity, start, end or timezone"
        )

    ts = copy(objs[0])

    for obj in objs:
        ts._df = pd.concat([ts._df, obj._df], verify_integrity=True)
        ts.stations = pd.concat([ts.stations, obj.stations])

    ts.stations = ts.stations.drop_duplicates()

    return ts
