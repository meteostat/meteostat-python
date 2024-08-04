"""
DWD national daily data import routine

Get daily data for weather stations in Germany.

The code is licensed under the MIT license.
"""

from datetime import datetime
from ftplib import FTP
from io import BytesIO
from typing import Optional
from zipfile import ZipFile
import pandas as pd
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache
from meteostat.utils.converters import ms_to_kmh, pres_to_msl
from meteostat.providers.dwd.shared import get_ftp_connection


BASE_DIR = "/climate_environment/CDC/observations_germany/climate/monthly/kl/"
USECOLS = [1, 4, 5, 6, 7, 10, 12, 14]  # CSV cols which should be read
PARSE_DATES = {"time": [0]}  # Which columns should be parsed as dates?
NAMES = {
    "MO_N": "cldc",
    "MO_TT": "tavg",
    "MO_TX": "tmax",
    "MO_TN": "tmin",
    "MX_FX": "wpgt",
    "MO_SD_S": "tsun",
    "MO_RR": "prcp",
}


def find_file(ftp: FTP, mode: str, needle: str):
    """
    Find file in directory
    """
    match = None

    try:
        ftp.cwd(BASE_DIR + mode)
        files = ftp.nlst()
        matching = [f for f in files if needle in f]
        match = matching[0]
    except BaseException:
        pass

    return match


@cache(60 * 60 * 24 * 7, "pickle")
def get_df(station: str, mode: str) -> Optional[pd.DataFrame]:
    """
    Get a file from DWD FTP server and convert to Polars DataFrame
    """
    ftp = get_ftp_connection()
    remote_file = find_file(ftp, mode, f"_{station}_")

    if remote_file is None:
        return None

    buffer = BytesIO()
    ftp.retrbinary("RETR " + remote_file, buffer.write)

    ftp.close()

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
        sep=r"\s*;\s*",
        date_format="%Y%m%d",
        na_values=["-999", -999],
        usecols=USECOLS,
        parse_dates=PARSE_DATES,
        engine="python",
    )

    # Rename columns
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=NAMES)

    # Convert data
    df["wpgt"] = df["wpgt"].apply(ms_to_kmh)
    df["tsun"] = df["tsun"] * 60
    df["tsun"] = df["tsun"].round()
    df["cldc"] = df["cldc"].round()

    # Set index
    df = df.set_index("time")

    # Round decimals
    df = df.round(1)

    return df


def fetch(query: QueryDict):
    if not "national" in query["station"]["identifiers"]:
        return pd.DataFrame()

    modes = [
        m
        for m in [
            "historical" if abs((query["start"] - datetime.now()).days) > 120 else None,
            "recent" if abs((query["end"] - datetime.now()).days) < 120 else None,
        ]
        if m is not None
    ]  # can be "recent" and/or "historical"

    data = [
        get_df(
            query["station"]["identifiers"]["national"],
            mode,
        )
        for mode in modes
    ]

    df = pd.concat(data)

    return df.loc[~df.index.duplicated(keep="first")]
