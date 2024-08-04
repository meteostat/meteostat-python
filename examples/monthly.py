from datetime import date
import logging
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)

ts = ms.monthly(
    "10637",
    date(2022, 1, 1),
    date(2022, 12, 31),
    providers=[ms.Provider.BULK_MONTHLY_DERIVED],
)

print(len(ts.fetch()))
