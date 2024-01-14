"""
DWD national hourly data import routine

Get hourly data for weather stations in Germany.

The code is licensed under the MIT license.
"""

from datetime import datetime
from ftplib import FTP
from io import BytesIO
from zipfile import ZipFile
import pandas as pd
from meteostat import Parameter
from meteostat.typing import Station
from meteostat.utils.decorators import cache
from meteostat.utils.converters import jcm2_to_wm2, ms_to_kmh
from meteostat.providers.dwd.shared import get_condicode
from meteostat.providers.dwd.shared import get_ftp_connection


BASE_DIR = "/climate_environment/CDC/observations_germany/climate/hourly/"
PARAMETERS = {
    "prcp": {
        "dir": "precipitation",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"R1": "prcp"},
        "convert": {},
    },
    "temp": {
        "dir": "air_temperature",
        "usecols": [1, 3, 4],
        "parse_dates": {"time": [0]},
        "names": {"TT_TU": "temp", "RF_TU": "rhum"},
        "convert": {},
    },
    "wind": {
        "dir": "wind",
        "usecols": [1, 3, 4],
        "parse_dates": {"time": [0]},
        "names": {"F": "wspd", "D": "wdir"},
        "convert": {"wspd": ms_to_kmh},
    },
    "pres": {
        "dir": "pressure",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"P": "pres"},
        "convert": {},
    },
    "tsun": {
        "dir": "sun",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"SD_SO": "tsun"},
        "convert": {},
    },
    "cloud": {
        "dir": "cloudiness",
        "usecols": [1, 4],
        "parse_dates": {"time": [0]},
        "names": {"V_N": "cldc"},
        "convert": {},
    },
    "visb": {
        "dir": "visibility",
        "usecols": [1, 4],
        "parse_dates": {"time": [0]},
        "names": {"V_VV": "vsby"},
        "convert": {},
    },
    "coco": {
        "dir": "weather_phenomena",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"WW": "coco"},
        "convert": {"coco": get_condicode},
        "encoding": "latin-1",
    },
    "srad": {
        "dir": "solar",
        "usecols": [1, 5],
        "parse_dates": {"time": [0]},
        "names": {"FG_LBERG": "srad"},
        "convert": {"srad": jcm2_to_wm2},
        "historical_only": True,
    },
}


def find_file(ftp: FTP, path: str, needle: str):
    """
    Find file in directory
    """
    match = None

    try:
        ftp.cwd(BASE_DIR + path)
        files = ftp.nlst()
        matching = [f for f in files if needle in f]
        match = matching[0]
    except BaseException:
        pass

    return match


@cache(60 * 60 * 24, "pickle")
def get_df(parameter: dict, mode: str, station_id: str) -> pd.DataFrame:
    """
    Get a file from DWD FTP server and convert to Polars DataFrame
    """
    ftp = get_ftp_connection()
    remote_file = find_file(ftp, f'{parameter["dir"]}/{mode}', station_id)

    if remote_file is None:
        return pd.DataFrame()

    buffer = BytesIO()
    ftp.retrbinary("RETR " + remote_file, buffer.write)
    # Unzip file
    with ZipFile(buffer, "r") as zipped:
        filelist = zipped.namelist()
        raw = None
        for file in filelist:
            if file[:7] == "produkt":
                with zipped.open(file, "r") as reader:
                    raw = BytesIO(reader.read())
    # Convert raw data to DataFrame
    df: pd.DataFrame = pd.read_csv(
        raw,
        sep=";",
        date_format="%Y%m%d%H",
        na_values="-999",
        usecols=parameter["usecols"],
        parse_dates=parameter["parse_dates"],
        encoding=parameter["encoding"] if "encoding" in parameter else None,
    )
    # Rename columns
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=parameter["names"])
    # Convert column data
    for col, func in parameter["convert"].items():
        df[col] = df[col].apply(func)
    # Set index
    df = df.set_index("time")
    # Round decimals
    df = df.round(1)

    return df


def get_parameter(parameter: str, modes: list[str], station: Station) -> pd.DataFrame:
    data = [
        get_df(PARAMETERS[parameter], mode, station["identifiers"]["national"])
        for mode in modes
    ]
    df = pd.concat(data)
    return df.loc[~df.index.duplicated(keep="first")]


def fetch(
    station: Station, start: datetime, end: datetime, parameters: list[Parameter]
):
    if not "national" in station["identifiers"]:
        return None

    modes = [
        m
        for m in [
            "historical" if abs((start - datetime.now()).days) > 120 else None,
            "recent" if abs((end - datetime.now()).days) < 120 else None,
        ]
        if m is not None
    ]  # can be "recent" and/or "historical"

    columns = map(
        lambda args: get_parameter(*args),
        (
            (parameter, modes, station)
            for parameter in {
                key: PARAMETERS[key] for key in parameters if key in PARAMETERS
            }
        ),
    )

    return pd.concat(columns, axis=1)
