import pandas as pd
from meteostat.data.point import Point
from meteostat.types import Station

class Collection:
    """
    A class for storing meteorological data
    """
    _df = pd.DataFrame()
    _stations: list[Station] = []
    _point: Point | None = None
    _squash = True

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def homogenize(elevation: int):
        """
        Pretend all stations in this collection were on the same altitude
        """
        pass

    def join(self):
        """
        Join data from all sources
        """
        pass

    def copyright() -> str:
        print('(C) DWD')

    def fetch(self, squash = True) -> pd.DataFrame:
        return self._df