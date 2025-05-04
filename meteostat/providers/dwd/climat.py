"""
DWD global CLIMAT data
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


cnf = config[Provider.CLIMAT]

BASE_DIR = "/climate_environment/CDC/observations_global/CLIMAT/monthly/qc/"
PARAMETERS = [
    {
        "dir": "precipitation_total",
        "parameter": Parameter.PRCP,
        "stubnames": {
            "jahr": "year",
            "jan": "prcp1",
            "feb": "prcp2",
            "mrz": "prcp3",
            "apr": "prcp4",
            "mai": "prcp5",
            "jun": "prcp6",
            "jul": "prcp7",
            "aug": "prcp8",
            "sep": "prcp9",
            "okt": "prcp10",
            "nov": "prcp11",
            "dez": "prcp12",
        },
    },
    {
        "dir": "air_temperature_mean",
        "parameter": Parameter.TEMP,
        "stubnames": {
            "jahr": "year",
            "jan": "tavg1",
            "feb": "tavg2",
            "mrz": "tavg3",
            "apr": "tavg4",
            "mai": "tavg5",
            "jun": "tavg6",
            "jul": "tavg7",
            "aug": "tavg8",
            "sep": "tavg9",
            "okt": "tavg10",
            "nov": "tavg11",
            "dez": "tavg12",
        },
    },
    {
        "dir": "air_temperature_mean_of_daily_max",
        "parameter": Parameter.TMAX,
        "stubnames": {
            "jahr": "year",
            "jan": "tmax1",
            "feb": "tmax2",
            "mrz": "tmax3",
            "apr": "tmax4",
            "mai": "tmax5",
            "jun": "tmax6",
            "jul": "tmax7",
            "aug": "tmax8",
            "sep": "tmax9",
            "okt": "tmax10",
            "nov": "tmax11",
            "dez": "tmax12",
        },
    },
    {
        "dir": "air_temperature_mean_of_daily_min",
        "parameter": Parameter.TMIN,
        "stubnames": {
            "jahr": "year",
            "jan": "tmin1",
            "feb": "tmin2",
            "mrz": "tmin3",
            "apr": "tmin4",
            "mai": "tmin5",
            "jun": "tmin6",
            "jul": "tmin7",
            "aug": "tmin8",
            "sep": "tmin9",
            "okt": "tmin10",
            "nov": "tmin11",
            "dez": "tmin12",
        },
    },
    {
        "dir": "mean_sea_level_pressure",
        "parameter": Parameter.PRES,
        "stubnames": {
            "jahr": "year",
            "jan": "pres1",
            "feb": "pres2",
            "mrz": "pres3",
            "apr": "pres4",
            "mai": "pres5",
            "jun": "pres6",
            "jul": "pres7",
            "aug": "pres8",
            "sep": "pres9",
            "okt": "pres10",
            "nov": "pres11",
            "dez": "pres12",
        },
    },
    {
        "dir": "sunshine_duration",
        "parameter": Parameter.TSUN,
        "stubnames": {
            "jahr": "year",
            "jan": "tsun1",
            "feb": "tsun2",
            "mrz": "tsun3",
            "apr": "tsun4",
            "mai": "tsun5",
            "jun": "tsun6",
            "jul": "tsun7",
            "aug": "tsun8",
            "sep": "tsun9",
            "okt": "tsun10",
            "nov": "tsun11",
            "dez": "tsun12",
        },
    },
]


def find_file(ftp: FTP, mode: str, dir: str, needle: str):
    """
    Find file in directory
    """
    match = None

    try:
        ftp.cwd(f"{BASE_DIR}{dir}/{mode}")
        files = ftp.nlst()
        matching = [f for f in files if needle in f]
        match = matching[0]
    except BaseException as error:
        logger.debug(f"Error while searching for file", exc_info=True)
        pass

    return match


@cache_service.cache(TTL.WEEK, "pickle")
def get_df(parameter: str, mode: str, station: str) -> Optional[pd.DataFrame]:
    """
    Get a file from DWD FTP server and convert to Polars DataFrame
    """
    parameter_data = next(
        param for param in PARAMETERS if param["parameter"] == parameter
    )
    ftp = get_ftp_connection()
    remote_file = find_file(
        ftp, mode, parameter_data["dir"], station if mode == "recent" else f"{station}_"
    )

    if remote_file is None:
        logger.debug(
            f"File not found for parameter '{parameter}', mode '{mode}' and station '{station}'"
        )
        return None

    buffer = BytesIO()
    ftp.retrbinary("RETR " + remote_file, buffer.write)

    buffer.seek(0)

    ftp.close()

    # Convert raw data to DataFrame
    df = pd.read_csv(buffer, sep=";")

    # Rename columns
    df = df.rename(columns=lambda x: x.strip().lower())
    df = df.rename(columns=parameter_data["stubnames"])

    # Translate from wide to long
    df = pd.wide_to_long(
        df,
        stubnames=parameter_data["parameter"],
        i="year",
        j="month",
    )

    # Sunshine hours to minutes
    if parameter_data["parameter"] == Parameter.TSUN:
        df[Parameter.TSUN] = df[Parameter.TSUN] * 60

    df = df.reset_index()
    df["date"] = (
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2) + "-01"
    )
    df["time"] = pd.to_datetime(df["date"])
    df = df.drop(["year", "month", "date"], axis=1).set_index("time")

    return df


def get_parameter(
    parameter: str, modes: List[str], station: Station
) -> Optional[pd.DataFrame]:
    logger.debug(f"Fetching {parameter} data ({modes}) for station '{station.id}'")

    try:

        data = [get_df(parameter, mode, station.identifiers["wmo"]) for mode in modes]

        if all(d is None for d in data):
            return None

        df = pd.concat(data)
        return df.loc[~df.index.duplicated(keep="first")]

    except Exception as error:

        logger.warning(error, exc_info=True)

        return None


def fetch(query: Query):
    if not "wmo" in query.station.identifiers:
        return pd.DataFrame()

    # Check which modes to consider for data fetching
    #
    # The dataset is divided into a versioned part with completed quality check ("historical"),
    # and a part for which the quality check has not yet been completed ("recent").
    #
    # There is no definite answer as to when the quality check is completed. We're assuming a
    # period of 5 years here. If the end date of the query is within this period, we will also
    # consider the "recent" mode.
    modes = ["historical"]
    if abs((query.end - datetime.now()).days) < 5 * 365:
        modes.append("recent")

    columns = map(
        lambda args: get_parameter(*args),
        (
            (parameter["parameter"].value, cnf.get("modes", modes), query.station)
            for parameter in [
                param for param in PARAMETERS if param["parameter"] in query.parameters
            ]
        ),
    )

    return pd.concat(columns, axis=1)
