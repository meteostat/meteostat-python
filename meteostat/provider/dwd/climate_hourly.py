from datetime import datetime
from meteostat.types import Station

def handler(station: Station, start: datetime, end: datetime):
    print(station, start, end)