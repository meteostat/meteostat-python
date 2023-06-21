from typing import Optional
from datetime import datetime

def parse_time(value: str | datetime, is_end: Optional[bool] = False) -> datetime:
    """
    Convert a given date/time input to datetime

    To set the time of a date-only string to 23:59:59, pass is_end=True
    """
    if is_end and isinstance(value, str) and len(value) == 10:
        value = f'{value} 23:59:59'

    return value if isinstance(value, datetime) else datetime.fromisoformat(value)