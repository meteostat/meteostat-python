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