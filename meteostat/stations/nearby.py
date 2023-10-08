import polars as pl

def nearby(lat: float, lon: float) -> pl.DataFrame:
    """
    Get nearby weather stations for a geo location
    """