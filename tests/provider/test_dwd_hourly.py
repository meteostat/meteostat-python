from datetime import datetime
from meteostat import settings, Parameter
from meteostat.providers.dwd.hourly import fetch
from meteostat.typing import QueryDict


def test_dwd_hourly():
    """
    It should load data from DWD Open Data (hourly)
    """
    settings["cache_enable"] = False

    query: QueryDict = {
        "start": datetime(2000, 2, 1, 15),
        "end": datetime(2000, 2, 1, 17),
        "station": {"id": "10637", "identifiers": {"national": "01420"}},
        "parameters": [Parameter.TEMP, Parameter.PRCP],
    }
    df = fetch(query)

    assert len(df) > 1
    assert "temp" in df
    assert "prcp" in df
