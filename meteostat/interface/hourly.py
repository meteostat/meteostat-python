from typing import Literal, Optional
from datetime import datetime
from importlib import import_module

from meteostat import framework
from meteostat import meta_bulk
from meteostat.utilities.time import parse_time

def hourly(
        station: list[str] | str,
        start: str | datetime,
        end: str | datetime,
        parameters: Optional[list[str]] = None,
        providers: Optional[list[Literal]] = None,
        sync = False
):
    """
    Retrieve hourly time series data
    """
    framework.logger().info(f'timeseries.hourly called for {len(station) if isinstance(station, list) else 1} station(s) with start={start} and end={end}')
    for st in meta_bulk(station):
        print(st.result())
    start = parse_time(start)
    end = parse_time(end, True)
    for provider in providers:
        details = framework.providers().get(provider.value)
        framework.logger().info(f'Calling handler {details["handler"]}')
        handler = import_module(details['handler'])
        df = handler.handler(station, start, end)