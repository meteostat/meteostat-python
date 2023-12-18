from datetime import datetime
import logging
import meteostat as ms

logging.basicConfig(level=logging.INFO)

nearby = ms.stations.nearby(50, 8, 10000, 4)

ts = ms.hourly(
    "01238",
    parameters=[ms.Parameter.TEMP],
    providers=[ms.Provider.SYNOP],
    lite=False,
)


print(ts.fetch(squash=False, fill=True))
