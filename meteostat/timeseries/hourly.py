from typing import Literal, Optional
from datetime import datetime
from importlib import import_module

import pandas as pd

from meteostat import stations, providers, Parameter
from meteostat.core import logger
from meteostat.core.pool import allocate_workers, Pool
from meteostat.utilities.time import parse_time

SUPPORTED_PARAMETERS = [
    Parameter.TEMP,
    Parameter.PRCP,
    Parameter.RHUM
]

def call_handler(provider, station, start, end, pool):
    details = providers.get(provider)
    handler = import_module(details['handler'])
    df = handler.handler(station, start, end, pool)
    df['station'] = station['id']
    print(station['id'])
    df = df.set_index("station", append=True)
    return df

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
    logger.info(f'timeseries.hourly called for {len(station) if isinstance(station, list) else 1} station(s) with start={start} and end={end}')
    # with framework.create_pool() as core_pool:
    #     result = core_pool.map(stations.meta, station)
    # for r in result:
    #     print(r)
    workers = allocate_workers(len(station) * len(providers))
    with Pool(workers[0]) as pool:
        station = pool.map(stations.meta, station)
    start = parse_time(start)
    end = parse_time(end, True)
    # print([[provider.name, s['id']] for provider in providers for s in station])
    data = []
    with Pool(workers[0]) as pool_outer, Pool(workers[1]) as pool_inner:
        for s in station:
            for provider in providers:
                data.append(pool_outer.submit(lambda: call_handler(provider, s, start, end, pool_inner)))
        data = [d.result() for d in data]
    # with framework.Pool(workers[0]) as pool:
    #     for s in station:
    #         for provider in providers:
    #             details = framework.providers.get(provider)
    #             framework.logger.info(f'Calling handler {details["handler"]}')
    #             handler = import_module(details['handler'])
    #             df = handler.handler(s, start, end, pool)
    #             df['station'] = s['id']
    #             df = df.set_index("station", append=True)
    #             data.append(df)
    print(pd.concat(data))
    exit()