"""
DWD national hourly data import routine

Get hourly data for weather stations in Germany.

The code is licensed under the MIT license.
"""

from datetime import datetime
from ftplib import FTP
from io import BytesIO
from typing import Callable, Dict, List, NotRequired, Optional, TypedDict
from zipfile import ZipFile
import pandas as pd
from meteostat.core.logger import logger
from meteostat.typing import QueryDict, StationDict
from meteostat.utils.decorators import cache
from meteostat.utils.converters import jcm2_to_wm2, ms_to_kmh
from meteostat.providers.dwd.shared import get_condicode
from meteostat.providers.dwd.shared import get_ftp_connection


class ParameterDefinition(TypedDict):
    dir: str
    usecols: List[int]
    parse_dates: Dict[str, List[int]]
    names: Dict[str, str]
    convert: NotRequired[Dict[str, Callable]]
    encoding: NotRequired[str]
    historical_only: NotRequired[bool]


BASE_DIR = "/climate_environment/CDC/observations_germany/climate/hourly/"
PARAMETERS: List[ParameterDefinition] = [
    {
        "dir": "precipitation",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"R1": "prcp"},
    },
    {
        "dir": "air_temperature",
        "usecols": [1, 3, 4],
        "parse_dates": {"time": [0]},
        "names": {"TT_TU": "temp", "RF_TU": "rhum"},
    },
    {
        "dir": "wind",
        "usecols": [1, 3, 4],
        "parse_dates": {"time": [0]},
        "names": {"F": "wspd", "D": "wdir"},
        "convert": {"wspd": ms_to_kmh},
    },
    {
        "dir": "pressure",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"P": "pres"},
    },
    {
        "dir": "sun",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"SD_SO": "tsun"},
    },
    {
        "dir": "cloudiness",
        "usecols": [1, 4],
        "parse_dates": {"time": [0]},
        "names": {"V_N": "cldc"},
    },
    {
        "dir": "visibility",
        "usecols": [1, 4],
        "parse_dates": {"time": [0]},
        "names": {"V_VV": "vsby"},
    },
    {
        "dir": "weather_phenomena",
        "usecols": [1, 3],
        "parse_dates": {"time": [0]},
        "names": {"WW": "coco"},
        "convert": {"coco": get_condicode},
        "encoding": "latin-1",
    },
    {
        "dir": "solar",
        "usecols": [1, 5],
        "parse_dates": {"time": [0]},
        "names": {"FG_LBERG": "srad"},
        "convert": {"srad": jcm2_to_wm2},
        "historical_only": True,
    },
]


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
def get_df(parameter_dir: str, mode: str, station_id: str) -> Optional[pd.DataFrame]:
    """
    Get a file from DWD FTP server and convert to Polars DataFrame
    """
    parameter = next(param for param in PARAMETERS if param["dir"] == parameter_dir)

    ftp = get_ftp_connection()
    remote_file = find_file(ftp, f'{parameter["dir"]}/{mode}', station_id)

    if remote_file is None:
        return None

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
        skipinitialspace=True,
        date_format="%Y%m%d%H",
        na_values=[-999, "-999"],
        usecols=parameter["usecols"],
        parse_dates=parameter["parse_dates"],
        encoding=parameter["encoding"] if "encoding" in parameter else None,
    )
    # Rename columns
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=parameter["names"])
    # Convert column data
    if "convert" in parameter:
        for col, func in parameter["convert"].items():
            df[col] = df[col].apply(func)
    # Set index
    df = df.set_index("time")
    # Round decimals
    df = df.round(1)

    return df


def get_parameter(
    parameter_dir: str, modes: list[str], station: StationDict
) -> Optional[pd.DataFrame]:
    try:
        data = [
            get_df(parameter_dir, mode, station["identifiers"]["national"])
            for mode in modes
        ]
        if all(d is None for d in data):
            return None
        df = pd.concat(data)
        return df.loc[~df.index.duplicated(keep="first")]
    except Exception as error:
        logger.error(error)
        return None


def fetch(query: QueryDict):
    if not "national" in query["station"]["identifiers"]:
        return None

    modes = [
        m
        for m in [
            "historical" if abs((query["start"] - datetime.now()).days) > 120 else None,
            "recent" if abs((query["end"] - datetime.now()).days) < 120 else None,
        ]
        if m is not None
    ]  # can be "recent" and/or "historical"

    columns = map(
        lambda args: get_parameter(*args),
        (
            (parameter["dir"], modes, query["station"])
            for parameter in [
                param
                for param in PARAMETERS
                if not set(query["parameters"]).isdisjoint(param["names"].values())
            ]
        ),
    )

    return pd.concat(columns, axis=1)
