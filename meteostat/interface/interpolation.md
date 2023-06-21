# Interpolation

## Concept

```py
nearby_stations = nearby(50, 8, limit=10)
ts = hourly(nearby_stations, '2020-01-01 20:00:00', parameters=['temp'])
ts = ts.homogenize(320)
model = SpatialModel(ts)
ts = model.interpolate(50, 8, 320)
```