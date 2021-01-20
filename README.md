# Meteostat Python Package

The Meteostat Python library provides a simple API for accessing open weather and climate data. The historical observations and statistics are collected by the [Meteostat project](https://meteostat.net/en) from different public interfaces, most of which are governmental.

Among the data sources are national weather services like the National Oceanic and Atmospheric Administration (NOAA) and Germany's national meteorological service (DWD).

## Installation

The Meteostat Python package is available through [PyPI](https://pypi.org/project/meteostat/):

```
pip install meteostat
```

Meteostat **requires Python 3.5** or higher.

## Documentation

The Meteostat Python library is divided into multiple classes which provide access to the actual data. The [documentation](https://dev.meteostat.net/python/) covers all aspects of the library:

* [Weather Stations](https://dev.meteostat.net/python/stations.html)
* [Hourly Data](https://dev.meteostat.net/python/hourly.html)
* [Daily Data](https://dev.meteostat.net/python/daily.html)
* [Contributing](https://dev.meteostat.net/python/contributing.html)

## Example

Let's pretend you want to plot temperature data for Vancouver, BC from 2018:

```python
# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily

# Set coordinates of Vancouver
lat = 49.2497
lon = -123.1193

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Get closest weather station to Vancouver, BC
stations = Stations()
stations = stations.nearby(lat, lon)
stations = stations.inventory('daily', (start, end))
station = stations.fetch(1)

# Get daily data for 2018 at the selected weather station
data = Daily(station, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
```

Take a look at the expected output:

![2018 temperature data for Vancouver, BC](https://dev.meteostat.net/assets/img/py-example-chart.046f8b8e.png)

## Contributing

Instructions on building and testing the Meteostat Python package can be found in the [documentation](https://dev.meteostat.net/python/contributing.html). More information about the Meteostat bulk data interface is available [here](https://dev.meteostat.net/bulk/).

If you want to support the project financially, you can make a donation via:

* [Patreon](https://www.patreon.com/meteostat)
* [PayPal](https://paypal.me/meteostat)

## Data License

Meteorological data is provided under the terms of the [Creative Commons Attribution-NonCommercial 4.0 International Public License](https://creativecommons.org/licenses/by-nc/4.0/legalcode). Please be aware that Meteostat uses data which is shared under [WMO resolution 40](https://www.wmo.int/pages/prog/www/ois/Operational_Information/Publications/Congress/Cg_XII/res40_en.html).

All meteorological data sources used by the Meteostat project are listed [here](https://dev.meteostat.net/docs/sources.html).

## Code License

The code of this library is available under the [MIT license](https://opensource.org/licenses/MIT).
