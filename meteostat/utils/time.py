from typing import Optional
from datetime import datetime

def parse_time(value: str | datetime | None, start: Optional[datetime] = None) -> datetime:
    """
    Convert a given date/time input to datetime

    To set the time of a date-only string to 23:59:59, pass is_end=True
    """
    if start and isinstance(value, str) and len(value) == 10:
        value = f'{value} 23:59:59'

    if start and not value:
        return datetime(start.year, start.month, start.day, 23, 59, 59)

    return value if isinstance(value, datetime) else datetime.fromisoformat(value)