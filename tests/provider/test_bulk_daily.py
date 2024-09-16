from datetime import datetime
from meteostat import settings
from meteostat.providers.data.daily import fetch
from meteostat.typing import QueryDict


def test_data_daily():
    settings["cache_enable"] = False

    query: QueryDict = {
        "start": datetime(2020, 2, 1, 15),
        "end": datetime(2020, 2, 1, 17),
        "station": {"id": "01001"},
    }
    df = fetch(query)

    assert len(df) > 1
    assert "tmin" in df
    assert "prcp" in df
