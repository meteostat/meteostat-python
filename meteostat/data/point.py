from typing import Optional

class Point:

    latitude: float = None
    longitude: float = None
    elevation: int = None

    def __init__(self, latitude: float, longitude: float, elevation: Optional[int] = None) -> None:
        if latitude < -90 or latitude > 90:
            raise Exception('Latitude must be between -90 and 90')
        
        if longitude < -180 or longitude > 180:
            raise Exception('Longitude must be between -180 and 180')

        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation