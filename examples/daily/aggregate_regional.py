"""
Example: Spatial aggregation

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

if __name__ == "__main__":

    from datetime import datetime
    import matplotlib.pyplot as plt
    from meteostat import Stations, Daily

    # Configuration
    Daily.cores = 12

    # Time period
    start = datetime(1980, 1, 1)
    end = datetime(2019, 12, 31)

    # Get random weather stations in the US
    stations = Stations()
    stations = stations.region("US")
    stations = stations.inventory("daily", (start, end))
    stations = stations.fetch(limit=150, sample=True)

    # Get daily data
    data = Daily(stations, start, end)

    # Normalize & aggregate
    data = data.normalize().aggregate("1Y", spatial=True).fetch()

    # Chart title
    TITLE = "Average US Annual Temperature from 1980 to 2019"

    # Plot chart
    data.plot(y=["tavg"], title=TITLE)
    plt.show()
