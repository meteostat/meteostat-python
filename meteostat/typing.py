"""
Meteostat Typing
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime

from meteostat.core.validator import Validator
from meteostat.enumerations import (
    Grade,
    Granularity,
    Parameter,
    Priority,
    Provider,
    Unit,
)


@dataclass
class Station:
    """
    A weather station

    For virtual stations created from Point objects, some fields will be None.
    """

    id: str  # The Meteostat station ID (e.g., "10637" or "$0001" for virtual stations)
    name: str | None = None  # The (usually English) name of the station
    country: str | None = None  # ISO 3166-1 alpha-2 country code
    region: str | None = None  # ISO 3166-2 state or region code
    identifiers: dict[str, str] = field(default_factory=dict)  # Provider identifiers
    latitude: float | None = None  # The latitude in degrees
    longitude: float | None = None  # The longitude in degrees
    elevation: int | None = None  # The elevation in meters
    timezone: str | None = None  # The IANA timezone name


@dataclass
class License:
    """
    A license
    """

    commercial: bool
    attribution: str | None = None
    name: str | None = None
    url: str | None = None


@dataclass
class ProviderSpec:
    """
    A provider's meta data
    """

    id: Provider | str  # The provider ID
    name: str  # A descriptive provider name
    granularity: Granularity  # The provider's time series granularity
    priority: Priority | int  # The priority of the provider
    grade: Grade | None  # The provider's data quality grade
    license: License | None  # The provider's license
    parameters: list[Parameter]  # List of supported meteorological parameters
    start: date  # The start date of the provider's data
    end: datetime | None = None  # The end date of the provider's data
    countries: list[str] | None = None  # List of supported countries
    module: str | None = None  # Module path to the provider's API


@dataclass
class ParameterSpec:
    """
    A parameter's meta data
    """

    id: Parameter | str  # The parameter ID
    name: str  # A descriptive parameter name
    granularity: Granularity  # The parameter's granularity
    dtype: str  # The parameter's data type
    unit: Unit | None = None  # The parameter's data unit
    validators: list[Validator | Callable] = field(
        default_factory=list
    )  # The parameter's validators


@dataclass
class Request:
    """
    A request to fetch meteorological time series data
    """

    granularity: Granularity  # Query's time series granularity
    providers: list[Provider]  # Providers to query
    parameters: list[Parameter]  # Schema of the query's data
    station: Station | list[Station]  # Station(s) to query
    start: datetime | None = None  # Start date of the query
    end: datetime | None = None  # End date of the query
    timezone: str | None = None  # Time zone of the query's data


@dataclass
class ProviderRequest:
    """
    A query to fetch meteorological data from a provider
    """

    station: Station  # Station to query
    parameters: list[Parameter]  # List of meteorological parameters to query
    start: datetime | None  # Start date of the query
    end: datetime | None  # End date of the query
