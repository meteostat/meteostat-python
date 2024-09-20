from datetime import date
import meteostat as ms

START = date(date.today().year - 3, 1, 1)
END = date.today()
PROVIDERS = [
    ms.Provider.SYNOP,
    ms.Provider.METAR,
    ms.Provider.MODEL,
    ms.Provider.ISD_LITE,
    ms.Provider.DWD_HOURLY,
    ms.Provider.ECCC_HOURLY,
]


def test_daily_hourly():
    ms.settings["cache_enable"] = False

    ts = ms.hourly("10637", start=START, end=END, providers=PROVIDERS, lite=False)

    df = ts.fetch()
    sourcemap = ts.sourcemap

    assert "temp" in df
    assert "prcp" in df
    assert "temp" in sourcemap
    assert "prcp" in sourcemap
    assert len(df.index.get_level_values("time").year.unique()) == 4
    assert sourcemap["temp"].str.contains(ms.Provider.DWD_HOURLY).any()
