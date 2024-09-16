from datetime import datetime
import os

import pandas as pd
import meteostat as ms


def test_daily(mocker):
    """
    It returns a filtered DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.data.daily.fetch")

    mock_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_daily.pickle",
        )
    )
    ts = ms.daily("01001", datetime(2020, 1, 5), datetime(2020, 1, 10))
    df = ts.fetch()

    assert len(df) == 6
    assert df.iloc[0]["tavg"] == 1.3


def test_daily_none(mocker):
    """
    It returns None if provider returns an empty DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.data.daily.fetch")
    mock_fetch.return_value = pd.DataFrame()
    ts = ms.daily("10637", datetime(2024, 1, 1), datetime(2024, 1, 5))
    assert ts.fetch() is None
