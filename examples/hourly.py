from datetime import date
import meteostat as ms

ts = ms.hourly(
    "10637", start=date(2021, 1, 1), end=date(2021, 1, 2)
)
df = ts.fetch()

print(df)
