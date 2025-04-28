# Meteostat Python Package

The Meteostat Python library provides a simple API for accessing open weather and climate data. The historical observations and statistics are collected by [Meteostat](https://meteostat.net) from different public interfaces, most of which are governmental.

Among the data sources are national weather services like the National Oceanic and Atmospheric Administration (NOAA) and Germany's national weather service (DWD).

Are you looking for a **hosted solution**? Try our [JSON API](https://rapidapi.com/meteostat/api/meteostat/).

## Installation

The Meteostat Python package is available through [PyPI](https://pypi.org/project/meteostat/):

```sh
pip install meteostat
```

Meteostat **requires Python 3.6** or higher. If you want to visualize data, please install Matplotlib, too.

## Documentation

The Meteostat Python library is divided into multiple classes which provide access to the actual data. The [documentation](https://dev.meteostat.net/python/) covers all aspects of the library:

* **Selecting Locations**
  * [Geographical Point](https://dev.meteostat.net/python/point.html)
  * [Weather Stations](https://dev.meteostat.net/python/stations.html)
* **Time Series**
  * [Hourly Data](https://dev.meteostat.net/python/hourly.html)
  * [Daily Data](https://dev.meteostat.net/python/daily.html)
  * [Monthly Data](https://dev.meteostat.net/python/monthly.html)
* **Miscellaneous Data**
  * [Climate Normals](https://dev.meteostat.net/python/normals.html)
* **Library**
  * [Contributing](https://dev.meteostat.net/python/contributing.html)
  * [Formats & Units](https://dev.meteostat.net/formats.html)
  * [Data Sources](https://dev.meteostat.net/sources.html)
  * [Terms & License](https://dev.meteostat.net/terms.html)

## Example

Let's plot 2018 temperature data for Vancouver, BC:

```python
# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

# Create Point for Vancouver, BC
location = Point(49.2497, -123.1193, 70)

# Get daily data for 2018
data = Daily(location, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()
```

Take a look at the expected output:

![2018 temperature data for Vancouver, BC](https://dev.meteostat.net/assets/img/py-example-chart.046f8b8e.png)

## Contributing

Instructions on building and testing the Meteostat Python package can be found in the [documentation](https://dev.meteostat.net/python/contributing.html). More information about the Meteostat bulk data interface is available [here](https://dev.meteostat.net/bulk/).

## Donating

If you want to support the project financially, you can make a donation using one of the following services:

* [GitHub](https://github.com/sponsors/clampr)
* [Patreon](https://www.patreon.com/meteostat)
* [PayPal](https://www.paypal.com/donate?hosted_button_id=MQ67WRDC8EW38)

## Data License

Meteorological data is provided under the terms of the [Creative Commons Attribution-NonCommercial 4.0 International Public License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/legalcode). You may build upon the material
for any purpose, even commercially. However, you are not allowed to redistribute Meteostat data "as-is" for commercial purposes.

By using the Meteostat Python library you agree to our [terms of service](https://dev.meteostat.net/terms.html). All meteorological data sources used by the Meteostat project are listed [here](https://dev.meteostat.net/sources.html).

## Code License

The code of this library is available under the [MIT license](https://opensource.org/licenses/MIT).
