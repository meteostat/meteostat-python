from datetime import date
import meteostat as ms

START = date(date.today().year - 3, 1, 1)
END = date.today()
PROVIDERS = [
    ms.Provider.GHCND,
    ms.Provider.DWD_DAILY,
    ms.Provider.BULK_DAILY_DERIVED
]


def test_bulk_daily():
    ms.settings.cache_enable = False

    ts = ms.daily("01001", start=START, end=END, providers=PROVIDERS, lite=False)

    df = ts.fetch()
    sourcemap = ts.sourcemap

    assert "tmin" in df
    assert "prcp" in df
    assert "tmin" in sourcemap
    assert "prcp" in sourcemap
    assert len(df.index.get_level_values("time").year.unique()) == 4
    assert sourcemap["tmin"].str.contains(ms.Provider.GHCND).any()
