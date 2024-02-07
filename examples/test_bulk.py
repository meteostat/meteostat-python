from datetime import date
import meteostat as ms


START = date(2023, 1, 1)
END = date(2022, 12, 31) #date.today()
PROVIDERS = (
    ms.Provider.SYNOP,
    ms.Provider.METAR,
    ms.Provider.MOSMIX,
    ms.Provider.ISD_LITE,
    ms.Provider.DWD_HOURLY,
)

ms.settings.cache_enable = False

ts = ms.hourly("00TG6", providers=PROVIDERS)

df = ts.fetch()

print(df, ts.sourcemap)