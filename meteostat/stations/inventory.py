import pandas as pd
from meteostat.stations.database import query_inventory


def inventory(station: str) -> pd.DataFrame:
    """
    Get inventory records for a single weather station
    """
    return query_inventory(
        """
        SELECT * FROM `inventory` WHERE `station` LIKE ?
        """,
        index_col=['station', 'provider', 'parameter'],
        params=(station,),
    )
