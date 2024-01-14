from datetime import date
import logging
import meteostat as ms

# ms.purge_cache(0)

logging.basicConfig(level=logging.INFO)

ts = ms.daily(
    "10637",
    date(2020, 1, 1),
    date(2020, 1, 31),
    parameters=(ms.Parameter.TAVG,),
    providers=(ms.Provider.NOAA_GHCND,),
)

print(ts.fetch(squash=False, fill=True))
