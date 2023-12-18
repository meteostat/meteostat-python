# Interpolation

## Concept

```py
import meteostat as ms

point = (50, 8)

stations = ms.stations.nearby(*point)

ts = ms.hourly(stations)

df = ts.interpolate(*point, 320)
```