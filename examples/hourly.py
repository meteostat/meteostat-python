from datetime import date
import meteostat as ms

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# ms.config.set('user_agent', 'myapp', context=ms.Provider.METNO_FORECAST)
# ms.config.get('user_agent', context=ms.Provider.METNO_FORECAST)
# ms.config.get_env_name('user_agent', context=ms.Provider.METNO_FORECAST)

ts = ms.hourly(
    "10637", start=date(2021, 1, 1), end=date(2021, 1, 2)
)
df = ts.fetch()

print(df)
