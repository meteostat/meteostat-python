import pandas as pd
from requests import get, HTTPError, Timeout
from meteostat import settings
from meteostat.utils.cache import cache
from meteostat.types import Station
from meteostat.utils.stations import get_distance


class StationsService:
    """
    """
    _columns = [
        "id",
        "latitude",
        "longitude"
    ]

    @staticmethod
    @cache(60 * 60 * 24, 'pickle')
    def _get_locations() -> pd.DataFrame | None:
        for mirror in settings.stations_locations_mirrors:
            try:  
                df = pd.read_csv(mirror, compression='gzip', names=StationsService._columns)
                return df.set_index(StationsService._columns[0])
            except (HTTPError, Timeout):
                continue
        return None
    
    def meta(self, id: str) -> Station | None:
        """
        Get meta data for a specific weather station
        """
        # Get all meta data mirrors
        mirrors = settings.stations_meta_mirrors
        # Get meta data for weather station
        for mirror in mirrors:
            try:  
                with get(mirror.format(id=id)) as res:
                    if res.status_code == 200:
                        return res.json()
            except (HTTPError, Timeout):
                continue
        # If meta data could not be found, return None
        return None
    
    def nearby(self, latitude: float, longitude: float, radius: float = None, limit: int = None) -> pd.DataFrame | None:
        df = self._get_locations()
        if df is None:
            return None

        # Get distance for each station
        df["distance"] = get_distance(
            latitude, longitude, df["latitude"], df["longitude"]
        )

        # Filter by radius
        if radius:
            df = df[df["distance"] <= radius]

        # Sort stations by distance
        df.columns.str.strip()
        df = df.sort_values("distance")

        return df

stations = StationsService()