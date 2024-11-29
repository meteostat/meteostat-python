from datetime import date, datetime
import logging
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)
ms.settings["load_sources"] = True

ts = ms.daily(
    "01001",
    datetime(2020, 1, 5),
    datetime(2020, 1, 10),
    providers=[ms.Provider.DAILY],
)
print(ts.fetch())
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
