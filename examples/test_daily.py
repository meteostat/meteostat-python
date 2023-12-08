import logging
import meteostat as ms

# ms.purge_cache(0)

logging.basicConfig(level=logging.INFO)

ts = ms.daily(
    "10637",
    "2020-01-01",
    "2020-01-31",
    parameters=[ms.Parameter.TAVG],
    providers=[ms.Provider.NOAA_GHCND],
)

ts.fetch(squash=False, fill=True)
