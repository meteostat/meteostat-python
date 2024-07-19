from datetime import date
import logging
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)
ms.settings.bulk_load_sources = True

ts = ms.monthly(
    "01001",
    date(2020, 1, 1),
    date(2020, 4, 30),
    providers=[ms.Provider.BULK_MONTHLY_DERIVED],
)

print(ts.fetch(sources=True))
