from datetime import date
import logging

from matplotlib import pyplot as plt
import meteostat as ms

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s [%(filename)s:%(lineno)s] %(message)s"
)

# ms.settings["load_sources"] = True

ts = ms.monthly(
    "10637",
    date(2022, 1, 1),
    date(2022, 12, 31),
    providers=[ms.Provider.MONTHLY_DERIVED],
)

print(ts.fetch())
exit()
plt.show()
