"""Water v1.2 terrain mask: slope, HAND and the 'not assessable' bookkeeping. Offline: synthetic DEMs."""
import numpy as np
import pytest

pytest.importorskip("rasterio")

from evideo import terrain as T  # noqa: E402
from evideo.data import cog  # noqa: E402
from evideo.instruments import get  # noqa: E402
from evideo.models import Intent, TileStatus  # noqa: E402

from test_instruments import SHAPE, W, FakeProvider, Selection, flood_db, job, scene, use  # noqa: E402


def v_valley(n=61, slope=0.1, res=30.0):
    """Channel down the middle column flowing south; both banks rise `slope` m per m."""
    x = (np.arange(n) - n // 2) * res
    dem = np.abs(x)[None, :] * slope + (np.arange(n)[::-1] * 0.01)[:, None]   # tiny fall to the south edge
    return dem.astype("float32")


def test_hand_is_height_above_channel():
    dem = v_valley()
    r = T.hand_from_dem(dem, 30.0, channel_km2=0.05)
    hand = r["hand"]
    mid = dem.shape[1] // 2
    assert np.nanmax(hand[:, mid]) < 0.5                       # channel cells sit on the channel
    row = 20
    # 10 cells (300 m) from the channel at 0.1 m/m = about 30 m above it
    assert hand[row, mid + 10] == pytest.approx(30.0, abs=1.5)
    assert hand[row, mid - 10] == pytest.approx(30.0, abs=1.5)
    assert r["channels"][:, mid].mean() > 0.8


def test_hand_survives_a_pit_and_is_deterministic():
    dem = v_valley()
    dem[25:28, 40:43] -= 8.0                                     # an unconditioned DEM pit on a bank
    a, b = T.hand_from_dem(dem, 30.0, 0.05), T.hand_from_dem(dem, 30.0, 0.05)
    assert np.isfinite(a["hand"][26, 41]) and np.array_equal(a["hand"], b["hand"], equal_nan=True)


def test_hand_nan_when_no_channel_is_reached():
    ramp = (np.arange(40)[:, None] * 0.5 + np.zeros((40, 40))).astype("float32")   # drains off the edge, 30 m cells
    r = T.hand_from_dem(ramp, 30.0, channel_km2=50.0)
    assert r["unknown_share"] == 1.0 and not np.isfinite(r["hand"]).any()


def test_slope_degrees():
    dem = (np.arange(30)[None, :] * 10.0 + np.zeros((30, 30))).astype("float32")   # 10 m per 20 m = 26.6 degrees
    assert np.nanmedian(T.slope_deg(dem, 20.0)) == pytest.approx(26.57, abs=0.1)


def test_missing_terrain_is_never_excluded():
    slope = np.array([[np.nan, 9.0], [1.0, 1.0]], "float32")
    hand = np.array([[np.nan, np.nan], [np.nan, 30.0]], "float32")
    ok, st = T.assessable_mask(slope, hand)
    assert ok[0, 0] and not ok[0, 1] and ok[1, 0]                # NaN kept, steep dropped
    assert ok[1, 1]                                              # one isolated high-HAND pixel is eroded away
    assert st["steep_share"] == 0.25 and st["terrain_known_share"] == 0.75


def hill_reader(steep_frac=0.4):
    """DEM for a tile whose left `steep_frac` of columns is a 31-degree hillside; the rest is flat."""
    def reader(crs, bounds, shape):
        l, b, r, t = bounds
        x = l + (np.arange(shape[1]) + 0.5) * (r - l) / shape[1]
        xs = l + (r - l) / 3 * (1 + steep_frac)                   # the tile occupies the middle third
        z = np.where(x < xs, (xs - x) * 0.6, 0.0)
        return np.tile(z, (shape[0], 1)).astype("float32")
    return reader


def test_terrain_for_tile_masks_the_hillside():
    bounds = (500000.0, 2900000.0, 505000.0, 2905500.0)
    out = T.terrain_for_tile("EPSG:32646", bounds, SHAPE, {}, dem_reader=hill_reader(0.4))
    ok = out["assessable"]
    assert ok[:, : int(0.3 * SHAPE[1])].mean() < 0.05            # hillside not assessable
    assert ok[:, int(0.5 * SHAPE[1]):].mean() > 0.95             # flat ground assessable
    assert out["stats"]["steep_share"] == pytest.approx(0.4, abs=0.08)


def _run(tcfg=None, reader=None, monkeypatch=None):
    s = scene("S1_after", "S1", "2024-07-11")
    p = use(FakeProvider([Selection(True, "S1", s, "monsoon month, radar first")], {("S1_after", "vv"): flood_db(0.4)}))
    if tcfg is not None:
        p.cfg["terrain"] = tcfg
    if reader is not None:
        monkeypatch.setattr(cog, "read_dem_on_grid", reader)
    return get("sar_water_otsu")[1](job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")]))


def test_shadow_on_a_hillside_is_not_counted_as_water(identity_calibration, monkeypatch):
    # The dark 40% of this tile is exactly the hillside: radar shadow, not flood water.
    off = _run(monkeypatch=monkeypatch)
    assert "terrain" not in off.params and off.value == pytest.approx(0.4 * off.params["measured_km2"], rel=0.05)
    on = _run({"enabled": True}, hill_reader(0.4), monkeypatch)
    assert on.status == TileStatus.ok
    assert on.value < 0.05 * on.params["measured_km2"] + 0.05
    assert on.params["terrain"]["applied"] and on.params["not_assessable_km2"] > 0.3 * off.params["measured_km2"]
    assert on.params["measured_km2"] < 0.75 * off.params["measured_km2"]


def test_real_flooding_on_flat_ground_survives_the_mask(identity_calibration, monkeypatch):
    flat = lambda crs, bounds, shape: np.zeros(shape, "float32") + np.linspace(0, 1, shape[0])[:, None].astype("float32")  # noqa: E731
    base = _run(monkeypatch=monkeypatch)
    on = _run({"enabled": True}, flat, monkeypatch)
    assert on.status == TileStatus.ok and on.params["terrain"]["applied"]
    assert on.value == pytest.approx(base.value, rel=0.05)
    assert on.params["terrain"]["not_assessable_share"] < 0.02


def test_dem_failure_falls_back_and_says_so(identity_calibration, monkeypatch):
    def boom(crs, bounds, shape):
        raise OSError("dem host unreachable")
    r = _run({"enabled": True}, boom, monkeypatch)
    assert r.status == TileStatus.ok and r.params["terrain"]["applied"] is False
    assert "dem host unreachable" in r.params["terrain"]["error"]


def test_dem_tile_urls_cross_a_degree_boundary():
    urls = cog.dem_tile_urls((90.98, 26.3, 91.02, 26.35))
    assert len(urls) == 2 and any("E090_00" in u for u in urls) and any("E091_00" in u for u in urls)
    assert "Copernicus_DSM_COG_10_N26_00_E091_00_DEM.tif" in cog.dem_tile_urls((91.0, 26.3, 91.05, 26.35))[0]
