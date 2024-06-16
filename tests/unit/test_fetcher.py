import os
import pandas as pd
from meteostat.enumerations import Parameter
from meteostat.fetcher import add_source, set_dtypes, stations_to_df


def test_add_source():
    """
    It should add a source column to a DataFrame
    """
    df = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_metar.pickle",
        )
    )
    df = add_source(df, "metar")

    assert df.index.get_level_values("source")[0] == "metar"


def test_set_dtypes(mocker):
    """
    It should set the correct data types on a DataFrame
    """
    df = pd.DataFrame({Parameter.TEMP: [1.1, 2.2], Parameter.RHUM: [30, 40]})
    parameters = [Parameter.TEMP, Parameter.RHUM]

    # Mock PARAMETER_DTYPES for test purposes
    PARAMETER_DTYPES = {Parameter.TEMP: "float64", Parameter.RHUM: "Int64"}

    mocker.patch("meteostat.fetcher.PARAMETER_DTYPES", PARAMETER_DTYPES)

    df = set_dtypes(df, parameters)

    assert df[Parameter.TEMP].dtype == "float64"
    assert df[Parameter.RHUM].dtype == "Int64"


def test_stations_to_df():
    """
    It should convert a list of weather stations into a DataFrame
    """
    stations = [
        {
            "id": "123",
            "name": {"en": "Station 1"},
            "country": "US",
            "location": {"latitude": 40.7128, "longitude": -74.0060, "elevation": 10},
            "timezone": "America/New_York",
        },
        {
            "id": "456",
            "name": {"en": "Station 2"},
            "country": "CA",
            "location": {"latitude": 45.4215, "longitude": -75.6972, "elevation": 100},
            "timezone": "America/Toronto",
        },
    ]

    df = stations_to_df(stations)

    expected_df = pd.DataFrame.from_records(
        [
            {
                "id": "123",
                "name": "Station 1",
                "country": "US",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "elevation": 10,
                "timezone": "America/New_York",
            },
            {
                "id": "456",
                "name": "Station 2",
                "country": "CA",
                "latitude": 45.4215,
                "longitude": -75.6972,
                "elevation": 100,
                "timezone": "America/Toronto",
            },
        ],
        index="id",
    )

    pd.testing.assert_frame_equal(df, expected_df)
