from datetime import datetime
from meteostat import settings
from meteostat.providers.meteostat.model import fetch
from meteostat.typing import QueryDict


def test_meteostat_model():
    """
    It should load model data from Meteostat
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
    assert "prcp" in df
