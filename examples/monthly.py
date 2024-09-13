from datetime import date
import logging

from matplotlib import pyplot as plt
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)

ms.settings["bulk_load_sources"] = True

ts = ms.monthly(
    "10637",
    date(2023, 1, 1),
    date(2023, 12, 31),
    providers=[ms.Provider.DWD_MONTHLY],
)

ts.fetch()[["tmin", "tmax", "tamn", "tamx"]].plot()
plt.show()
