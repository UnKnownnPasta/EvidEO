"""Compare the Sentinel-1 instrument with NRSC's flood layer on the same pass, then test the area estimator on it.

Event        Assam, Sentinel-1D pass of 27 July 2026 (relative orbit 143). NRSC map 2026/FL/AS/33/27072026.
Instrument   classify_sar_water, the code used by the project's flood instrument, on 0.05 degree tiles at 20 m.
Flood        Primary: water on 27 July, minus water on the same orbit on 27 April 2026, minus NRSC's river layer.
             This mirrors NRSC's stated inputs (a pre-flood April image and a river layer). NRSC also uses a
             1:10,000 land-use layer that is not public, so the instrument cannot fully match it.
Terrain      The project's slope and HAND mask (5 degrees, 10 m). Comparison is limited to assessable pixels.
             A tile is "hill" when over half of it is not assessable.
Reference    NRSC is an analyst product marked "no ground verification". It is a comparison, not the truth.

Protocol, fixed before the first run:
  Report       total area ratio, pixel IoU and tile correlation, for all tiles and for plain tiles.
  Estimator    Treat NRSC as the label source. Sampling tiles at n = 25, 50, 100, 200, estimate NRSC's total from the
               instrument map using the difference and stratified difference estimators of ppi_pilot.py.
  Pass         At some n <= 100, a 95% interval covers NRSC's total at least 90% of the time with a median
               half-width of at most 50%.
  Reading      A pass shows the estimator survives a rare, spatially clumped class on a real event. It does not show
               either map is correct.

Run from the repo root: python research/flood_area/nrsc_compare.py <masks_dir> [workers]
Writes nrsc_compare_tiles.csv and nrsc_compare_results.json beside this script.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject, transform_bounds

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "backend"), str(Path(__file__).parent)]
from evideo import terrain as terrain_mod  # noqa: E402
from evideo.data.cog import read_window, sign_href  # noqa: E402
from evideo.instruments.water import classify_sar_water, db  # noqa: E402
from ppi_pilot import difference, make_strata, stratified_difference, stratified_sample  # noqa: E402

HERE = Path(__file__).parent
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
COLLECTION = "sentinel-1-rtc"
FLOOD_DATE = "2026-07-27T00:00:00Z/2026-07-27T23:59:59Z"
PRE_DATE = "2026-04-27T00:00:00Z/2026-04-27T23:59:59Z"
ORBIT = 143
CELL = 0.05
RES = 20.0
PX = (RES / 1000) ** 2
TERRAIN_CFG = {"terrain": {"slope_max_deg": 5.0, "hand_max_m": 10.0, "channel_km2": 1.0}}


def scenes(bbox, when):
    import httpx

    r = httpx.post(STAC, json={"collections": [COLLECTION], "bbox": bbox, "datetime": when, "limit": 20}, timeout=60)
    r.raise_for_status()
    return [f for f in r.json()["features"] if f["properties"].get("sat:relative_orbit") == ORBIT]


def pick(items, lon, lat):
    from shapely.geometry import Point, shape

    return next((s for s in items if shape(s["geometry"]).contains(Point(lon, lat))), None)


def read_db(item, pol, bbox):
    r = read_window(sign_href(item["assets"][pol]["href"], "planetary-computer", COLLECTION), bbox, RES, resampling="average")
    return r, db(r.data)


def warp_mask(arr, src_t, crs, bounds, shape):
    """Cut the tile out of the in-memory NRSC mask (EPSG:4326) and warp it to the tile grid."""
    west, south, east, north = transform_bounds(crs, "EPSG:4326", *bounds)
    pad = 0.002
    rows, cols = arr.shape
    c0, r0 = ~src_t * (west - pad, north + pad)
    c1, r1 = ~src_t * (east + pad, south - pad)
    c0, r0, c1, r1 = max(int(c0), 0), max(int(r0), 0), min(int(c1) + 1, cols), min(int(r1) + 1, rows)
    out = np.zeros(shape, dtype="uint8")
    if c1 <= c0 or r1 <= r0:
        return out.astype(bool)
    h, w = shape
    reproject(arr[r0:r1, c0:c1], out, src_transform=src_t * src_t.translation(c0, r0), src_crs="EPSG:4326",
              dst_transform=from_bounds(*bounds, w, h), dst_crs=crs, resampling=Resampling.nearest)
    return out.astype(bool)


def tile(args):
    x0, y0, flood_items, pre_items, flood_arr, river_arr, src_t = args
    bbox = (x0, y0, x0 + CELL, y0 + CELL)
    cx, cy = x0 + CELL / 2, y0 + CELL / 2
    item, pre = pick(flood_items, cx, cy), pick(pre_items, cx, cy)
    row = {"lon": round(x0, 3), "lat": round(y0, 3), "status": "no_scene"}
    if item is None or pre is None:
        return row
    try:
        vv_r, vv = read_db(item, "vv", bbox)
        _, vh = read_db(item, "vh", bbox)
        _, pre_vv = read_db(pre, "vv", bbox)
        _, pre_vh = read_db(pre, "vh", bbox)
    except Exception as exc:  # noqa: BLE001
        return {**row, "status": f"read_error {type(exc).__name__}"}
    if not (vv.shape == vh.shape == pre_vv.shape == pre_vh.shape):
        return {**row, "status": "grid_mismatch"}
    valid = np.isfinite(vv) & np.isfinite(pre_vv)
    if valid.mean() < 0.5:
        return {**row, "status": "low_valid"}
    try:
        t = terrain_mod.terrain_for_tile(vv_r.crs, vv_r.bounds, vv.shape, TERRAIN_CFG)
    except Exception as exc:  # noqa: BLE001
        return {**row, "status": f"terrain_error {type(exc).__name__}"}
    assess = t["assessable"] & valid
    water, q = classify_sar_water(vv, assess, None, vh)
    pre_water, _ = classify_sar_water(pre_vv, assess, None, pre_vh)
    flood_n = warp_mask(flood_arr, src_t, vv_r.crs, vv_r.bounds, vv.shape)
    river_n = warp_mask(river_arr, src_t, vv_r.crs, vv_r.bounds, vv.shape)
    change = water & ~pre_water & ~river_n
    n = flood_n & assess
    a = lambda m: float(m.sum()) * PX  # noqa: E731
    return {**row, "status": "ok", "valid_km2": a(valid), "assessable_km2": a(assess), "assessable_share": float(assess.sum() / max(valid.sum(), 1)),
            "s1_water_km2": a(water), "s1_pre_water_km2": a(pre_water), "s1_flood_km2": a(change), "s1_net_river_km2": a(water & ~river_n),
            "nrsc_flood_km2": a(n), "nrsc_flood_all_km2": a(flood_n & valid), "nrsc_river_km2": a(river_n & valid),
            "inter_km2": a(change & n), "union_km2": a(change | n), "raw_quality": q["raw_quality"], "scene": item["id"][:40]}


def estimator_test(y, f, seed=20261107, reps=4000, ns=(25, 50, 100, 200)):
    y, f = np.asarray(y, float), np.asarray(f, float)
    truth, N = y.sum(), len(y)
    strata = make_strata(f)
    rng = np.random.default_rng(seed)
    res = {}
    for n in ns:
        if n >= N:
            continue
        row = {}
        for name, fn in (("difference", difference), ("stratified_difference", stratified_difference)):
            hit, wid, err = [], [], []
            for _ in range(reps):
                s = stratified_sample(strata, n, rng) if name == "stratified_difference" else rng.choice(N, n, replace=False)
                est, lo, hi = fn(y, f, s, strata)
                if np.isfinite(lo):
                    hit.append(lo <= truth <= hi)
                    wid.append((hi - lo) / 2)
                    err.append(abs(est - truth))
            row[name] = {"coverage": float(np.mean(hit)), "median_half_width_pct": float(100 * np.median(wid) / truth),
                         "median_abs_error_pct": float(100 * np.median(err) / truth)}
        res[n] = row
    return res


def summarise(d):
    t = lambda c: float(d[c].sum())  # noqa: E731
    return {"tiles": len(d), "s1_flood_km2": t("s1_flood_km2"), "nrsc_flood_km2": t("nrsc_flood_km2"), "s1_water_km2": t("s1_water_km2"), "s1_pre_water_km2": t("s1_pre_water_km2"),
            "area_ratio_s1_over_nrsc": t("s1_flood_km2") / max(t("nrsc_flood_km2"), 1e-9), "pixel_iou": t("inter_km2") / max(t("union_km2"), 1e-9),
            "nrsc_covered_by_s1": t("inter_km2") / max(t("nrsc_flood_km2"), 1e-9), "s1_confirmed_by_nrsc": t("inter_km2") / max(t("s1_flood_km2"), 1e-9),
            "tile_pearson": float(np.corrcoef(d.s1_flood_km2, d.nrsc_flood_km2)[0, 1]) if len(d) > 2 else None, "tiles_with_nrsc_flood": int((d.nrsc_flood_km2 > 0).sum())}


def self_check():
    """A rare, clumped class with a map that doubles area: the estimator must recover the total; the map alone must not."""
    rng = np.random.default_rng(3)
    y = np.where(rng.random(1400) < 0.08, rng.gamma(1.0, 3.0, 1400), 0.0)
    f = 2 * y + rng.normal(0, 0.05, 1400).clip(0)
    r = estimator_test(y, f, reps=600, ns=(200,))[200]["difference"]
    assert r["median_abs_error_pct"] < 25, r
    assert abs(f.sum() / y.sum() - 2) < 0.2
    # The mask cut must place a known block correctly on a same-CRS grid.
    arr = np.zeros((100, 100), dtype="uint8")
    arr[40:60, 40:60] = 1
    t = from_bounds(90, 20, 91, 21, 100, 100)
    got = warp_mask(arr, t, "EPSG:4326", (90.4, 20.4, 90.6, 20.6), (20, 20))
    assert got.mean() > 0.95, got.mean()


def main(masks, workers=10):
    masks = Path(masks)
    cache = HERE / "nrsc_compare_tiles.csv"
    with rasterio.open(masks / "nrsc_flood.tif") as a, rasterio.open(masks / "nrsc_river.tif") as b:
        flood_arr, river_arr = a.read(1), b.read(1)
        src_t, (west, south, east, north) = a.transform, a.bounds
    box = [west, south, east, north]
    flood_items, pre_items = scenes(box, FLOOD_DATE), scenes(box, PRE_DATE)
    print("flood", [s["id"][:44] for s in flood_items], "pre", [s["id"][:44] for s in pre_items], flush=True)
    xs = np.arange(np.ceil(west / CELL) * CELL, east - CELL + 1e-9, CELL)
    ys = np.arange(np.ceil(south / CELL) * CELL, north - CELL + 1e-9, CELL)
    grid = [(float(x), float(y), flood_items, pre_items, flood_arr, river_arr, src_t) for x in xs for y in ys]
    print("tiles", len(grid), flush=True)
    rows = []
    with ThreadPoolExecutor(workers) as ex:
        for i, r in enumerate(ex.map(tile, grid)):
            rows.append(r)
            if i % 100 == 0:
                print(i, r["status"], flush=True)
                pd.DataFrame(rows).to_csv(cache, index=False)
    d = pd.DataFrame(rows)
    d.to_csv(cache, index=False)
    ok = d[d.status == "ok"].copy()
    plain = ok[ok.assessable_share >= 0.5]
    res = {"status_counts": d.status.value_counts().to_dict(), "all_tiles": summarise(ok), "plain_tiles": summarise(plain),
           "nrsc_flood_all_valid_km2": float(ok.nrsc_flood_all_km2.sum()),
           "estimator_targeting_nrsc_plain": estimator_test(plain.nrsc_flood_km2.values, plain.s1_flood_km2.values)}
    (HERE / "nrsc_compare_results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    self_check()
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
