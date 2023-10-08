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
from meteostat.types import Station
from meteostat.provider.dwd.condicode import get_condicode
from meteostat.provider.dwd.shared import get_ftp_connection
from meteostat.utilities.units import jcm2_to_wm2, ms_to_kmh
from meteostat.core.cache import cache
from meteostat.core.pool import allocate_workers


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
    }
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

@cache(60*60*24, 'pickle')
def fetch(parameter: str, mode: str, station_id: str) -> pd.DataFrame:
    """
    Get a file from DWD FTP server and convert to Polars DataFrame
    """
    parameter = PARAMETERS[parameter]
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
        encoding=parameter["encoding"]
        if "encoding" in parameter
        else None,
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
    for mode in modes:
        data = []
        data.append(
            fetch(parameter, mode, station["identifiers"]["national"])
        )
    return pd.concat(data)

def handler(station: Station, start: datetime, end: datetime, pool: Pool):
    if not "national" in station["identifiers"]:
        return pd.DataFrame()

    modes = [m for m in [
        "historical" if abs((start - datetime.now()).days) > 120 else None,
        "recent" if abs((end - datetime.now()).days) < 120 else None
    ] if m is not None] # can be "recent" and/or "historical"

    columns = pool.map(lambda i: get_parameter(*i), ((parameter, modes, station) for parameter in PARAMETERS))

    return pd.concat(columns, axis=1)

