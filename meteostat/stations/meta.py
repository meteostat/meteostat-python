from meteostat.stations.database import query
from meteostat.typing import Station


def _get_station(id: str) -> dict:
    """
    Get key meta data for a weather station by ID
    """
    return query(
        """
        SELECT
            `id`,
            `country`,
            `region`,
            `latitude`,
            `longitude`,
            `elevation`,
            `timezone`
        FROM
            `stations`
        WHERE
            `id` LIKE ?
        """,
        params=(id,),
    ).to_dict("records")[0]


def _get_names(id: str) -> dict:
    """
    Get dict of weather station names in different languages by station ID
    """
    names = query(
        f"SELECT `language`, `name` FROM `names` WHERE `station` LIKE ?", params=(id,)
    ).to_dict("records")
    return {name["language"]: name["name"] for name in names}


def _get_identifers(id: str) -> dict:
    """
    Get dict of weather station identifers by station ID
    """
    identifiers = query(
        f"SELECT `key`, `value` FROM `identifiers` WHERE `station` LIKE ?", params=(id,)
    ).to_dict("records")
    return {identifier["key"]: identifier["value"] for identifier in identifiers}


def meta(id: str) -> Station | None:
    """
    Get meta data for a specific weather station
    """
    try:
        station = _get_station(id)

        return {
            "id": station["id"],
            "name": _get_names(id),
            "country": station["country"],
            "region": station["region"],
            "identifiers": _get_identifers(id),
            "location": {
                "latitude": station["latitude"],
                "longitude": station["longitude"],
                "elevation": station["elevation"],
            },
            "timezone": station["timezone"],
        }
    except IndexError:
        return None
