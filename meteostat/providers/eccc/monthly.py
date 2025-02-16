from typing import Optional
import pandas as pd
import requests

from meteostat.enumerations import TTL, Parameter
from meteostat.utils.decorators import cache
from meteostat.providers.eccc.shared import ENDPOINT, get_meta_data
from meteostat.typing import QueryDict

BATCH_LIMIT = 9000
PROPERTIES = {
    "LOCAL_DATE": "time",
    "MAX_TEMPERATURE": Parameter.TXMX,
    "MEAN_TEMPERATURE": Parameter.TEMP,
    "MIN_TEMPERATURE": Parameter.TXMN,
    "TOTAL_PRECIPITATION": Parameter.PRCP,
    "DAYS_WITH_PRECIP_GE_1MM": Parameter.PDAY,
    "TOTAL_SNOWFALL": Parameter.SNOW,
}


@cache(TTL.WEEK, "pickle")
def get_df(
    climate_id: str,
) -> Optional[pd.DataFrame]:
    response = requests.get(
        f"{ENDPOINT}/collections/climate-monthly/items",
        params={
            "CLIMATE_IDENTIFIER": climate_id,
            "f": "json",
            "properties": ",".join(PROPERTIES.keys()),
            "limit": BATCH_LIMIT,
        },
    )

    data = response.json()

    # Extract features from the response
    features = map(
        lambda feature: feature["properties"] if "properties" in feature else {},
        data.get("features", []),
    )

    # Create a DataFrame from the extracted features
    df = pd.DataFrame(features)
    df = df.rename(columns=PROPERTIES)

    # Handle time column & set index
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index(["time"])

    return df


def fetch(query: QueryDict) -> Optional[pd.DataFrame]:
    if not "national" in query["station"]["identifiers"]:
        return None

    meta_data = get_meta_data(query["station"]["identifiers"]["national"])
    climate_id = meta_data.get("CLIMATE_IDENTIFIER")

    if not climate_id:
        return None

    return get_df(climate_id)
