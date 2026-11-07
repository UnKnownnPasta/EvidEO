"""Pilot: can a small labelled sample put a valid confidence interval on total flooded area?

Protocol, fixed before the first run:
  Population   every usable chip of one Sen1Floods11 event. Truth is the sum of hand-labelled water area.
  Map          the Sentinel-1 instrument's predicted water area per chip (v1.1).
  Sampling     n chips labelled, chosen by simple random sampling without replacement. n = 8, 16, 32.
  Estimators   map only; labels only; difference (the mean form of prediction-powered inference, PPI);
               ratio; stratified difference with strata from the predicted area.
  Pass         on the Indian chips at n <= 16, a 95% interval must cover the truth at least 90% of the time
               and have a median half-width of at most 50% of the true total.
  Report       India first, then all events, including failures. No criteria change after seeing results.

Run from the repo root: python research/flood_area/ppi_pilot.py
Writes research/flood_area/ppi_pilot_results.json.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
CHIPS = ROOT / "training/calibration/reports/sar_water_otsu_chips.csv"
OUT = Path(__file__).with_name("ppi_pilot_results.json")
NS = (8, 16, 32)
REPS = 5000
ALPHA = 0.05


def interval(est, se, df):
    if not np.isfinite(se) or df < 1:
        return np.nan, np.nan
    t = stats.t.ppf(1 - ALPHA / 2, df)
    return est - t * se, est + t * se


def labels_only(y, f, s, strata=None):
    N, n = len(y), len(s)
    v = y[s]
    est = N * v.mean()
    se = N * v.std(ddof=1) / np.sqrt(n) * np.sqrt(1 - n / N)
    return (est, *interval(est, se, n - 1))


def difference(y, f, s, strata=None):
    """Map total plus a correction learned from the labelled sample."""
    N, n = len(y), len(s)
    r = y[s] - f[s]
    est = f.sum() + N * r.mean()
    se = N * r.std(ddof=1) / np.sqrt(n) * np.sqrt(1 - n / N)
    return (est, *interval(est, se, n - 1))


def ratio(y, f, s, strata=None):
    N, n = len(y), len(s)
    if f[s].sum() <= 0:
        return np.nan, np.nan, np.nan
    b = y[s].sum() / f[s].sum()
    est = b * f.sum()
    se = N * (y[s] - b * f[s]).std(ddof=1) / np.sqrt(n) * np.sqrt(1 - n / N)
    return (est, *interval(est, se, n - 1))


def make_strata(f):
    """Three strata: nothing predicted, then predicted area split at its median."""
    g = np.zeros(len(f), dtype=int)
    pos = f > 0
    if pos.any():
        g[pos] = 1 + (f[pos] > np.median(f[pos])).astype(int)
    return g


def stratified_sample(g, n, rng):
    """Proportional allocation, at least two labels in each non-empty stratum where possible."""
    ids = [np.flatnonzero(g == k) for k in np.unique(g)]
    take = [min(len(i), max(2, round(n * len(i) / len(g)))) for i in ids]
    while sum(take) > n:
        j = int(np.argmax(take))
        if take[j] <= 2:
            break
        take[j] -= 1
    while sum(take) < n:
        room = [len(i) - t for i, t in zip(ids, take)]
        j = int(np.argmax(room))
        if room[j] <= 0:
            break
        take[j] += 1
    return np.concatenate([rng.choice(i, t, replace=False) for i, t in zip(ids, take)])


def stratified_difference(y, f, s, strata):
    est, var, nus = f.sum(), 0.0, []
    for k in np.unique(strata):
        Nk = (strata == k).sum()
        sk = s[strata[s] == k]
        nk = len(sk)
        if nk == 0:
            return np.nan, np.nan, np.nan
        r = y[sk] - f[sk]
        est += Nk * r.mean()
        if nk > 1:
            v = Nk**2 * r.var(ddof=1) / nk * (1 - nk / Nk)
            var += v
            nus.append((v, nk - 1))
    if var <= 0:
        return est, est, est
    df = var**2 / sum(v**2 / d for v, d in nus)  # Satterthwaite
    return (est, *interval(est, np.sqrt(var), df))


METHODS = {"labels_only": labels_only, "difference": difference, "ratio": ratio, "stratified_difference": stratified_difference}


def evaluate(y, f, seed=20261107, reps=REPS, ns=NS):
    y, f = np.asarray(y, float), np.asarray(f, float)
    truth, N = y.sum(), len(y)
    strata = make_strata(f)
    rng = np.random.default_rng(seed)
    out = {"chips": N, "true_km2": truth, "map_km2": f.sum(), "map_error_pct": 100 * (f.sum() - truth) / truth,
           "water_share_of_chips_with_water": float((y > 0).mean()), "n": {}}
    for n in ns:
        if n >= N:
            continue
        row = {}
        for name, fn in METHODS.items():
            hits, widths, errs, fails = [], [], [], 0
            for _ in range(reps):
                s = stratified_sample(strata, n, rng) if name == "stratified_difference" else rng.choice(N, n, replace=False)
                est, lo, hi = fn(y, f, s, strata)
                if not np.isfinite(lo):
                    fails += 1
                    continue
                hits.append(lo <= truth <= hi)
                widths.append((hi - lo) / 2)
                errs.append(abs(est - truth))
            row[name] = {"coverage": float(np.mean(hits)) if hits else None,
                         "median_half_width_pct": float(100 * np.median(widths) / truth) if widths else None,
                         "median_abs_error_pct": float(100 * np.median(errs) / truth) if errs else None,
                         "no_interval_share": fails / reps}
        out["n"][n] = row
    return out


def passes(result):
    """Protocol check for one estimator: every n <= 16 meets both thresholds."""
    verdict = {}
    for m in METHODS:
        ok = True
        for n in (8, 16):
            r = result["n"][n][m]
            ok &= r["coverage"] is not None and r["coverage"] >= 0.90 and r["median_half_width_pct"] <= 50 and r["no_interval_share"] == 0
        verdict[m] = bool(ok)
    return verdict


def self_check():
    """A simulated population with a known biased map: the difference interval must cover near nominal, and the
    map alone must stay biased. Fails loudly if the estimator or the finite-population correction breaks."""
    rng = np.random.default_rng(1)
    y = rng.gamma(2.0, 3.0, 400)
    f = 0.7 * y + rng.normal(0, 0.5, 400)
    r = evaluate(y, f, reps=1500, ns=(32,))
    d = r["n"][32]["difference"]
    assert 0.92 <= d["coverage"] <= 0.98, d
    assert abs(r["map_error_pct"]) > 20, r["map_error_pct"]
    assert d["median_abs_error_pct"] < abs(r["map_error_pct"]) / 3, d


if __name__ == "__main__":
    self_check()
    d = pd.read_csv(CHIPS)
    d = d[d.status == "ok"]
    results = {}
    for ev in ["India"] + sorted(e for e in d.event.unique() if e != "India"):
        s = d[d.event == ev]
        results[ev] = evaluate(s.ref_km2.values, s.pred_km2.values)
    results["India"]["protocol_pass"] = passes(results["India"])
    OUT.write_text(json.dumps(results, indent=1))
    for ev, r in results.items():
        print(f"\n{ev}: {r['chips']} chips, true {r['true_km2']:.1f} km2, map {r['map_km2']:.1f} km2 ({r['map_error_pct']:+.0f}%)")
        for n, row in r["n"].items():
            for m, v in row.items():
                print(f"  n={n:<2} {m:<22} coverage {v['coverage'] if v['coverage'] is None else round(v['coverage'], 3)}  half-width {v['median_half_width_pct'] and round(v['median_half_width_pct'])}%  abs error {v['median_abs_error_pct'] and round(v['median_abs_error_pct'])}%  no interval {v['no_interval_share']:.2f}")
    print("\nProtocol verdict, India:", results["India"]["protocol_pass"])
