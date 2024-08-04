from datetime import date
import os

import pandas as pd
import meteostat as ms


def test_monthly_derived(mocker):
    """
    It uses daily data to aggregate monthly averages
    """
    mock_fetch = mocker.patch("meteostat.providers.bulk.daily.fetch")

    mock_fetch.return_value = pd.read_pickle(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "fixtures",
            "df_monthly_derived.pickle",
        )
    )
    ts = ms.monthly(
        "10637",
        date(2022, 1, 1),
        date(2022, 12, 31),
        providers=[ms.Provider.BULK_MONTHLY_DERIVED],
    )
    df = ts.fetch()

    assert len(df) == 12
    assert df.iloc[0]["tavg"] == 3.8


def test_monthly_derived_none(mocker):
    """
    It returns None if daily data provider returns an empty DataFrame
    """
    mock_fetch = mocker.patch("meteostat.providers.bulk.daily.fetch")
    mock_fetch.return_value = pd.DataFrame()
    ts = ms.monthly(
        "10637",
        date(2022, 1, 1),
        date(2022, 12, 31),
        providers=[ms.Provider.BULK_MONTHLY_DERIVED],
    )
    assert ts.fetch() is None
