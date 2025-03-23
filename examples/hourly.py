from datetime import date
import meteostat as ms

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

ts = ms.hourly("10637", start=date(2021, 1, 1), end=date(2021, 1, 2), providers=[ms.Provider.DWD_HOURLY])
df = ts.fetch()

print(df)
