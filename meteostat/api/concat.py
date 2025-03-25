from copy import copy
from datetime import datetime
from typing import List, Optional

from meteostat.core.data import data_service
from meteostat.core.schema import schema_service
from meteostat.api.timeseries import TimeSeries


def _get_dt(
    dt_a: Optional[datetime], dt_b: Optional[datetime], start=True
) -> Optional[datetime]:
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
    ts = objs[0]

    if not all(
        obj.granularity == ts.granularity and obj.timezone == ts.timezone
        for obj in objs[1:]
    ):
        raise ValueError(
            "Can't concatenate time series objects with divergent granularity or time zone"
        )

    stations = copy(ts.stations)
    start = copy(ts.start)
    end = copy(ts.end)
    parameters = ts.parameters

    for obj in objs[1:]:
        stations.extend(obj.stations)
        start = _get_dt(start, obj.start)
        end = _get_dt(end, obj.end, False)
        parameters.extend(obj.parameters)

    df = data_service.concat_fragments(
        [obj._df for obj in objs], ts.granularity, list(dict.fromkeys(parameters))
    )
    df = schema_service.format(df, ts.granularity)

    return TimeSeries(
        ts.granularity,
        stations,
        df,
        start,
        end,
        ts.timezone,
    )
