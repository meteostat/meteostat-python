from copy import copy
from typing import List

import pandas as pd
from meteostat.timeseries.timeseries import TimeSeries


def concat(objs: List[TimeSeries]) -> TimeSeries:
    """
    Merge one or multiple Meteostat time series into a common one
    """
    ts = copy(objs[0])

    if not all(
        obj.granularity == ts.granularity
        and obj.start == ts.start
        and obj.end == ts.end
        and obj.timezone == ts.timezone
        for obj in objs[1:]
    ):
        raise ValueError(
            "Can't concatenate time series objects with divergent granularity, start, end or timezone"
        )

    for obj in objs[1:]:
        ts._df = pd.concat([ts._df, obj._df], verify_integrity=True)
        ts.stations = pd.concat([ts.stations, obj.stations]).drop_duplicates()

    return ts
