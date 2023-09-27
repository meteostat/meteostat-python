from datetime import datetime
from meteostat import Stations, Hourly


def test_pandas_20():
    stations = Stations()
    stations = stations.nearby(49.2497, -123.1193)
    station = stations.fetch(1)

    start = datetime(2018, 1, 1)
    end = datetime(2018, 12, 31, 23, 59)

    data = Hourly(station, start=start, end=end)
    data = data.normalize()
    data = data.interpolate()
    data = data.fetch()

    assert len(data) > 0
