import meteostat as ms

ts = ms.normals(
    "01001",
    2010,
    2020,
)

# TODO: Make fetch squashable
print(ts.fetch(squash=False))
