from copy import copy
from datetime import datetime
from typing import List, Optional

import pandas as pd
from pulire import Schema
from meteostat import schema as schemas
from meteostat.enumerations import Granularity, Parameter
from meteostat.fetcher import concat_fragments
from meteostat.timeseries.timeseries import TimeSeries
from meteostat.typing import ProviderDict
from meteostat.utils.parsers import get_schema


def _get_schema(granularity: Granularity, parameters: List[Parameter]) -> Schema:
    root_schema = getattr(schemas, f"{granularity.upper()}_SCHEMA")
    return get_schema(root_schema, parameters)


def _append_parameter(items: List[Parameter], new_item: Parameter) -> None:
    if not any(item == new_item for item in items):
        items.append(new_item)


def _append_provider(items: List[ProviderDict], new_item: ProviderDict) -> None:
    if not any(item["id"] == new_item["id"] for item in items):
        items.append(new_item)


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

    parameters = ts.schema.names
    stations = copy(ts.stations)
    providers = copy(ts.providers)
    start = copy(ts.start)
    end = copy(ts.end)

    for obj in objs[1:]:
        stations = pd.concat([stations, obj.stations]).drop_duplicates()
        start = _get_dt(start, obj.start)
        end = _get_dt(end, obj.end, False)
        for parameter in obj.schema.names:
            _append_parameter(parameters, parameter)
        for provider in obj.providers:
            _append_provider(providers, provider)

    schema = _get_schema(ts.granularity, parameters)
    df = concat_fragments([obj._df for obj in objs], schema)

    return TimeSeries(
        ts.granularity,
        schema,
        providers,
        stations,
        schema.format(df),
        start,
        end,
        ts.timezone,
    )
