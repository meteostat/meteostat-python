from enum import Enum
from typing import TypedDict

class Station(TypedDict):
    """
    A typed dictionary for weather stations
    """
    
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
    """
    A typed dictionary for a provider
    """
    
    id: Enum
    name: str
    countries: list[str]
    parameters: list[Enum]
    license: str
    handler: str