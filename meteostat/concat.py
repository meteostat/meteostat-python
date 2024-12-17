from copy import copy
from datetime import datetime
from typing import List, Optional

import pandas as pd
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.typing import ProviderDict

def _append_provider(items: List[ProviderDict], new_item: ProviderDict) -> None:
    if not any(item['id'] == new_item['id'] for item in items):
        items.append(new_item)

def _get_dt(dt_a: Optional[datetime], dt_b: Optional[datetime], start = True) -> Optional[datetime]:
    """
    Return the earlier or later (depending on "start" argument) of two datetimes,
    considering None as 'no value'.

    If both are None, return None.
    """
    if dt_a is None:
        return dt_b
    if dt_b is None:
        return dt_a
    return min(dt_a, dt_b) if start else max(dt_a, dt_b)

def concat(objs: List[TimeSeries]) -> TimeSeries:
    """
    Merge one or multiple Meteostat time series into a common one
    """
    ts_base = objs[0]

    if not all(
        obj.granularity == ts_base.granularity
        and obj.timezone == ts_base.timezone
        for obj in objs[1:]
    ):
        raise ValueError(
            "Can't concatenate time series objects with divergent granularity or time zone"
        )
    
    df = copy(ts_base._df)
    stations = copy(ts_base.stations)
    providers = copy(ts_base.providers)
    start = copy(ts_base.start)
    end = copy(ts_base.end)

    for obj in objs[1:]:
        df = pd.concat([df, obj._df], verify_integrity=True)
        stations = pd.concat([stations, obj.stations]).drop_duplicates()
        start = _get_dt(start, obj.start)
        end = _get_dt(end, obj.end, False)
        for provider in obj.providers:
            _append_provider(providers, provider)

    return TimeSeries(
        ts_base.granularity,
        ts_base.schema,
        providers,
        stations,
        df,
        start,
        end,
        ts_base.timezone
    )
