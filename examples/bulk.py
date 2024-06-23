from datetime import date
import meteostat as ms

"""
Set start & end date
"""
START = date(date.today().year - 1, 1, 1)
END = date.today()

"""
Define included providers (should be all available providers)
"""
PROVIDERS = [
    ms.Provider.BULK_DAILY_DERIVED,
    ms.Provider.GHCND,
    ms.Provider.DWD_DAILY,
]

ts = ms.daily('10637', start=START, end=END, providers=PROVIDERS, lite=False)

print(ts.fetch())
print(ts.sourcemap)
exit()



# START = date(2023, 1, 1)
# END = date(2022, 12, 31)  # date.today()
# PROVIDERS = (
#     ms.Provider.SYNOP,
#     ms.Provider.METAR,
#     # ms.Provider.MODEL,
#     # ms.Provider.ISD_LITE,
#     # ms.Provider.DWD_HOURLY,
# )

# ms.settings.cache_enable = False

# ts = ms.hourly("10635", start=START, providers=PROVIDERS)

# df = ts.sourcemap

# df["year"] = df.index.get_level_values("time").year
# df["month"] = df.index.get_level_values("time").month
# df["day"] = df.index.get_level_values("time").day
# df["hour"] = df.index.get_level_values("time").hour

# df = df.set_index(["year", "month", "day", "hour"])
# df = df[~df.index.duplicated(keep="first")]

# print(df)
