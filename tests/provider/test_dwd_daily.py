from datetime import datetime
from meteostat import settings, Parameter
from meteostat.providers.dwd.daily import fetch
from meteostat.typing import QueryDict


def test_dwd_daily():
    """
    It should load data from DWD Open Data (daily)
    """
    settings["cache_enable"] = False

    query: QueryDict = {
        "start": datetime(2000, 2, 1, 15),
        "end": datetime(2000, 2, 1, 17),
        "station": {
            "id": "10637",
            "identifiers": {"national": "01420"},
            "location": {"elevation": 111},
        },
        "parameters": [Parameter.TAVG, Parameter.PRCP],
    }
    df = fetch(query)

    assert len(df) > 1
    assert "tavg" in df
    assert "prcp" in df
