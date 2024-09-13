from datetime import datetime
from enum import Enum
from typing import List, NotRequired, TypedDict, Optional
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
    module: str


class QueryDict(TypedDict):
    station: StationDict
    start: datetime
    end: datetime
    parameters: List[Parameter]


class SettingsDict(TypedDict):
    cache_enable: bool
    cache_dir: str
    cache_ttl_max: int
    cache_ttl_min: int
    cache_autoclean: bool
    station_mirrors: List[str]
    location_mirrors: List[str]
    bulk_load_sources: bool
    point_radius: int
    point_stations: int
