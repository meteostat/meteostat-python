from datetime import datetime
from meteostat import settings
from meteostat.providers.noaa.ghcnd import fetch
from meteostat.typing import QueryDict


def test_noaa_ghcnd():
    """
    It should load data from NOAA GHCND
    """
    settings.cache_enable = False

    query: QueryDict = {
        "start": datetime(2021, 2, 1, 15),
        "end": datetime(2022, 2, 1, 17),
        "station": {"id": "10637", "identifiers": {"ghcn": "GMW00035032"}},
    }
    df = fetch(query)

    assert len(df) > 1
    assert "tavg" in df
    assert "prcp" in df
