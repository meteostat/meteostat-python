import polars as pl

class Collection:
    """
    A class for storing meteorological data
    """
    _df: str

    def __init__(self, df: pl.DataFrame):
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