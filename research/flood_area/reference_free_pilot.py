"""Pilot: can three flood maps estimate their own accuracy and the flooded area with no reference?

Method: a two-class latent class model (equivalent to categorical triple collocation under conditional
independence) fitted by EM to the eight-cell agreement table of three binary maps.

Protocol, fixed before the first run:
  Maps         S1 = the Sen1Floods11 Sentinel-1 Otsu map; S2 = Sentinel-2 MNDWI > 0; third map is either
               JRC permanent water (different information, poor flood sensitivity) or a Sentinel-1 VH threshold
               (same sensor, so independence is doubtful). Both triples are always reported.
  Truth        Hand labels, withheld from the model and used only for scoring.
  Pass         On Indian chips: estimated water share within 25% of the true share, and sensitivity and
               specificity of S1 and S2 each within 0.10 of their true values.
  Generality   The same test on each event; report how many pass.
  Note         Hand labels were drawn with Sentinel-2 in view, so S2 may look better than it would against an
               independent truth. This favours the S2 scores but does not tune the model.

Run from the repo root:
  python research/flood_area/reference_free_pilot.py fetch     # streams about 3 GB, keeps counts only
  python research/flood_area/reference_free_pilot.py analyse
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "training" / "calibration"))
HERE = Path(__file__).parent
COUNTS = HERE / "reference_free_counts.json"
OUT = HERE / "reference_free_results.json"
HAND = "data/flood_events/HandLabeled"


def threshold_otsu(values, bins=256):
    """Otsu's threshold: maximise between-class variance on a histogram."""
    h, edges = np.histogram(values, bins=bins)
    mid = (edges[:-1] + edges[1:]) / 2
    w = np.cumsum(h)
    m = np.cumsum(h * mid)
    with np.errstate(divide="ignore", invalid="ignore"):
        between = (m[-1] * w - m * w[-1]) ** 2 / (w * (w[-1] - w))
    return mid[np.nanargmax(between[:-1])]


def fetch_chip(chip):
    from fit_water import BUCKET, _get, _read

    name = chip["chip"]
    try:
        y = _read(_get(chip["label"]))[0]
        s1 = _read(_get(chip["s1"]))
        otsu = _read(_get(f"{BUCKET}/{HAND}/S1OtsuLabelHand/{name}_S1OtsuLabelHand.tif"))[0]
        s2 = _read(_get(f"{BUCKET}/{HAND}/S2Hand/{name}_S2Hand.tif"))
        jrc = _read(_get(f"{BUCKET}/{HAND}/JRCWaterHand/{name}_JRCWaterHand.tif"))[0]
    except Exception as exc:  # noqa: BLE001
        return {"chip": name, "event": chip["event"], "error": f"{type(exc).__name__}: {exc}"[:160]}
    green, swir = s2[2], s2[11]  # Sen1Floods11 S2 band order B1..B12 with B8A: B3 is index 2, B11 is index 11
    vh = s1[1]
    ok = (y >= 0) & (otsu >= 0) & (jrc >= 0) & np.isfinite(vh) & np.isfinite(green) & np.isfinite(swir) & ((green + swir) > 0)
    if ok.sum() < 100:
        return {"chip": name, "event": chip["event"], "error": "too few valid pixels"}
    mndwi = (green - swir) / np.where(green + swir == 0, np.nan, green + swir)
    vh_map = vh < threshold_otsu(vh[ok])
    bits = (otsu == 1) * 1 + (mndwi > 0) * 2 + (jrc == 1) * 4 + vh_map * 8 + (y == 1) * 16
    counts = np.bincount(bits[ok].astype(int), minlength=32)
    return {"chip": name, "event": chip["event"], "split": chip["split"], "counts": counts.tolist()}


def fetch():
    from fit_water import list_chips

    chips = list_chips()
    with ThreadPoolExecutor(8) as ex:
        rows = []
        for i, r in enumerate(ex.map(fetch_chip, chips)):
            rows.append(r)
            if i % 40 == 0:
                print(i, len(chips), r.get("error", "ok"), flush=True)
    COUNTS.write_text(json.dumps(rows))
    print("saved", len(rows), "failed", sum("error" in r for r in rows))


def fit_latent_class(table, starts=8, iters=2000, seed=0):
    """table: length-8 counts indexed by bit0 + 2*bit1 + 4*bit2. Returns prevalence, sensitivity[3], specificity[3]."""
    table = np.asarray(table, float)
    x = np.array([[(i >> b) & 1 for b in range(3)] for i in range(8)])
    rng = np.random.default_rng(seed)
    best, best_ll = None, -np.inf
    for _ in range(starts):
        pi = rng.uniform(0.05, 0.5)
        se, sp = rng.uniform(0.6, 0.95, 3), rng.uniform(0.8, 0.999, 3)
        ll = -np.inf
        for _ in range(iters):
            w1 = pi * np.prod(se**x * (1 - se) ** (1 - x), axis=1)
            w0 = (1 - pi) * np.prod((1 - sp) ** x * sp ** (1 - x), axis=1)
            tot = np.maximum(w1 + w0, 1e-300)
            post = w1 / tot
            new_ll = float((table * np.log(tot)).sum())
            m1 = table * post
            pi = m1.sum() / table.sum()
            se = np.clip((m1[:, None] * x).sum(0) / max(m1.sum(), 1e-9), 1e-6, 1 - 1e-6)
            m0 = table * (1 - post)
            sp = np.clip((m0[:, None] * (1 - x)).sum(0) / max(m0.sum(), 1e-9), 1e-6, 1 - 1e-6)
            if abs(new_ll - ll) < 1e-7 * abs(new_ll):
                ll = new_ll
                break
            ll = new_ll
        # The two classes are interchangeable. Water is the class whose maps mostly say yes.
        if (se + sp).sum() < 3:
            pi, se, sp = 1 - pi, 1 - sp, 1 - se
        if pi > 0.5:  # water is never the majority class across a whole chip set in this data
            pi, se, sp = 1 - pi, 1 - sp, 1 - se
        if ll > best_ll:
            best, best_ll = (float(pi), se.tolist(), sp.tolist()), ll
    return best


def truth_rates(counts, b):
    """Sensitivity and specificity of map bit b against the hand-label bit 4."""
    i = np.arange(32)
    m, y = (i >> b) & 1, (i >> 4) & 1
    tp, fn = counts[(m == 1) & (y == 1)].sum(), counts[(m == 0) & (y == 1)].sum()
    tn, fp = counts[(m == 0) & (y == 0)].sum(), counts[(m == 1) & (y == 0)].sum()
    return tp / max(tp + fn, 1), tn / max(tn + fp, 1)


def score(counts, third):
    """Fit S1 (bit 0), S2 (bit 1) and the third map, then compare with hand labels."""
    i = np.arange(32)
    idx = ((i >> 0) & 1) + 2 * ((i >> 1) & 1) + 4 * ((i >> third) & 1)
    table = np.bincount(idx, weights=counts, minlength=8)
    pi, se, sp = fit_latent_class(table)
    true_pi = counts[((i >> 4) & 1) == 1].sum() / counts.sum()
    tr = {b: truth_rates(counts, b) for b in (0, 1)}
    share_err = (pi - true_pi) / true_pi if true_pi > 0 else float("nan")
    gaps = {"S1_se": se[0] - tr[0][0], "S1_sp": sp[0] - tr[0][1], "S2_se": se[1] - tr[1][0], "S2_sp": sp[1] - tr[1][1]}
    maps = {"S1": counts[((i >> 0) & 1) == 1].sum() / counts.sum(), "S2": counts[((i >> 1) & 1) == 1].sum() / counts.sum()}
    return {"true_water_share": float(true_pi), "estimated_water_share": pi, "share_error_pct": 100 * share_err,
            "S1_map_share_error_pct": 100 * (maps["S1"] - true_pi) / max(true_pi, 1e-9),
            "S2_map_share_error_pct": 100 * (maps["S2"] - true_pi) / max(true_pi, 1e-9),
            "gaps": {k: float(v) for k, v in gaps.items()},
            "passes": bool(abs(share_err) <= 0.25 and all(abs(v) <= 0.10 for v in gaps.values()))}


def self_check():
    """Conditionally independent maps must recover their known rates; a correlated pair must visibly fail less cleanly."""
    pi, se, sp = 0.1, np.array([0.8, 0.9, 0.6]), np.array([0.98, 0.95, 0.99])
    x = np.array([[(i >> b) & 1 for b in range(3)] for i in range(8)])
    p = pi * np.prod(se**x * (1 - se) ** (1 - x), 1) + (1 - pi) * np.prod((1 - sp) ** x * sp ** (1 - x), 1)
    got = fit_latent_class(p * 1e7)
    assert abs(got[0] - pi) < 0.01, got
    assert np.allclose(got[1], se, atol=0.02) and np.allclose(got[2], sp, atol=0.02), got
    low, high = np.random.default_rng(0).normal(-22, 1, 4000), np.random.default_rng(1).normal(-10, 1, 4000)
    t = threshold_otsu(np.r_[low, high])  # Otsu's score is flat across the empty gap, so test separation, not a value
    assert (low < t).mean() > 0.99 and (high > t).mean() > 0.99, t


def analyse():
    rows = [r for r in json.loads(COUNTS.read_text()) if "counts" in r]
    results = {}
    for ev in ["India", "ALL"] + sorted({r["event"] for r in rows} - {"India"}):
        c = np.sum([r["counts"] for r in rows if ev == "ALL" or r["event"] == ev], axis=0, dtype=float)
        results[ev] = {"chips": sum(ev == "ALL" or r["event"] == ev for r in rows),
                       "S1+S2+JRC": score(c, 2), "S1+S2+VH": score(c, 3)}
    OUT.write_text(json.dumps(results, indent=1))
    for ev, r in results.items():
        for t in ("S1+S2+JRC", "S1+S2+VH"):
            s = r[t]
            print(f"{ev:<10}{t:<11} chips {r['chips']:<4} true {s['true_water_share']:.3f} est {s['estimated_water_share']:.3f} "
                  f"({s['share_error_pct']:+.0f}%) S1 map {s['S1_map_share_error_pct']:+.0f}% S2 map {s['S2_map_share_error_pct']:+.0f}% "
                  f"gaps {[round(v, 2) for v in s['gaps'].values()]} pass={s['passes']}")
    for t in ("S1+S2+JRC", "S1+S2+VH"):
        evs = [k for k in results if k not in ("ALL",)]
        print(t, "passes on", sum(results[k][t]["passes"] for k in evs), "of", len(evs), "events")


if __name__ == "__main__":
    self_check()
    {"fetch": fetch, "analyse": analyse}[sys.argv[1] if len(sys.argv) > 1 else "analyse"]()
