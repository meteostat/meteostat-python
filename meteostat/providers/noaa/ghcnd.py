"""
Process GHCND data

The code is licensed under the MIT license.
"""
from io import StringIO
from ftplib import FTP
from numpy import nan
import pandas as pd
from meteostat.typing import QueryDict
from meteostat.utils.decorators import cache
from meteostat.utils.converters import ms_to_kmh, percentage_to_okta

FTP_SERVER = "ftp.ncdc.noaa.gov"
COLUMN_NAMES = {
    "MM/DD/YYYY": "time",
    "TMAX": "tmax",
    "TMIN": "tmin",
    "TAVG": "tavg",
    "PRCP": "prcp",
    "SNWD": "snow",
    "AWDR": "wdir",
    "AWND": "wspd",
    "TSUN": "tsun",
    "WSFG": "wpgt",
    "ACMC": "cldc",
}


def connect_to_ftp():
    """
    Connect to FTP server
    """
    ftp = FTP(FTP_SERVER)
    ftp.login()

    return ftp


def get_flags(string):
    """
    Get flags, replacing empty flags with '_' for clarity (' S ' becomes '_S_')
    """
    m_flag = string.read(1)
    m_flag = m_flag if m_flag.strip() else "_"
    q_flag = string.read(1)
    q_flag = q_flag if q_flag.strip() else "_"
    s_flag = string.read(1)
    s_flag = s_flag if s_flag.strip() else "_"

    return [m_flag + q_flag + s_flag]


def create_df(element, dict_element):
    """
    Create dataframes from dicts, turn indices into date strings (YYYY-MM-DD)
    """
    element = element.upper()
    df_element = pd.DataFrame(dict_element)

    # Add dates (YYYY-MM-DD) as index on df. Pad days with zeros to two places
    df_element.index = (
        df_element["YEAR"]
        + "-"
        + df_element["MONTH"]
        + "-"
        + df_element["DAY"].str.zfill(2)
    )
    df_element.index.name = "DATE"

    # Arrange columns so ID, YEAR, MONTH, DAY are at front. Leaving them in
    # for plotting later - https://stackoverflow.com/a/31396042
    for col in ["DAY", "MONTH", "YEAR", "ID"]:
        df_element = move_col_to_front(col, df_element)

    # Convert numerical values to float
    df_element.loc[:, element] = df_element.loc[:, element].astype(float)

    return df_element


def move_col_to_front(element, df):
    """
    Move DataFrame column to position 0
    """
    element = element.upper()
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index(element)))
    df = df.reindex(columns=cols)

    return df


# pylint: disable=too-many-locals
def dly_to_df(ftp, station_id):
    """
    Convert .dly files to DataFrame
    """
    ftp_filename = station_id + ".dly"

    # Write .dly file to stream using StringIO using FTP command 'RETR'
    stream = StringIO()
    ftp.retrlines("RETR " + "/pub/data/ghcn/daily/all/" + ftp_filename, stream.write)

    # Move to first char in file
    stream.seek(0)

    # File params
    num_chars_line = 269
    num_chars_metadata = 21

    element_list = [
        "TMAX",
        "TMIN",
        "TAVG",
        "PRCP",
        "SNWD",
        "AWDR",
        "AWND",
        "TSUN",
        "WSFG",
        "ACMC",
    ]

    # Read through entire StringIO stream (the .dly file)
    # and collect the data
    all_dicts = {}
    element_flag = {}
    prev_year = "0000"
    index = 0

    while True:
        index += 1

        # Read metadata for each line
        # (one month of data for a particular element per line)
        id_station = stream.read(11)
        year = stream.read(4)
        month = stream.read(2)
        day = 0
        element = stream.read(4)

        # If this is blank then we've reached EOF and should exit loop
        if not element:
            break

        # Loop through each day in rest of row,
        # break if current position is end of row
        while stream.tell() % num_chars_line != 0:
            day += 1
            # Fill in contents of each dict depending on element type in
            # current row
            if day == 1:
                try:
                    first_hit = element_flag[element]
                    pass
                except BaseException:
                    element_flag[element] = 1
                    all_dicts[element] = {}
                    all_dicts[element]["ID"] = []
                    all_dicts[element]["YEAR"] = []
                    all_dicts[element]["MONTH"] = []
                    all_dicts[element]["DAY"] = []
                    all_dicts[element][element.upper()] = []
                    all_dicts[element][element.upper() + "_FLAGS"] = []

            value = stream.read(5)
            flags = get_flags(stream)
            if value == "-9999":
                continue
            all_dicts[element]["ID"] += [station_id]
            all_dicts[element]["YEAR"] += [year]
            all_dicts[element]["MONTH"] += [month]
            all_dicts[element]["DAY"] += [str(day)]
            all_dicts[element][element.upper()] += [value]
            all_dicts[element][element.upper() + "_FLAGS"] += flags

    # Create dataframes from dict
    all_dfs = {}
    for element in list(all_dicts.keys()):
        all_dfs[element] = create_df(element, all_dicts[element])

    # Combine all element dataframes into one dataframe,
    # indexed on date.
    #
    # pd.concat automagically aligns values to matching indices, therefore the
    # data is date aligned!
    list_dfs = []
    for df in list(all_dfs.keys()):
        list_dfs += [all_dfs[df]]
    df_all = pd.concat(list_dfs, axis=1, sort=False)
    df_all.index.name = "MM/DD/YYYY"

    # Remove duplicated/broken columns and rows
    # https://stackoverflow.com/a/40435354
    df_all = df_all.loc[:, ~df_all.columns.duplicated()]
    df_all = df_all.loc[df_all["ID"].notnull(), :]

    return df_all


@cache(60 * 60 * 24, "pickle")
def get_df(station: str) -> pd.DataFrame:
    ftp = connect_to_ftp()
    df = dly_to_df(ftp, station)
    # Filter relevant columns
    df = df.drop(columns=[col for col in df if col not in COLUMN_NAMES.keys()])
    # Add missing columns
    for col in list(COLUMN_NAMES.keys())[1:]:
        if col not in df.columns:
            df[col] = nan

    # Rename columns
    df = df.reset_index().rename(columns=COLUMN_NAMES)

    # Adapt columns
    df["time"] = pd.to_datetime(df["time"])
    df["tavg"] = df["tavg"].div(10)
    df["tmin"] = df["tmin"].div(10)
    df["tmax"] = df["tmax"].div(10)
    df["prcp"] = df["prcp"].div(10)
    df["wspd"] = df["wspd"].div(10).apply(ms_to_kmh)
    df["wpgt"] = df["wpgt"].div(10).apply(ms_to_kmh)
    df["cldc"] = df["cldc"].apply(percentage_to_okta)

    return df.set_index("time")


def fetch(query: QueryDict):
    ghcn_id = (
        query["station"]["identifiers"]["ghcn"]
        if "ghcn" in query["station"]["identifiers"]
        else None
    )
    if not ghcn_id:
        return pd.DataFrame()
    return get_df(ghcn_id)
