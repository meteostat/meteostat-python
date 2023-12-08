from datetime import datetime
from importlib import import_module
from itertools import chain
import pandas as pd
import pytz
from meteostat import Provider, types, stations
from meteostat.core.logger import logger
from meteostat.core.providers import filter_providers
from meteostat.data.timeseries import Timeseries
from meteostat.enumerations import Granularity, Parameter
from meteostat.utils.mutations import filter_parameters, filter_time


def validate_parameters(supported: list[Parameter], requested: list[Parameter]) -> None:
    """
    Raise an exception if a requested parameter is not supported
    """
    diff = set(requested).difference(set(supported))
    if len(diff):
        logger.warn(f"""Tried to request data for unsupported parameters: {
            ", ".join([p.value for p in diff])
        }""")


def load_stations(station: list[str] | str) -> list[types.Station]:
    """
    Convert a single station ID or a list of IDs to a list of Station objects
    """
    return list(map(stations.meta, [station] if isinstance(station, str) else station))


def parse_time(
    value: str | datetime | None, timezone: str | None = None, is_end: bool = False
) -> datetime | None:
    """
    Convert a given date/time input to datetime

    To set the time of a date-only string to 23:59:59, pass is_end=True
    """
    if not value:
        return None

    if isinstance(value, str) and len(value) == 10:
        value = f"{value} 23:59:59" if is_end else f"{value} 00:00:00"
        value = datetime.fromisoformat(value)
    elif isinstance(value, str):
        value = datetime.fromisoformat(value)

    if timezone:
        timezone = pytz.timezone(timezone)
        value = value.astimezone(timezone).astimezone(pytz.utc).replace(tzinfo=None)

    return value


def call_provider(provider: types.Provider, *args) -> pd.DataFrame:
    """
    Get data from a given provider
    """
    module = import_module(provider["module"])
    df = module.fetch(*args)
    return df


def load_data(
    granularity: Granularity,
    providers: list[Provider],
    parameters: list[Parameter],
    stations: list[types.Station],
    start: datetime | None = None,
    end: datetime | None = None,
    lite: bool = True,
    max_station_count: int | None = None,
) -> types.LoaderResponse:
    """
    Load meteorological data from different providers
    """
    data = []
    included_stations = []
    for station in stations:
        s_data = []
        for provider in filter_providers(
            granularity, parameters, providers, station["country"], start, end
        ):
            df = call_provider(
                provider,
                station,
                start if start else provider["start"],
                end
                if end
                else (provider["end"] if "end" in provider else datetime.now()),
                parameters,
            )
            df = pd.concat([df], keys=[station["id"]], names=["station"])
            df["source"] = provider["id"].value
            df.set_index(["source"], append=True, inplace=True)
            df = filter_parameters(df, parameters)
            df = filter_time(df, start, end)
            # Drop NaN-only rows
            df = df.dropna(how="all")
            s_data.append(df)
            # Check if request is satisfied
            if (
                lite
                and Timeseries(
                    Granularity.HOURLY, [station], pd.concat(s_data), start, end
                ).coverage()
                == 1
            ):
                break
        if len(s_data):
            # Append station data to full data
            data.append(s_data)
            # Add station to included_stations
            included_stations.append(station)
        # Check for max_station_count
        if max_station_count and len(data) == max_station_count:
            break

    df = pd.concat(chain.from_iterable(data)) if len(data) > 0 else pd.DataFrame()

    return types.LoaderResponse({"stations": included_stations, "df": df})
