"""Terrain exclusion for SAR flood water: slope and HAND (Height Above Nearest Drainage).

Why: NRSC's newest automated flood method keeps flood pixels only up to HAND 15 m and subtracts a
permanent-river mask (Chimata et al., NHESS 2025); Copernicus GFM marks pixels with HAND >= 10 m as
"not assessable" and excludes slopes over about 5 degrees (archive A083, A210, A213). Dark pixels on
hillsides are radar shadow, not water (the Sindhudurg error in PLOS ONE, NOVELTY.md). Marking them
"not assessable" instead of "dry" keeps the answer honest: the card reports the area it could not judge.

HAND here is computed from the DEM tile (plus a context ring) in five transparent steps:
  1. priority-flood fill with an epsilon so every cell has a strictly descending path (Barnes et al. 2014);
  2. D8 steepest-descent flow directions on the filled surface;
  3. flow accumulation, highest cell first;
  4. channels = cells whose upslope area reaches `channel_km2`;
  5. HAND = cell elevation minus the elevation of the channel cell its flow path reaches.
Cells whose path leaves the grid before reaching a channel get HAND = NaN ("unknown"), which is never
treated as excluded. The DEM is the Copernicus GLO-30 surface model, which GFM does not feed to HAND
directly because it is not hydrologically conditioned; the fill above is a light conditioning, and a
MERIT Hydro HAND layer can replace `hand_from_dem` without touching the rest (SOLUTION.md, v1.2 plan).
"""
from __future__ import annotations

import heapq
from typing import Any, Optional

import numpy as np

SLOPE_MAX_DEG = 5.0       # GFM / Twele et al. 2016 slope exclusion
HAND_MAX_M = 10.0         # GFM; NRSC uses 15 m. Not yet validated on Indian floodplains (see NOVELTY.md)
CHANNEL_KM2 = 1.0         # upslope area that makes a cell a drainage channel
HAND_RES_M = 60.0         # HAND is computed on a coarser grid: the pure-Python flow loops cost O(cells)
EPS = 1e-4

# D8 neighbour offsets and their distances in cell units
_NB = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
_DIST = [2 ** 0.5, 1.0, 2 ** 0.5, 1.0, 1.0, 2 ** 0.5, 1.0, 2 ** 0.5]


def slope_deg(dem: np.ndarray, res_m: float) -> np.ndarray:
    """Slope in degrees from central differences (NaN where the DEM is NaN)."""
    gy, gx = np.gradient(dem.astype("float64"), res_m)
    return np.degrees(np.arctan(np.hypot(gx, gy))).astype("float32")


def _fill(dem: np.ndarray) -> np.ndarray:
    """Priority-flood with epsilon: edge cells and NaN-adjacent cells are outlets, pits are raised to
    spill level plus a tiny slope. Deterministic (ties broken by cell index)."""
    h, w = dem.shape
    z = np.where(np.isfinite(dem), dem, np.nan).astype("float64")
    filled = z.copy()
    done = np.zeros((h, w), bool)
    heap: list[tuple[float, int]] = []
    for y in range(h):
        for x in range(w):
            if not np.isfinite(z[y, x]):
                done[y, x] = True
                continue
            edge = y in (0, h - 1) or x in (0, w - 1)
            if not edge:
                for dy, dx in _NB:
                    if not np.isfinite(z[y + dy, x + dx]):
                        edge = True
                        break
            if edge:
                heapq.heappush(heap, (z[y, x], y * w + x))
                done[y, x] = True
    while heap:
        zc, i = heapq.heappop(heap)
        y, x = divmod(i, w)
        for dy, dx in _NB:
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and not done[yy, xx]:
                done[yy, xx] = True
                filled[yy, xx] = max(z[yy, xx], zc + EPS)
                heapq.heappush(heap, (filled[yy, xx], yy * w + xx))
    return filled


def hand_from_dem(dem: np.ndarray, res_m: float, channel_km2: float = CHANNEL_KM2) -> dict[str, Any]:
    """HAND in metres on the DEM grid, plus the filled surface, channel mask and the share of cells
    whose flow path never reached a channel (HAND unknown)."""
    h, w = dem.shape
    ok = np.isfinite(dem)
    if ok.sum() < 9:
        return {"hand": np.full(dem.shape, np.nan, "float32"), "channels": np.zeros(dem.shape, bool), "unknown_share": 1.0}
    filled = _fill(dem)
    pad = np.pad(filled, 1, constant_values=np.nan)
    best = np.zeros((h, w))
    down = np.full((h, w), -1, dtype=np.int64)
    idx = np.arange(h * w).reshape(h, w)
    for (dy, dx), d in zip(_NB, _DIST):
        nb = pad[1 + dy:1 + dy + h, 1 + dx:1 + dx + w]
        with np.errstate(invalid="ignore"):
            drop = (filled - nb) / d
        better = np.isfinite(drop) & (drop > best)
        best = np.where(better, drop, best)
        down = np.where(better, idx + dy * w + dx, down)
    order = np.argsort(-filled.ravel(), kind="stable")          # highest first, deterministic
    order = order[ok.ravel()[order]]
    acc = np.ones(h * w)
    dflat = down.ravel()
    for i in order:
        j = dflat[i]
        if j >= 0:
            acc[j] += acc[i]
    cell_km2 = (res_m / 1000.0) ** 2
    channels = ok & (acc.reshape(h, w) * cell_km2 >= channel_km2)
    chan = channels.ravel()
    zflat = np.where(ok, dem, np.nan).ravel().astype("float64")
    ref = np.full(h * w, np.nan)
    for i in order[::-1]:                                       # lowest first, so the downstream cell is done
        if chan[i]:
            ref[i] = zflat[i]
        else:
            j = dflat[i]
            if j >= 0:
                ref[i] = ref[j]
    hand = np.maximum(zflat - ref, 0.0).reshape(h, w).astype("float32")
    unknown = ok & ~np.isfinite(hand)
    return {"hand": hand, "channels": channels, "unknown_share": float(unknown.sum() / max(ok.sum(), 1))}


def erode1(mask: np.ndarray) -> np.ndarray:
    """Shrink a boolean mask by one pixel (4-neighbourhood), as GFM shrinks its exclusion mask."""
    p = np.pad(mask, 1, constant_values=False)
    return mask & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]


def assessable_mask(slope: np.ndarray, hand: Optional[np.ndarray], slope_max: float = SLOPE_MAX_DEG,
                    hand_max: float = HAND_MAX_M) -> tuple[np.ndarray, dict[str, float]]:
    """True where flood water can be judged. Steep pixels and pixels with HAND >= hand_max (shrunk by one
    pixel) are 'not assessable'. NaN slope or HAND never excludes: missing terrain is reported, not guessed."""
    with np.errstate(invalid="ignore"):
        steep = np.isfinite(slope) & (slope > slope_max)
        high = np.isfinite(hand) & (hand >= hand_max) if hand is not None else np.zeros(slope.shape, bool)
    high = erode1(high)
    out = ~(steep | high)
    n = max(slope.size, 1)
    return out, {"steep_share": round(float(steep.sum()) / n, 4), "high_hand_share": round(float(high.sum()) / n, 4),
                 "not_assessable_share": round(float((~out).sum()) / n, 4),
                 "terrain_known_share": round(float(np.isfinite(slope).sum()) / n, 4)}


def terrain_for_tile(crs: str, bounds: tuple[float, float, float, float], shape: tuple[int, int],
                     cfg: dict[str, Any], dem_reader=None) -> dict[str, Any]:
    """Assessable-pixel mask on a Sentinel-1 tile grid (crs, bounds, shape).

    Slope and HAND are both computed on a HAND_RES_M grid covering the tile plus one tile on every side
    (so a channel just outside the tile still drains it), then warped to the tile grid. Slope is taken at
    that scale on purpose: the 30 m surface model carries tree and building noise that reads as >5 degrees
    on flat floodplain at 20 m (measured: Barpeta 10.6% 'steep' at 20 m, 0.2% at 60 m).
    `dem_reader(crs, bounds, shape)` defaults to the Copernicus GLO-30 reader; tests inject a synthetic one."""
    import rasterio
    from rasterio.transform import from_bounds
    from rasterio.warp import Resampling, reproject

    if dem_reader is None:
        from .data.cog import read_dem_on_grid as dem_reader
    c = cfg.get("terrain", {}) if cfg else {}
    slope_max = float(c.get("slope_max_deg", SLOPE_MAX_DEG))
    hand_max = float(c.get("hand_max_m", HAND_MAX_M))
    channel_km2 = float(c.get("channel_km2", CHANNEL_KM2))
    left, bottom, right, top = bounds
    dx, dy = right - left, top - bottom
    cb = (left - dx, bottom - dy, right + dx, top + dy)
    cshape = (max(int(round(3 * dy / HAND_RES_M)), 3), max(int(round(3 * dx / HAND_RES_M)), 3))
    cres = ((cb[2] - cb[0]) / cshape[1] + (cb[3] - cb[1]) / cshape[0]) / 2
    dem = dem_reader(crs, cb, cshape)
    if not np.isfinite(dem).any():
        raise ValueError("no DEM coverage for this tile")
    sl = slope_deg(dem, cres)
    hd = hand_from_dem(dem, cres, channel_km2)
    src_tf = from_bounds(*cb, cshape[1], cshape[0])
    dst_tf = from_bounds(*bounds, shape[1], shape[0])
    warped = []
    for arr in (sl, hd["hand"]):
        out = np.full(shape, np.nan, dtype="float32")
        reproject(arr.astype("float32"), out, src_transform=src_tf, src_crs=crs, dst_transform=dst_tf, dst_crs=crs,
                  src_nodata=np.nan, dst_nodata=np.nan, resampling=Resampling.nearest)
        warped.append(out)
    ok, stats = assessable_mask(warped[0], warped[1], slope_max, hand_max)
    stats.update({"slope_max_deg": slope_max, "hand_max_m": hand_max, "channel_km2": channel_km2,
                  "hand_unknown_share": round(hd["unknown_share"], 4), "grid_m": round(cres, 1),
                  "dem": "Copernicus GLO-30 (DSM), lightly conditioned (priority-flood)"})
    return {"assessable": ok, "hand": warped[1], "slope": warped[0], "stats": stats}
