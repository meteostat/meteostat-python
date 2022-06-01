"""
Example: Hourly point data performance

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

if __name__ == "__main__":

    from timeit import default_timer as timer

    # Get start time
    s = timer()

    # Run script
    from datetime import datetime
    from meteostat import Hourly

    Hourly.cores = 12

    start = datetime(1960, 1, 1)
    end = datetime(2021, 1, 1, 23, 59)

    data = Hourly("10637", start, end, timezone="Europe/Berlin")
    data = data.fetch()

    # Get end time
    e = timer()

    # Print performance
    print(e - s)
