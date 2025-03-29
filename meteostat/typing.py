"""
Meteostat Typing
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List, Optional

from meteostat.core.validator import Validator
from meteostat.enumerations import (
    Grade,
    Priority,
    Granularity,
    Parameter,
    Provider,
    Unit,
)


@dataclass
class Station:
    """
    A weather station
    """

    id: str  # The Meteostat station ID
    names: dict[str, str]  # The name of the station in different languages
    country: str  # ISO 3166-1 alpha-2 country code
    region: str  # ISO 3166-2 state or region code
    identifiers: dict[str, str]  # Provider identifiers
    latitude: float  # The latitude in degrees
    longitude: float  # The longitude in degrees
    elevation: int  # The elevation in meters
    timezone: str  # The IANA timezone name

    @property
    def name(self) -> str:
        """
        The English name of the station
        """
        return self.names["en"]


@dataclass
class License:
    """
    A license
    """

    commercial: bool
    attribution: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None


@dataclass
class ProviderSpec:
    """
    A provider's meta data
    """

    id: Provider | str  # The provider ID
    granularity: Granularity  # The provider's time series granularity
    priority: Priority  # The priority of the provider
    grade: Optional[Grade]  # The provider's data quality grade
    license: Optional[License]  # The provider's license
    parameters: List[Parameter]  # List of supported meteorological parameters
    start: datetime  # The start date of the provider's data
    end: Optional[datetime] = None  # The end date of the provider's data
    countries: Optional[list[str]] = None  # List of supported countries
    module: Optional[str] = None  # Module path to the provider's API


@dataclass
class ParameterSpec:
    """
    A parameter's meta data
    """

    id: Parameter | str  # The parameter ID
    name: str  # A descriptive parameter name
    granularity: Granularity  # The perameter's granularity
    dtype: str  # The parameter's data type
    unit: Optional[Unit] = None  # The parameter's data unit
    validators: List[Validator | Callable] = field(
        default_factory=list
    )  # The parameter's validators


@dataclass
class Request:
    """
    A request to fetch meteorological time series data
    """

    granularity: Granularity  # Query's time series granularity
    providers: List[Provider]  # Providers to query
    parameters: List[Parameter]  # Schema of the query's data
    stations: List[Station]  # Stations to query
    start: Optional[datetime] = None  # Start date of the query
    end: Optional[datetime] = None  # End date of the query
    timezone: Optional[str] = None  # Time zone of the query's data
    model: bool = True  # Include model data?


@dataclass
class Query:
    """
    A query to fetch meteorological data from a provider
    """

    station: Station  # Station to query
    parameters: List[Parameter]  # List of meteorological parameters to query
    start: Optional[datetime]  # Start date of the query
    end: Optional[datetime]  # End date of the query
