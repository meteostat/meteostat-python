"""
Example: Request with source flags

Meteorological data provided by Meteostat (https://dev.meteostat.net)
under the terms of the Creative Commons Attribution-NonCommercial
4.0 International Public License.

The code is licensed under the MIT license.
"""

from datetime import datetime
from meteostat import Daily

# Time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31)

data = Daily("10637", start, end, flags=True)
df = data.fetch()

# Print DataFrame
print(df)
