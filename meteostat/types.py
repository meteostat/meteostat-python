from enum import Enum
from typing import TypedDict

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
    interface: Enum
    countries: list[str]
    parameters: list[Enum]
    license: str
    module: str