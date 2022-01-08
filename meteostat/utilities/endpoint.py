"""
Utilities - Endpoint Helpers

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from typing import Union
from meteostat.enumerations.granularity import Granularity


def generate_endpoint_path(
        granularity: Granularity,
        station: str,
        model: bool = True,
        year: Union[int, None] = None
) -> str:
    """
    Generate Meteostat Bulk path
    """

    # Base path
    path = f"{granularity.value}/"

    if granularity != Granularity.NORMALS:
        if model:
            path += 'full/'
        else:
            path += 'obs/'

    if Granularity.HOURLY and year:
        path += f"{year}/"

    return f"{path}{station}.csv.gz"
