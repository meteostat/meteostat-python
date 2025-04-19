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
    year: Union[int, None] = None,
    map_file: bool = False,  # Is a source map file?
) -> str:
    """
    Generate Meteostat Bulk path
    """

    # Base path
    path = f"{granularity.value}/"

    if granularity in (Granularity.HOURLY, Granularity.DAILY) and year:
        path += f"{year}/"

    appendix = ".map" if map_file else ""

    return f"{path}{station}{appendix}.csv.gz"
