from typing import Optional

import requests

from meteostat.enumerations import TTL
from meteostat.utils.decorators import cache
from meteostat.core.logger import logger


ENDPOINT = "https://api.weather.gc.ca"


@cache(TTL.WEEK)
def get_meta_data(station: str) -> Optional[dict]:
    response = requests.get(
        f"{ENDPOINT}/collections/climate-stations/items",
        params={
            "STN_ID": station,
            "properties": ",".join(
                [
                    "CLIMATE_IDENTIFIER",
                    "TIMEZONE",
                    "HLY_FIRST_DATE",
                    "HLY_LAST_DATE",
                    "DLY_FIRST_DATE",
                    "DLY_LAST_DATE",
                    "MLY_FIRST_DATE",
                    "MLY_LAST_DATE",
                ]
            ),
            "f": "json",
        },
    )

    if response.status_code == 200:
        data = response.json()
        try:
            return data["features"][0]["properties"]
        except (IndexError, KeyError):
            logger.info(f"ECCC climate identifier for station {station} not found")
    else:
        logger.warning(
            f"ECCC climate identifier for station {station} not found (status: {response.status_code})"
        )

    return None
