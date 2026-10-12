"""Experiments for the EvidEO paper. Reads the committed per-chip calibration rows and writes
paper/analysis/results.json plus figures in paper/figures/. Deterministic (seeded). Run from repo root:
    python paper/analysis/experiments.py
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REP = ROOT / "training/calibration/reports"
OUT = ROOT / "paper/analysis/results.json"
T = 0.60
rng = np.random.default_rng(20261012)


def platt(raw, y, iters=100, w0=None, fix_a=None):
    """Platt scaling with smoothed targets. fix_a: keep slope fixed, fit intercept only."""
    n1, n0 = y.sum(), len(y) - y.sum()
    t = np.where(y > 0, (n1 + 1) / (n1 + 2), 1 / (n0 + 2))
    if fix_a is not None:
        b = 0.0 if w0 is None else w0[1]
        for _ in range(iters):
            p = 1 / (1 + np.exp(-np.clip(fix_a * raw + b, -30, 30)))
            g = (p - t).sum(); h = (p * (1 - p)).sum() + 1e-6
            b -= g / h
        return fix_a, b
    X = np.stack([raw, np.ones_like(raw)], 1)
    w = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        g = X.T @ (p - t)
        H = X.T @ (X * (p * (1 - p))[:, None]) + 1e-6 * np.eye(2)
        w -= np.linalg.solve(H, g)
    return float(w[0]), float(w[1])


def sig(a, b, raw):
    return 1 / (1 + np.exp(-(a * raw + b)))


def ece(p, y, bins=10):
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        s = (p >= edges[i]) & ((p < edges[i + 1]) if i < bins - 1 else (p <= 1))
        if s.any():
            e += s.mean() * abs(p[s].mean() - y[s].mean())
    return float(e)


def sel(p, y, t=T):
    k = p >= t
    return float(k.mean()), (float(1 - y[k].mean()) if k.any() else float("nan"))


def rc_curve(p, y):
    o = np.argsort(-p, kind="stable")
    err = 1 - y[o]
    n = len(err)
    risk = np.cumsum(err) / np.arange(1, n + 1)
    return np.arange(1, n + 1) / n, risk, float(risk.mean())


def oracle_aurc(y):
    return rc_curve(y.astype(float), y)[2]


def boot_ci(fn, *arrs, n=2000):
    vals = []
    m = len(arrs[0])
    for _ in range(n):
        i = rng.integers(0, m, m)
        vals.append(fn(*[a[i] for a in arrs]))
    vals = np.array(vals)
    vals = vals[~np.isnan(vals)]
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def load(name):
    d = pd.read_csv(REP / name)
    return d[d.status == "ok"].copy()


res = {}
v11 = load("sar_water_otsu_chips.csv")
v10 = load("sar_water_otsu_v1.0_chips.csv")
cfg = json.load(open(ROOT / "config/calibration/sar_water_otsu.json"))
A, B = cfg["a"], cfg["b"]

# ---- E1: held-out test, risk-coverage, operating point, bootstrap CIs ----
fitv10 = json.load(open(REP / "sar_water_otsu_v1.0_fit.json"))
e1 = {}
for tag, d in (("v1.1", v11), ("v1.0", v10)):
    fit = d[d.split.isin(["train", "valid"])]
    a, b = (A, B) if tag == "v1.1" else platt(fit.raw.values, fit.correct.values.astype(float))
    te = d[d.split == "test"]
    y = te.correct.values.astype(float); r = te.raw.values; p = sig(a, b, r)
    cov, err = sel(p, y)
    _, _, au = rc_curve(p, y)
    pooled_iou = float(te.inter_px.sum() / te.union_px.sum()) if "inter_px" in te else None
    e1[tag] = {"n": len(te), "acc_always_answer": float(y.mean()), "error_always_answer": float(1 - y.mean()),
               "ece_raw": ece(r, y), "ece_cal": ece(p, y), "coverage_at_0.6": cov, "error_when_published": err,
               "err_ci95": boot_ci(lambda p_, y_: sel(p_, y_)[1], p, y),
               "aurc": au, "aurc_oracle": oracle_aurc(y), "aurc_random": float(1 - y.mean()),
               "median_iou": float(te.iou.median()), "pooled_iou": pooled_iou, "a": a, "b": b,
               "pooled_iou_bolivia": float(d[d.split == "bolivia"].inter_px.sum() / d[d.split == "bolivia"].union_px.sum()) if "inter_px" in d else None}
    if tag == "v1.1":
        cv, rk, _ = rc_curve(p, y)
        e1["curve_v11"] = [cv.tolist(), rk.tolist()]
        bins = np.linspace(0, 1, 11)
        e1["reliability_test"] = [[float(p[(p >= bins[i]) & (p < bins[i + 1] + (i == 9))].mean()) if ((p >= bins[i]) & (p < bins[i + 1] + (i == 9))).any() else None,
                                   float(y[(p >= bins[i]) & (p < bins[i + 1] + (i == 9))].mean()) if ((p >= bins[i]) & (p < bins[i + 1] + (i == 9))).any() else None,
                                   int(((p >= bins[i]) & (p < bins[i + 1] + (i == 9))).sum())] for i in range(10)]
    else:
        cv, rk, _ = rc_curve(p, y)
        e1["curve_v10"] = [cv.tolist(), rk.tolist()]
res["E1_test"] = e1

# ---- E2: leave-one-event-out calibration transfer (v1.1) ----
allrows = v11.copy()
e2 = {}
for ev in sorted(allrows.event.unique()):
    tr = allrows[allrows.event != ev]; te = allrows[allrows.event == ev]
    a, b = platt(tr.raw.values, tr.correct.values.astype(float))
    y = te.correct.values.astype(float); p = sig(a, b, te.raw.values)
    cov, err = sel(p, y)
    e2[ev] = {"n": len(te), "share_correct": float(y.mean()), "ece": ece(p, y), "mean_conf": float(p.mean()),
              "overconfidence": float(p.mean() - y.mean()), "coverage": cov, "error_when_published": err}
res["E2_loeo"] = e2

# ---- E3: local calibration budget for India (v1.1) ----
ind = allrows[allrows.event == "India"].reset_index(drop=True)
glob = allrows[(allrows.event != "India") & (allrows.split != "test")]
ga, gb = platt(glob.raw.values, glob.correct.values.astype(float))
Ks = [0, 4, 8, 12, 16, 24, 32]
R = 500
e3 = {"n_india": len(ind), "global_fit": [ga, gb], "K": Ks, "strategies": {}}
for strat in ("intercept_only", "pooled_refit", "india_only"):
    rows = []
    for k in Ks:
        E, C, ER, OC = [], [], [], []
        for _ in range(R):
            idx = rng.permutation(len(ind)); cal, ev = ind.iloc[idx[:k]], ind.iloc[idx[k:]]
            if k == 0:
                a, b = ga, gb
            elif strat == "intercept_only":
                a, b = platt(cal.raw.values, cal.correct.values.astype(float), fix_a=ga, w0=(ga, gb))
            elif strat == "pooled_refit":
                a, b = platt(np.r_[glob.raw.values, cal.raw.values], np.r_[glob.correct.values, cal.correct.values].astype(float))
            else:
                if cal.correct.nunique() < 2:
                    a, b = platt(cal.raw.values, cal.correct.values.astype(float), fix_a=ga, w0=(ga, gb))
                else:
                    a, b = platt(cal.raw.values, cal.correct.values.astype(float))
            y = ev.correct.values.astype(float); p = sig(a, b, ev.raw.values)
            c, er = sel(p, y)
            E.append(ece(p, y)); C.append(c); ER.append(er); OC.append(p.mean() - y.mean())
        ER = np.array(ER)
        rows.append({"k": k, "ece_mean": float(np.mean(E)), "ece_p10": float(np.percentile(E, 10)), "ece_p90": float(np.percentile(E, 90)),
                     "coverage_mean": float(np.mean(C)), "err_pub_mean": float(np.nanmean(ER)),
                     "err_pub_p10": float(np.nanpercentile(ER, 10)), "err_pub_p90": float(np.nanpercentile(ER, 90)),
                     "overconf_mean": float(np.mean(OC)), "share_runs_publishing_nothing": float(np.mean(np.isnan(ER)))})
    e3["strategies"][strat] = rows
res["E3_india_local_calibration"] = e3

# ---- E4: change instrument (copied from committed report, grouped CV by event) ----
res["E4_change"] = {"source": "training/calibration/reports/sar_logratio_change.md",
                    "maps": {"raw score": [0.255, 0.517, 0.53, 0.358], "borrowed water map": [0.214, 0.517, 0.44, 0.311],
                             "one map": [0.152, 0.319, 0.31, 0.605], "regime maps": [0.041, 0.638, 0.67, 0.335]},
                    "fields": ["ECE", "AUROC", "coverage_at_0.6", "error_when_published"],
                    "regimes": {"no change": [635, 0.677], "change": [213, 0.272]}}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res["E1_test"].items() if not k.startswith(("curve", "rel"))}, indent=1))
for k, v in e2.items():
    print(k, {kk: round(vv, 3) if isinstance(vv, float) else vv for kk, vv in v.items()})
for s, rows in e3["strategies"].items():
    print(s)
    for r in rows:
        print("  ", {kk: round(vv, 3) for kk, vv in r.items()})

# ---- E5: ranking quality per event (AUROC of raw score), per-chip mean IoU ----
def auroc(s, y):
    from scipy.stats import rankdata
    y = np.asarray(y); pos, neg = y == 1, y == 0
    if pos.sum() == 0 or neg.sum() == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * neg.sum()))

e5 = {ev: {"auroc_raw": auroc(g.raw.values, g.correct.values), "mean_iou": float(g.iou.mean()), "n": len(g)}
      for ev, g in allrows.groupby("event")}
te = allrows[allrows.split == "test"]
e5["_test_all"] = {"auroc_raw": auroc(te.raw.values, te.correct.values), "mean_iou": float(te.iou.mean()), "n": len(te)}
bo = allrows[allrows.split == "bolivia"]
e5["_bolivia_split"] = {"mean_iou": float(bo.iou.mean()), "n": len(bo)}
res["E5_ranking"] = e5
OUT.write_text(json.dumps(res, indent=1))
for k, v in e5.items():
    print(k, {kk: round(vv, 3) for kk, vv in v.items()})
