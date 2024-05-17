from datetime import date, datetime
import logging
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)
ms.settings.bulk_load_sources = True

ts = ms.daily(
    "10637",
    datetime(2024, 1, 1, 0),
    datetime(2024, 1, 31, 23),
    providers=[ms.Provider.BULK_DAILY_DERIVED],
)
print(ts)
exit()

# ms.purge_cache(0)

logging.basicConfig(level=logging.INFO)

ts = ms.daily(
    "10637",
    date(2020, 1, 1),
    date(2020, 1, 31),
    parameters=(ms.Parameter.TAVG,),
    providers=(ms.Provider.GHCND,),
)

print(ts.fetch(squash=False, fill=True))
