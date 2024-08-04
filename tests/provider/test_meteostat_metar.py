from datetime import datetime
from meteostat import settings
from meteostat.providers.meteostat.metar import fetch
from meteostat.typing import QueryDict


def test_meteostat_metar():
    """
    It should load METAR data from Meteostat
    """
    settings["cache_enable"] = False

    query: QueryDict = {
        "start": datetime(2020, 2, 1, 15),
        "end": datetime(2020, 2, 1, 17),
        "station": {"id": "10637"},
    }
    df = fetch(query)

    assert len(df) > 1
    assert "temp" in df
    assert "rhum" in df
