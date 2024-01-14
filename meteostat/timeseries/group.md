```py
import meteostat as ms

ts = ms.daily('10637', '1960-01-01', '1990-12-31')

df1 = ms.group.monthly(ts).agg('avg')
df2 = ms.group.normals(ts).agg('avg')
```