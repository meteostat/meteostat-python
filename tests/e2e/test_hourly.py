from datetime import datetime
import meteostat as ms

def test_hourly():
    ts = ms.hourly("10637", datetime(2024, 1, 1, 15), datetime(2024, 1, 1, 17))
    df = ts.fetch()
    assert len(df) == 3