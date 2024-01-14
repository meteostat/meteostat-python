from datetime import datetime, date
from enum import Enum
from typing import List, NotRequired, Tuple, TypeVar, TypedDict, Union, Optional
from meteostat.enumerations import Priority, Granularity


T = TypeVar("T")
SequenceInput = Union[Tuple[T, ...], List[T], T]

DateTimeInput = Optional[Union[datetime, date]]


class Location(TypedDict):
    latitude: float
    longitude: float
    elevation: int


class Station(TypedDict):
    id: str
    name: dict[str, str]
    country: str
    region: str
    identifiers: dict[str, str]
    location: Location
    timezone: str


class Provider(TypedDict):
    id: Enum
    name: str
    granularity: Granularity
    priority: Priority
    start: datetime
    end: NotRequired[Optional[datetime]]
    countries: NotRequired[list[str]]
    parameters: list[Enum]
    license: NotRequired[str]
    module: str
