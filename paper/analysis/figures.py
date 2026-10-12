"""Figures for the EvidEO paper and deck. Run after experiments.py:  python paper/analysis/figures.py"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "paper/figures"
R = json.load(open(ROOT / "paper/analysis/results.json"))
NAVY, ORANGE, TEAL, PURPLE, GRAY, INK = "#1F5A99", "#D9822B", "#2A9D8F", "#8C5BA8", "#9A9A9A", "#222222"
plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "font.size": 8, "axes.titlesize": 8.5,
                     "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#555555",
                     "axes.grid": True, "grid.color": "#E6E6E6", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
W1, W2 = 3.45, 7.1  # IEEE single and double column widths (in)


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png", dpi=220)
    plt.close(fig)


# ---------- Fig: landscape from the literature (numbers read from the papers' tables) ----------
ground = [  # (label, value %, kind, source)
    ("GPT-4o\n(GEOBench-VLM)", 0.87, "gen"), ("GPT-4V\n(VLEO-Bench)", 7.6, "gen"),
    ("GeoChat\n(own bench.)", 10.6, "rs"), ("Qwen2-VL\n(GEOBench-VLM)", 15.18, "gen"),
    ("EarthDial\n(GEOBench-VLM)", 24.29, "rs"), ("Sphinx\n(GEOBench-VLM)", 34.08, "gen"),
    ("MGVLF, supervised\n(VLEO-Bench)", 76.8, "sup")]
hallu = [("LHRS-Bot", 36.33), ("GeoChat", 44.17), ("LLaVA-1.5", 53.17), ("LHRS-Bot-Nova", 67.0),
         ("Qwen2-VL", 67.83), ("VHM", 68.33), ("mPLUG-Owl3", 69.0)]
fig, (a, b) = plt.subplots(1, 2, figsize=(W2, 2.35), gridspec_kw={"width_ratios": [1.35, 1], "wspace": 0.42})
cols = {"gen": GRAY, "rs": NAVY, "sup": TEAL}
y = np.arange(len(ground))
a.barh(y, [g[1] for g in ground], color=[cols[g[2]] for g in ground], height=0.62)
for i, g in enumerate(ground):
    if g[1] > 60:
        a.text(g[1] - 1.5, i, f"{g[1]:.1f}", va="center", ha="right", fontsize=7, color="white")
    else:
        a.text(g[1] + 1.2, i, f"{g[1]:.1f}", va="center", fontsize=7, color=INK)
a.set_yticks(y, [g[0] for g in ground], fontsize=6.5)
a.set_xlim(0, 88); a.set_xlabel("Grounding accuracy at IoU 0.5 (%)")
a.set_title("(a) Locating the object the question names", loc="left")
a.grid(axis="y", visible=False)
from matplotlib.patches import Patch
a.legend(handles=[Patch(color=GRAY, label="general VLM"), Patch(color=NAVY, label="remote-sensing VLM"),
                  Patch(color=TEAL, label="supervised specialist")], loc="center right", frameon=False)
y2 = np.arange(len(hallu))
b.barh(y2, [h[1] for h in hallu], color=NAVY, height=0.62)
b.barh(y2, [100 - h[1] for h in hallu], left=[h[1] for h in hallu], color="#E9D3BC", height=0.62)
for i, h in enumerate(hallu):
    b.text(h[1] - 2, i, f"{h[1]:.0f}%", va="center", ha="right", fontsize=7, color="white")
b.set_yticks(y2, [h[0] for h in hallu], fontsize=6.5); b.set_xlim(0, 100)
b.set_xlabel("Answers judged hallucination-free by experts (%)")
b.set_title("(b) Remote-sensing VLM answers without hallucination", loc="left")
b.grid(axis="y", visible=False)
save(fig, "fig_landscape")

# ---------- Fig: risk-coverage ----------
e1 = R["E1_test"]
fig, ax = plt.subplots(figsize=(W1, 2.45))
for key, c, lab in (("curve_v10", GRAY, "v1.0 (VV only)"), ("curve_v11", NAVY, "v1.1 (VV or VH)")):
    cv, rk = map(np.array, e1[key])
    ax.plot(cv, rk, color=c, lw=1.8, label=f"{lab}, AURC {e1[key[-3:].replace('v10','v1.0').replace('v11','v1.1')]['aurc']:.2f}" if False else lab)
y_test = None
ax.axhline(e1["v1.1"]["error_always_answer"], color=ORANGE, lw=1.2, ls="--")
ax.text(0.02, e1["v1.1"]["error_always_answer"] + 0.015, "always answer (v1.1): 45% wrong", color="#A35A12", fontsize=6.8)
for tag, c in (("v1.0", GRAY), ("v1.1", NAVY)):
    ax.plot(e1[tag]["coverage_at_0.6"], e1[tag]["error_when_published"], "o", ms=6, color=c, mec="white", mew=1.2, zorder=5)
ax.annotate("published at conf. >= 0.60:\n43% answered, 26% wrong", (e1["v1.1"]["coverage_at_0.6"], e1["v1.1"]["error_when_published"]),
            xytext=(0.47, 0.06), fontsize=6.8, color=INK, arrowprops=dict(arrowstyle="-", color="#777777", lw=0.7))
ax.set_xlabel("Coverage (share of questions answered)"); ax.set_ylabel("Risk (share of answers wrong)")
ax.set_xlim(0, 1); ax.set_ylim(0, 0.75)
ax.legend([plt.Line2D([], [], color=GRAY, lw=1.8), plt.Line2D([], [], color=NAVY, lw=1.8)],
          [f"v1.0 VV only (AURC {e1['v1.0']['aurc']:.2f})", f"v1.1 VV or VH (AURC {e1['v1.1']['aurc']:.2f})"],
          loc="upper left", frameon=False)
save(fig, "fig_riskcov")

# ---------- Fig: reliability (test, raw vs calibrated) ----------
d = pd.read_csv(ROOT / "training/calibration/reports/sar_water_otsu_chips.csv"); d = d[d.status == "ok"]
A, B = e1["v1.1"]["a"], e1["v1.1"]["b"]
fig, axs = plt.subplots(1, 2, figsize=(W1, 1.9), sharey=True)
for ax, (name, sub) in zip(axs, (("Held-out test (82 chips)", d[d.split == "test"]), ("India, fit without India (64)", d[d.event == "India"]))):
    yv = sub.correct.values.astype(float)
    for s, c, lab, mk in ((sub.raw.values, GRAY, "raw score", "s"), (1 / (1 + np.exp(-(A * sub.raw.values + B))), NAVY, "calibrated", "o")):
        bins = np.linspace(0, 1, 6); xs, ys, ns = [], [], []
        for i in range(5):
            m = (s >= bins[i]) & (s < bins[i + 1] + (i == 4) * 1e-9)
            if m.sum() >= 3:
                xs.append(s[m].mean()); ys.append(yv[m].mean()); ns.append(m.sum())
        ax.plot(xs, ys, marker=mk, color=c, lw=1.4, ms=4.5, label=lab)
    ax.plot([0, 1], [0, 1], color="#BBBBBB", lw=0.8, ls=":")
    ax.set_title(name, fontsize=7.2, loc="left"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("Stated confidence")
axs[0].set_ylabel("Observed share correct"); axs[0].legend(frameon=False, loc="upper left")
save(fig, "fig_reliability")

# ---------- Fig: leave-one-event-out calibration transfer ----------
e2 = R["E2_loeo"]
evs = sorted(e2, key=lambda k: e2[k]["overconfidence"])
fig, ax = plt.subplots(figsize=(W1, 2.5))
vals = [e2[k]["overconfidence"] * 100 for k in evs]
south = {"India", "Pakistan", "Sri-Lanka"}
ax.barh(range(len(evs)), vals, color=[ORANGE if k in south else NAVY for k in evs], height=0.62)
for i, k in enumerate(evs):
    v = vals[i]
    ax.text(v + (1 if v >= 0 else -1), i, f"{v:+.0f}", va="center", ha="left" if v >= 0 else "right", fontsize=6.8)
ax.set_yticks(range(len(evs)), [f"{k} (n={e2[k]['n']})" for k in evs], fontsize=6.6)
ax.axvline(0, color="#555555", lw=0.8); ax.set_xlim(-40, 40)
ax.set_xlabel("Mean confidence minus share correct (points)\n<- under-confident        over-confident ->")
ax.grid(axis="y", visible=False)
ax.legend(handles=[Patch(color=ORANGE, label="South Asia"), Patch(color=NAVY, label="other events")], frameon=False, loc="lower right")
save(fig, "fig_loeo")

# ---------- Fig: local calibration budget ----------
e3 = R["E3_india_local_calibration"]; K = e3["K"]
fig, axs = plt.subplots(1, 2, figsize=(W2, 2.1), gridspec_kw={"wspace": 0.3})
for strat, c, lab in (("pooled_refit", GRAY, "add Indian chips to global pool"), ("intercept_only", NAVY, "shift intercept on Indian chips only")):
    rows = e3["strategies"][strat]
    axs[0].plot(K, [r["err_pub_mean"] * 100 for r in rows], "o-", color=c, lw=1.6, ms=3.5, label=lab)
    axs[0].fill_between(K, [r["err_pub_p10"] * 100 for r in rows], [r["err_pub_p90"] * 100 for r in rows], color=c, alpha=0.12, lw=0)
    axs[1].plot(K, [r["coverage_mean"] * 100 for r in rows], "o-", color=c, lw=1.6, ms=3.5, label=lab)
axs[0].set_ylabel("Wrong among published answers (%)"); axs[1].set_ylabel("Questions answered (%)")
for ax in axs:
    ax.set_xlabel("Indian labelled chips used to calibrate"); ax.set_xticks(K)
axs[0].set_ylim(0, 80); axs[1].set_ylim(0, 60)
axs[1].legend(frameon=False, loc="center right", fontsize=6.8)
axs[0].set_title("(a) Reliability of what is published", loc="left"); axs[1].set_title("(b) Price paid in coverage", loc="left")
save(fig, "fig_local")

# ---------- Fig: change instrument calibration ----------
e4 = R["E4_change"]; names = list(e4["maps"])
fig, axs = plt.subplots(1, 2, figsize=(W1, 2.0), gridspec_kw={"wspace": 0.5, "width_ratios": [1.25, 1]})
axs[0].bar(range(4), [e4["maps"][n][0] for n in names], color=[GRAY, GRAY, GRAY, NAVY], width=0.62)
axs[0].set_xticks(range(4), ["raw\nscore", "water\nmap", "one\nmap", "regime\nmaps"], fontsize=6.0); axs[0].set_title("ECE, lower is better", loc="left")
for i, n in enumerate(names):
    axs[0].text(i, e4["maps"][n][0] + 0.006, f"{e4['maps'][n][0]:.3f}", ha="center", fontsize=6.3)
axs[0].grid(axis="x", visible=False)
rg = e4["regimes"]
axs[1].bar([0, 1], [rg["no change"][1] * 100, rg["change"][1] * 100], color=[TEAL, ORANGE], width=0.55)
axs[1].set_xticks([0, 1], [f"no new\nwater\n(n={rg['no change'][0]})", f"X km2\nnew\n(n={rg['change'][0]})"], fontsize=6.3)
axs[1].set_title("Share correct (%)", loc="left"); axs[1].set_ylim(0, 100)
for i, v in enumerate([rg["no change"][1] * 100, rg["change"][1] * 100]):
    axs[1].text(i, v + 2, f"{v:.0f}", ha="center", fontsize=6.8)
axs[1].grid(axis="x", visible=False)
save(fig, "fig_change")
print("ok", sorted(p.name for p in FIG.iterdir()))
