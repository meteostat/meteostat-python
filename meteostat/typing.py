from datetime import datetime
from enum import Enum
from typing import Callable, List, NotRequired, TypedDict, Optional
from meteostat.enumerations import Priority, Granularity, Parameter, Provider


class LocationDict(TypedDict):
    latitude: float
    longitude: float
    elevation: int


class StationDict(TypedDict):
    id: str
    name: dict[str, str]
    country: str
    region: str
    identifiers: dict[str, str]
    location: LocationDict
    timezone: str


class ProviderDict(TypedDict):
    id: Provider
    name: str
    granularity: Granularity
    priority: Priority
    start: datetime
    end: NotRequired[Optional[datetime]]
    countries: NotRequired[list[str]]
    parameters: list[Enum]
    license: NotRequired[str]
    module: str


class ParameterGranularityDict(TypedDict):
    granularity: Granularity
    default: NotRequired[bool]


class ParameterDict(TypedDict):
    id: Parameter
    name: str
    dtype: type
    aggregation: NotRequired[str | Callable]
    granularities: List[ParameterGranularityDict]


class QueryDict(TypedDict):
    station: StationDict
    start: datetime
    end: datetime
    parameters: List[Parameter]
