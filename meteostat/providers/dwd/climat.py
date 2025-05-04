"""
DWD Global CLIMAT Data
"""

from datetime import datetime
from ftplib import FTP
from io import BytesIO
from typing import List, Optional

import pandas as pd

from meteostat.core.logger import logger
from meteostat.core.config import config
from meteostat.enumerations import TTL, Parameter, Provider
from meteostat.typing import Query, Station
from meteostat.core.cache import cache_service
from meteostat.providers.dwd.shared import get_ftp_connection

# Constants
CNF = config[Provider.CLIMAT]
BASE_DIR = "/climate_environment/CDC/observations_global/CLIMAT/monthly/qc/"

# Monthly column stubnames mapping template
MONTHS_MAP = {
    "jan": 1,
    "feb": 2,
    "mrz": 3,
    "apr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "nov": 11,
    "dez": 12,
}

# Parameter directory configurations
PARAMETERS = [
    ("precipitation_total", Parameter.PRCP),
    ("air_temperature_mean", Parameter.TEMP),
    ("air_temperature_mean_of_daily_max", Parameter.TMAX),
    ("air_temperature_mean_of_daily_min", Parameter.TMIN),
    ("mean_sea_level_pressure", Parameter.PRES),
    ("sunshine_duration", Parameter.TSUN),
]

# Precomputed parameter configs with stubnames
PARAMETER_CONFIGS = {
    param: {
        "dir": dir_name,
        "stubnames": {
            "jahr": "year",
            **{
                month: f"{param}{i+1}"
                for i, (month, _) in enumerate(MONTHS_MAP.items())
            },
        },
    }
    for dir_name, param in PARAMETERS
}


def find_file(ftp: FTP, mode: str, directory: str, search_term: str) -> Optional[str]:
    """
    Find a file in the FTP directory matching a pattern.
    """
    try:
        ftp.cwd(f"{BASE_DIR}{directory}/{mode}")
        matches = [f for f in ftp.nlst() if search_term in f]
        return matches[0] if matches else None
    except Exception:
        logger.debug("Error while searching for file", exc_info=True)
        return None


@cache_service.cache(TTL.WEEK, "pickle")
def get_df(parameter: str, mode: str, station_code: str) -> Optional[pd.DataFrame]:
    """
    Download and parse a CLIMAT dataset from DWD FTP.
    """
    config = PARAMETER_CONFIGS.get(parameter)
    if not config:
        logger.debug(f"Unknown parameter '{parameter}'")
        return None

    ftp = get_ftp_connection()
    search_term = station_code if mode == "recent" else f"{station_code}_"
    remote_file = find_file(ftp, mode, config["dir"], search_term)

    if not remote_file:
        logger.debug(
            f"No file found for parameter '{parameter}', mode '{mode}', station '{station_code}'"
        )
        return None

    buffer = BytesIO()
    ftp.retrbinary(f"RETR {remote_file}", buffer.write)
    ftp.close()

    buffer.seek(0)
    df = pd.read_csv(buffer, sep=";").rename(columns=lambda col: col.strip().lower())
    df.rename(columns=config["stubnames"], inplace=True)

    # Convert wide to long format
    df = pd.wide_to_long(
        df, stubnames=parameter, i="year", j="month", sep="", suffix="\\d+"
    ).reset_index()

    if parameter == Parameter.TSUN:
        df[Parameter.TSUN] *= 60  # convert hours to minutes

    # Create datetime index
    df["time"] = pd.to_datetime(
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
    )

    return df.drop(columns=["year", "month"]).set_index("time")


def get_parameter(
    parameter: str, modes: List[str], station: Station
) -> Optional[pd.DataFrame]:
    """
    Fetch and merge data for a parameter over multiple modes (e.g., recent, historical).
    """
    try:
        station_code = station.identifiers.get("wmo")
        if not station_code:
            return None

        datasets = [get_df(parameter, mode, station_code) for mode in modes]
        datasets = [df for df in datasets if df is not None]

        if not datasets:
            return None

        return pd.concat(datasets).loc[lambda df: ~df.index.duplicated(keep="first")]
    except Exception as e:
        logger.warning(
            f"Failed to fetch data for parameter '{parameter}': {e}", exc_info=True
        )
        return None


def fetch(query: Query) -> pd.DataFrame:
    """
    Entry point to fetch all requested parameters for a station query.
    """
    station_code = query.station.identifiers.get("wmo")
    if not station_code:
        return pd.DataFrame()

    modes = ["historical"]
    if (datetime.now() - query.end).days < 5 * 365:
        modes.append("recent")

    data_frames = [
        get_parameter(param.value, CNF.get("modes", modes), query.station)
        for param in query.parameters
        if param in PARAMETER_CONFIGS
    ]

    return pd.concat([df for df in data_frames if df is not None], axis=1)
