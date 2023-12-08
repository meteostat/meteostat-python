from datetime import datetime
from enum import Enum
from typing import TypedDict

import pandas as pd
from meteostat.enumerations import Priority, Granularity


class Station(TypedDict):
    id: str
    name: dict[str]
    country: str
    region: str
    identifiers: dict[str]
    latitude: float
    longitude: float
    elevation: int
    timezone: str


class Provider(TypedDict):
    id: Enum
    name: str
    granularity: Granularity
    priority: Priority
    start: datetime
    end: datetime | None
    countries: list[str]
    parameters: list[Enum]
    license: str
    module: str


class LoaderResponse(TypedDict):
    stations: list[Station]
    df: pd.DataFrame
    providers: list[Provider]
