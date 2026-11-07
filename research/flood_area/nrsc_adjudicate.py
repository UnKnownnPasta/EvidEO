"""Why does the Sentinel-1 instrument map 2.4 times NRSC's flood area on the Assam pass of 27 July 2026?

Run after nrsc_compare.py, which found the excess. This script looks at the excess pixels; it does not change that result.

Protocol, fixed before the first run:
  Sample       100 plain tiles by simple random sampling from nrsc_compare_tiles.csv, seed 20261107.
  Classes      both = S1 change and NRSC; s1_only = S1 change, not NRSC; nrsc_only = NRSC, not S1 change;
               perm = water in both April and July; dry = neither date, not NRSC, not river.
  Evidence     ESA WorldCover 2021 land cover (40 = cropland). Sentinel-2 L2A, 21 to 26 July, latest clear pixel
               (SCL 4, 5, 6), water = MNDWI > 0. S1-only area in patches under 1 ha, and within 100 m of NRSC flood.
  Readings     Cropland exclusion supported: s1_only cropland share >= 0.70 and at least 0.20 above that of both.
               Optical test valid only if perm water share >= 0.70 and dry water share <= 0.10.
               Optics agree with S1: s1_only water share >= 0.50.
               Optics contradict S1: s1_only water share <= 0.20 while both >= 0.50.
               Anything else is unresolved.
  Limits       Optics precede the pass by 1 to 6 days and see only cloud gaps. Rice canopy can hide water from optics
               and standing paddy water is real water, so optics cannot separate flood from a planted field.
               Neither source is ground truth, and NRSC's land-use mask is not public.

Run from the repo root: python research/flood_area/nrsc_adjudicate.py <masks_dir> [workers]
Writes nrsc_adjudicate_tiles.csv and nrsc_adjudicate_results.json beside this script.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import Resampling, reproject
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).parent))
from nrsc_compare import CELL, FLOOD_DATE, HERE, PRE_DATE, RES, STAC, TERRAIN_CFG, pick, read_db, scenes, warp_mask  # noqa: E402
from nrsc_compare import classify_sar_water, read_window, sign_href, terrain_mod  # noqa: E402

CLASSES = ("both", "s1_only", "nrsc_only", "perm", "dry")
S2_DATE = "2026-07-21T00:00:00Z/2026-07-26T23:59:59Z"
S2_OFFSET = 1000  # processing baseline 04.00 and later adds this to every DN; see backend/evideo/data/scene.py
ONE_HA_PX = 25
FRINGE_PX = 5  # 100 m at 20 m


def onto(win, ref):
    """Nearest-neighbour warp of a RasterWindow to another window's grid."""
    out = np.full(ref.data.shape, np.nan, "float32")
    reproject(win.data, out, src_transform=win.transform, src_crs=win.crs, src_nodata=np.nan,
              dst_transform=ref.transform, dst_crs=ref.crs, dst_nodata=np.nan, resampling=Resampling.nearest)
    return out


def tally(classes, wc, clear, s2_water, change, n):
    """Pixel counts per class. All inputs are boolean grids except wc, the WorldCover code."""
    row = {}
    for name, m in classes.items():
        row[f"{name}_px"] = int(m.sum())
        row[f"{name}_crop"] = int((m & (wc == 40)).sum())
        row[f"{name}_tree"] = int((m & (wc == 10)).sum())
        row[f"{name}_grass"] = int((m & (wc == 30)).sum())
        row[f"{name}_wetland"] = int((m & (wc == 90)).sum())
        row[f"{name}_wcwater"] = int((m & (wc == 80)).sum())
        row[f"{name}_clear"] = int((m & clear).sum())
        row[f"{name}_s2water"] = int((m & clear & s2_water).sum())
    s1_only = classes["s1_only"]
    lab, k = ndimage.label(change, np.ones((3, 3)))
    size = ndimage.sum(change, lab, range(1, k + 1)) if k else np.array([])
    small = np.isin(lab, 1 + np.flatnonzero(size < ONE_HA_PX)) if k else np.zeros_like(change)
    row["s1_only_speck"] = int((s1_only & small).sum())
    row["s1_only_fringe"] = int((s1_only & ndimage.binary_dilation(n, np.ones((3, 3)), FRINGE_PX)).sum())
    return row


def s2_composite(items, bbox, cx, cy, ref):
    """Latest clear Sentinel-2 pixel per grid cell. Stops once 80% of the tile is filled."""
    shape = ref.data.shape
    clear, water, used = np.zeros(shape, bool), np.zeros(shape, bool), 0
    for it in items:
        if not pick([it], cx, cy):
            continue
        signed = lambda b: sign_href(it["assets"][b]["href"], "planetary-computer", "sentinel-2-l2a")  # noqa: E731, B023
        scl = onto(read_window(signed("SCL"), bbox, RES), ref)
        new = np.isin(scl, (4, 5, 6)) & ~clear
        if not new.any():
            continue
        green = onto(read_window(signed("B03"), bbox, RES, resampling="average"), ref) - S2_OFFSET
        swir = onto(read_window(signed("B11"), bbox, RES), ref) - S2_OFFSET
        with np.errstate(invalid="ignore", divide="ignore"):
            mndwi = (green - swir) / (green + swir)
        new &= np.isfinite(mndwi)
        water[new] = mndwi[new] > 0
        clear |= new
        used += 1
        if clear.mean() >= 0.8:
            break
    return clear, water, used


def tile(args):
    x0, y0, flood_items, pre_items, s2_items, wc_items, flood_arr, river_arr, src_t = args
    bbox = (x0, y0, x0 + CELL, y0 + CELL)
    cx, cy = x0 + CELL / 2, y0 + CELL / 2
    row = {"lon": x0, "lat": y0}
    try:
        item, pre = pick(flood_items, cx, cy), pick(pre_items, cx, cy)
        vv_r, vv = read_db(item, "vv", bbox)
        _, vh = read_db(item, "vh", bbox)
        _, pre_vv = read_db(pre, "vv", bbox)
        _, pre_vh = read_db(pre, "vh", bbox)
        valid = np.isfinite(vv) & np.isfinite(pre_vv)
        assess = terrain_mod.terrain_for_tile(vv_r.crs, vv_r.bounds, vv.shape, TERRAIN_CFG)["assessable"] & valid
        water, _ = classify_sar_water(vv, assess, None, vh)
        pre_water, _ = classify_sar_water(pre_vv, assess, None, pre_vh)
        flood_n = warp_mask(flood_arr, src_t, vv_r.crs, vv_r.bounds, vv.shape)
        river_n = warp_mask(river_arr, src_t, vv_r.crs, vv_r.bounds, vv.shape)
        change = water & ~pre_water & ~river_n
        n = flood_n & assess
        classes = {"both": change & n, "s1_only": change & ~n, "nrsc_only": n & ~change, "perm": water & pre_water,
                   "dry": assess & ~water & ~pre_water & ~river_n & ~n}
        wc = onto(read_window(sign_href(pick(wc_items, cx, cy)["assets"]["map"]["href"], "planetary-computer", "esa-worldcover"), bbox), vv_r)
        clear, s2_water, used = s2_composite(s2_items, bbox, cx, cy, vv_r)
    except Exception as exc:  # noqa: BLE001
        return {**row, "status": f"error {type(exc).__name__}: {exc}"[:120]}
    return {**row, "status": "ok", "s2_scenes": used, **tally(classes, wc, clear, s2_water, change, n)}


def shares(d):
    """Pooled shares per class, with tile-bootstrap 95% intervals on the ones the readings use."""
    rng = np.random.default_rng(0)
    boots = [rng.integers(0, len(d), len(d)) for _ in range(2000)]

    def est(num, den):
        a, b = d[num].values.astype(float), d[den].values.astype(float)
        vals = [a[i].sum() / max(b[i].sum(), 1) for i in boots]
        return {"share": float(a.sum() / max(b.sum(), 1)), "ci95": [float(v) for v in np.percentile(vals, [2.5, 97.5])]}

    out = {}
    for c in CLASSES:
        out[c] = {"km2": float(d[f"{c}_px"].sum() * (RES / 1000) ** 2),
                  "cropland": est(f"{c}_crop", f"{c}_px"), "tree": est(f"{c}_tree", f"{c}_px"), "grass": est(f"{c}_grass", f"{c}_px"),
                  "wetland": est(f"{c}_wetland", f"{c}_px"), "worldcover_water": est(f"{c}_wcwater", f"{c}_px"),
                  "clear_share": est(f"{c}_clear", f"{c}_px"), "s2_water_of_clear": est(f"{c}_s2water", f"{c}_clear")}
    out["s1_only"]["in_patches_under_1ha"] = est("s1_only_speck", "s1_only_px")
    out["s1_only"]["within_100m_of_nrsc"] = est("s1_only_fringe", "s1_only_px")
    return out


def readings(r):
    crop, bothc = r["s1_only"]["cropland"]["share"], r["both"]["cropland"]["share"]
    w = {c: r[c]["s2_water_of_clear"]["share"] for c in CLASSES}
    valid = w["perm"] >= 0.70 and w["dry"] <= 0.10
    if not valid:
        optics = "invalid"
    elif w["s1_only"] >= 0.50:
        optics = "agree"
    elif w["s1_only"] <= 0.20 and w["both"] >= 0.50:
        optics = "contradict"
    else:
        optics = "unresolved"
    return {"cropland_exclusion_supported": bool(crop >= 0.70 and crop - bothc >= 0.20), "optical_test_valid": bool(valid), "optics": optics}


def self_check():
    """A 2-pixel speck, a fringe pixel and a far block must land in the right counts."""
    n = np.zeros((40, 40), bool)
    n[:5, :5] = True
    change = np.zeros((40, 40), bool)
    change[0, 5] = True  # fringe, part of a 1-pixel patch
    change[30:36, 30:36] = True  # far from NRSC, 36 pixels, above 1 ha
    wc = np.full(n.shape, 40.0)
    clear = np.ones(n.shape, bool)
    r = tally({"both": change & n, "s1_only": change & ~n, "nrsc_only": n & ~change, "perm": n & False, "dry": ~change & ~n}, wc, clear, n, change, n)
    assert r["s1_only_px"] == 37 and r["s1_only_speck"] == 1 and r["s1_only_fringe"] == 1, r
    assert r["nrsc_only_px"] == 25 and r["nrsc_only_s2water"] == 25 and r["s1_only_crop"] == 37, r
    g = lambda s: {"s2_water_of_clear": {"share": s}, "cropland": {"share": s}}  # noqa: E731
    assert readings({"perm": g(0.9), "dry": g(0.05), "s1_only": g(0.1), "both": g(0.6), "nrsc_only": g(0.5)})["optics"] == "contradict"
    assert readings({"perm": g(0.5), "dry": g(0.05), "s1_only": g(0.6), "both": g(0.6), "nrsc_only": g(0.5)})["optics"] == "invalid"


def main(masks, workers=8):
    masks = Path(masks)
    with rasterio.open(masks / "nrsc_flood.tif") as a, rasterio.open(masks / "nrsc_river.tif") as b:
        flood_arr, river_arr = a.read(1), b.read(1)
        src_t, (west, south, east, north) = a.transform, a.bounds
    box = [west, south, east, north]

    import httpx

    def search(coll, **kw):
        r = httpx.post(STAC, json={"collections": [coll], "bbox": box, "limit": 100, **kw}, timeout=60)
        r.raise_for_status()
        return r.json()["features"]

    s2_items = sorted(search("sentinel-2-l2a", datetime=S2_DATE), key=lambda f: (f["properties"]["datetime"][:10], -f["properties"]["eo:cloud_cover"]), reverse=True)
    wc_items = [f for f in search("esa-worldcover") if "2021" in f["id"]]
    flood_items, pre_items = scenes(box, FLOOD_DATE), scenes(box, PRE_DATE)
    d = pd.read_csv(HERE / "nrsc_compare_tiles.csv")
    plain = d[(d.status == "ok") & (d.assessable_share >= 0.5)]
    sample = plain.sample(100, random_state=20261107)
    print("sample holds", round(sample.s1_flood_km2.sum() - sample.inter_km2.sum(), 1), "km2 of excess of", round(plain.s1_flood_km2.sum() - plain.inter_km2.sum(), 1), flush=True)
    grid = [(float(x), float(y), flood_items, pre_items, s2_items, wc_items, flood_arr, river_arr, src_t) for x, y in zip(sample.lon, sample.lat)]
    with ThreadPoolExecutor(workers) as ex:
        rows = []
        for i, r in enumerate(ex.map(tile, grid)):
            rows.append(r)
            if i % 10 == 0:
                print(i, r["status"], flush=True)
    t = pd.DataFrame(rows)
    t.to_csv(HERE / "nrsc_adjudicate_tiles.csv", index=False)
    ok = t[t.status == "ok"]
    res = {"tiles_ok": len(ok), "tiles_failed": int(len(t) - len(ok)), "classes": shares(ok)}
    res["readings"] = readings(res["classes"])
    (HERE / "nrsc_adjudicate_results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    self_check()
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
