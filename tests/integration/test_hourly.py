from datetime import datetime
import os

import pandas as pd
import meteostat as ms


def test_hourly(mocker):
    """
    It returns a filtered DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.data.hourly.fetch")

    mock_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_hourly.pickle",
        )
    )
    ts = ms.hourly("10637", datetime(2020, 1, 1, 15), datetime(2020, 1, 1, 17))
    df = ts.fetch()

    assert len(df) == 3
    assert df.iloc[0]["temp"] == 3.6


def test_hourly_timezone(mocker):
    """
    It should consider the timezone when filtering the DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.data.hourly.fetch")

    mock_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_hourly.pickle",
        )
    )
    ts = ms.hourly(
        "10637",
        datetime(2020, 1, 1, 15),
        datetime(2020, 1, 1, 17),
        timezone="Europe/Berlin",
    )
    df = ts.fetch()

    assert len(df) == 3
    assert df.iloc[0]["temp"] == 4.3


def test_hourly_none(mocker):
    """
    It returns None if provider returns an empty DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.data.hourly.fetch")
    mock_fetch.return_value = pd.DataFrame()
    ts = ms.hourly("10637", datetime(2024, 1, 1, 15), datetime(2024, 1, 1, 17))
    assert ts.fetch() is None


def test_hourly_multiple(mocker):
    """
    It should handle data from multiple providers
    """
    mock_metar_fetch = mocker.patch("meteostat.providers.meteostat.metar.fetch")
    mock_model_fetch = mocker.patch("meteostat.providers.meteostat.model.fetch")
    mock_synop_fetch = mocker.patch("meteostat.providers.meteostat.synop.fetch")
    mock_metar_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_metar.pickle",
        )
    )
    mock_model_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_model.pickle",
        )
    )
    mock_synop_fetch.return_value = None

    ts = ms.hourly(
        "10637",
        datetime(2023, 2, 1, 3),
        datetime(2023, 2, 1, 21),
        providers=[ms.Provider.METAR, ms.Provider.MODEL, ms.Provider.SYNOP],
    )
    df = ts.fetch()
    sources = ts.sourcemap

    assert len(df) == 19
    assert len(sources) == 19
    assert "metar" in sources["temp"].values
    assert "model" not in sources["temp"].values
    assert "metar" not in sources["prcp"].values
    assert "model" in sources["prcp"].values
    assert df["temp"].mean().round() == 7
    assert df["prcp"].sum().round() == 1
