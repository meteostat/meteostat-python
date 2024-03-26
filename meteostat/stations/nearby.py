from meteostat.point import Point
from meteostat.stations.database import query_stations


def nearby(point: Point, radius=50000, limit=100) -> list[str] | None:
    """
    Get a list of weather station IDs ordered by distance
    """
    return query_stations(
        """
        SELECT
            `id`,
            `names`.`name` as `name`,
            `country`,
            `region`,
            `latitude`,
            `longitude`,
            `elevation`,
            `timezone`,
            ROUND(
                (
                    6371000 * acos(
                        cos(radians(:lat)) * cos(radians(`latitude`)) * cos(radians(`longitude`) - radians(:lon)) + sin(radians(:lat)) * sin(radians(`latitude`))
                    )
                ),
                1
            ) AS `distance`
        FROM
            `stations`
            INNER JOIN `names` ON `stations`.`id` = `names`.`station`
            AND `names`.`language` = "en"
        WHERE
            `distance` <= :radius
        ORDER BY
            `distance`
        LIMIT
            :limit
        """,
        index_col="id",
        params={
            "lat": point.latitude,
            "lon": point.longitude,
            "radius": radius,
            "limit": limit,
        },
    )
