"""Figures for review/REVIEW.md. Every plotted number is copied from the source named beside it.

Run from the repo root: python review/figures.py
"""
import collections
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review" / "figures"
OUT.mkdir(exist_ok=True)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # validated categorical slots 1 to 3
NEUTRAL, INK, MUTED, GRID = "#a3a29c", "#0b0b0b", "#52514e", "#e7e6e2"
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "font.size": 8.5,
    "axes.titlesize": 9, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.labelsize": 8.5,
    "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": INK, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": NEUTRAL, "axes.grid": False,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 8,
    "savefig.dpi": 220, "savefig.bbox": "tight", "savefig.pad_inches": 0.04, "figure.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png")
    plt.close(fig)


def hbars(ax, labels, values, colors=BLUE, fmt="{:g}", xmax=None, xlabel=None, height=0.62):
    """Horizontal bars, largest list item on top, each value printed at the bar end."""
    y = list(range(len(labels)))[::-1]
    ax.barh(y, values, color=colors, height=height)
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", length=0)
    limit = xmax or max(values) * 1.15
    ax.set_xlim(0, limit)
    for yi, v in zip(y, values):
        ax.text(v + limit * 0.012, yi, fmt.format(v), va="center", fontsize=8, color=INK)
    ax.grid(axis="x")
    ax.spines["left"].set_visible(False)
    if xlabel:
        ax.set_xlabel(xlabel)


def box(ax, x, y, w, h, text, face="#eef3fb", edge=BLUE, size=8.5, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012", fc=face, ec=edge, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, weight=weight, linespacing=1.3)


def arrow(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=10, color=MUTED, lw=1, shrinkA=0, shrinkB=0))


# Figure 3. Conceptual framework used in Section 1.2.
fig, ax = plt.subplots(figsize=(7.4, 2.6))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
links = [
    ("1 Parse", "Question becomes\nplace, dates,\nquantity", "Ambiguous district,\nwrong period"),
    ("2 Retrieve", "Right scenes are\nfound and read", "Cloud, missing\npass, invented\ncollection IDs"),
    ("3 Measure", "A number and a\nmask are produced", "Missed built-up or\nvegetated flooding"),
    ("4 Qualify", "Answer gets a\nconfidence or\nan abstention", "Over-confidence\nafter a change\nof region"),
    ("5 Communicate", "A person reads\nit and decides", "Misread probability,\nover-reliance"),
]
w, gap = 0.176, 0.03
ax.text(0, 0.95, "What happens", fontsize=8.5, color=MUTED, weight="bold")
ax.text(0, 0.325, "Typical failure", fontsize=8.5, color=MUTED, weight="bold")
for i, (name, does, fails) in enumerate(links):
    x = i * (w + gap)
    box(ax, x, 0.42, w, 0.46, f"{name}\n\n{does}", size=7.8)
    box(ax, x, 0.0, w, 0.29, fails, face="#fdf0ea", edge=ORANGE, size=7.5)
    if i < 4:
        arrow(ax, (x + w, 0.65), (x + w + gap, 0.65))
save(fig, "fig3_answer_chain")

# Figure 1. Search counts from Supplementary Table S2. Records are not deduplicated across strings.
fig, ax = plt.subplots(figsize=(7.4, 4.1))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
cols = [
    (0.0, ["Annotated corpus\n227 papers, 14 categories", "Read for relevance\nto RQ1 to RQ5", "36 cited"]),
    (0.345, ["Web search, 2026-11-06\n14 queries", "Candidates verified against\npublisher or preprint pages", "5 new primary sources\n3 reporting guidelines"]),
    (0.69, ["Database search, 2026-11-07\nOpenAlex (8 strings), arXiv (2)\n2,428 records", "434 records considered\n(all of 7 sets, top 100 of 3 others)\nScreened by title and keyword", "11 new primary sources"]),
]
w = 0.31
for x, (a, b, c) in cols:
    box(ax, x, 0.72, w, 0.24, a)
    box(ax, x, 0.40, w, 0.20, b, face="#f5f5f2", edge=NEUTRAL, size=7.8)
    box(ax, x, 0.17, w, 0.13, c, face="#e8f7f1", edge=AQUA)
    arrow(ax, (x + w / 2, 0.72), (x + w / 2, 0.60))
    arrow(ax, (x + w / 2, 0.40), (x + w / 2, 0.30))
    arrow(ax, (x + w / 2, 0.17), (x + w / 2, 0.11))
box(ax, 0.0, 0.0, 1.0, 0.11, "55 references in this review: 52 evidence sources and 3 reporting guidelines", face="#eef3fb", weight="bold")
save(fig, "fig1_search_flow")

# Figure 2. Computed from archive/index.csv.
rows = list(csv.DictReader(open(ROOT / "archive" / "index.csv", encoding="utf8")))
years = collections.Counter(int(r["year"]) for r in rows)
span = list(range(2016, 2027))
early = sum(v for k, v in years.items() if k < 2016)
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.3), gridspec_kw={"width_ratios": [1, 0.9], "wspace": 0.75})
a = axs[0]
labels = ["<2016"] + [str(y) for y in span]
vals = [early] + [years[y] for y in span]
a.bar(labels, vals, color=[NEUTRAL] + [BLUE] * len(span), width=0.68)
for i, v in enumerate(vals):
    a.text(i, v + 0.6, str(v), ha="center", fontsize=7.5, color=INK)
a.set_title("(a) Publication year")
a.set_ylabel("Papers")
a.tick_params(axis="x", rotation=60, length=0)
a.grid(axis="y")
names = {"rs-vlm": "RS vision-language models", "rs-benchmark": "RS benchmarks", "trust-calibration": "Trust and calibration",
         "eo-foundation": "EO foundation models", "change-detection": "Change detection", "sar-optical-fusion": "SAR and optical fusion",
         "indian-context": "Indian context", "eo-agents": "EO agents", "human-factors": "Human factors", "upcoming": "Newly posted work",
         "data-infrastructure": "Data infrastructure", "efficient-inference": "Efficient inference", "historical": "Historical methods",
         "object-detection": "Object detection"}
cats = collections.Counter(r["category"] for r in rows).most_common()
hbars(axs[1], [names[k] for k, _ in cats], [v for _, v in cats], xlabel="Papers", height=0.68)
axs[1].set_title("(b) Topic")
save(fig, "fig2_corpus")

# Figure 4. Zhou et al. 2026 Table 1; Danish et al. 2024 Table 4; Zhang and Wang 2024.
fig, axs = plt.subplots(1, 3, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1, 0.72], "wspace": 0.62})
hf = [("mPLUG-Owl3", 69.00, 0), ("VHM", 68.33, 1), ("Qwen2-VL", 67.83, 0), ("LHRS-Bot-Nova", 67.00, 1),
      ("LLaVA-1.5", 53.17, 0), ("GeoChat", 44.17, 1), ("LHRS-Bot", 36.33, 1)]
hbars(axs[0], [h[0] for h in hf], [h[1] for h in hf], colors=[BLUE if h[2] else ORANGE for h in hf], fmt="{:.1f}", xmax=100, xlabel="Hallucination-free rate (%)")
axs[0].set_title("(a) RSHalluEval, expert-scored")
axs[0].legend(handles=[Patch(color=BLUE, label="RS-specific"), Patch(color=ORANGE, label="General")], loc="upper center", bbox_to_anchor=(0.4, -0.2), ncol=2, handlelength=1, columnspacing=1)
geo = [("Sphinx", 34.08), ("EarthDial", 24.29), ("Qwen2-VL", 15.18), ("GeoChat", 11.51), ("SkySenseGPT", 10.82), ("Ferret", 9.43), ("LHRS-Bot-Nova", 9.30), ("GPT-4o", 0.87)]
hbars(axs[1], [g[0] for g in geo], [g[1] for g in geo], fmt="{:.1f}", xmax=100, xlabel="Precision at IoU 0.5 (%)")
axs[1].set_title("(b) GEOBench-VLM referring")
hbars(axs[2], ["MGVLF\n(specialist)", "GPT-4V"], [76.8, 7.6], colors=[AQUA, ORANGE], fmt="{:.1f}", xmax=100, xlabel="Accuracy at IoU 0.5 (%)", height=0.42)
axs[2].set_title("(c) DIOR-RSVG")
save(fig, "fig4_language_models")

# Figure 5. Ma et al. 2026 Table 2; Shabbir et al. 2026 Table 4; Kao et al. 2026 Sec 4.4; Angelidis et al. 2026.
fig, axs = plt.subplots(2, 2, figsize=(7.4, 4.4), gridspec_kw={"wspace": 0.55, "hspace": 0.62})
hbars(axs[0, 0], ["EO-Gym, tuned 4B", "Gemini-2.5-Pro", "Base 4B"], [0.74, 0.67, 0.49], colors=[BLUE, ORANGE, NEUTRAL], fmt="{:.2f}", xmax=1, xlabel="Pass@3")
axs[0, 0].set_title("(a) EO-Gym")
hbars(axs[0, 1], ["OpenEarthAgent", "GPT-4o", "Base Qwen3-4B"], [45.26, 39.22, 13.72], colors=[BLUE, ORANGE, NEUTRAL], fmt="{:.1f}", xmax=100, xlabel="End-to-end answer accuracy")
axs[0, 1].set_title("(b) OpenEarthAgent")
a = axs[1, 0]
a.barh([1.2, 0.2], [40.0, 15.7], height=0.36, color=NEUTRAL, label="Zero-shot")
a.barh([0.8, -0.2], [64.5, 26.0], height=0.36, color=BLUE, label="With Reflexion")
for y, v in [(1.2, 40.0), (0.8, 64.5), (0.2, 15.7), (-0.2, 26.0)]:
    a.text(v + 1.2, y, f"{v:.1f}", va="center", fontsize=8, color=INK)
a.set_yticks([1, 0], ["Correct", "Wrong answer"])
a.tick_params(axis="y", length=0)
a.set_xlim(0, 100)
a.set_xlabel("Share of questions (%)")
a.grid(axis="x")
a.spines["left"].set_visible(False)
a.set_title("(c) UnivEARTH v3, Claude-4.5-Sonnet")
a.legend(loc="lower right", handlelength=1)
hbars(axs[1, 1], ["Use an LLM in scoring", "Include unanswerable tasks", "Report monetary cost", "Repeat runs", "Measure calibration"], [4, 3, 3, 1, 0], fmt="{:d}", xmax=12, xlabel="Benchmarks, of 12 audited")
axs[1, 1].set_title("(d) What benchmarks measure")
save(fig, "fig5_agents")

# Figure 6. Kolluru et al. 2026 Figs 4 and 8; Soudagar and Thakur 2025 Table 2 and Section 4.
fig = plt.figure(figsize=(7.4, 5.0))
gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.42, height_ratios=[1, 1.15])
a = fig.add_subplot(gs[0, 0])
hbars(a, ["Cropland", "Wetland", "Grassland", "Built-up", "Tree cover"], [52, 45, 41, 4, 4], fmt="{:d}", xmax=100, xlabel="IoU against GFM (%)")
a.set_title("(a) By land cover (optical, 19 events)")
a = fig.add_subplot(gs[0, 1])
hbars(a, ["Riverine (n=6)", "Dam failure (n=3)", "Tropical cyclone (n=7)", "Flash (n=3)"], [0.69, 0.61, 0.56, 0.55], fmt="{:.2f}", xmax=1, xlabel="F1 against GFM")
a.set_title("(b) By flood type (optical)")
a = fig.add_subplot(gs[1, :])
dates = ["8 Jul", "20 Jul", "1 Aug", "13 Aug", "25 Aug", "6 Sep", "18 Sep", "30 Sep", "12 Oct", "24 Oct"]
extent = [215.32, 306.89, 299.44, 209.10, 320.37, 470.27, 116.31, 213.23, 239.49, 268.83]
days = [i * 12 for i in range(10)]
a.plot(days, extent, color=BLUE, lw=2, marker="o", ms=5, label="Measured Sentinel-1 extent")
a.plot([57], [484.13], marker="o", ms=7, mfc="white", mec=ORANGE, mew=1.6, ls="none", label="Reported peak (spline, 3 Sep)")
a.plot([72], [116.31], marker="s", ms=8, color=AQUA, ls="none", label="Only validated scene (18 Sep)")
a.annotate("470 sq km", (60, 470.27), xytext=(63, 490), va="center", fontsize=8, color=INK)
a.annotate("116 sq km", (72, 116.31), xytext=(77, 105), va="center", fontsize=8, color=INK)
a.set_xticks(days, dates)
a.set_ylim(0, 620)
a.set_ylabel("Water extent (sq km)")
a.tick_params(axis="x", length=0)
a.grid(axis="y")
a.set_title("(c) Patna, 2023 monsoon (radar)")
a.legend(loc="upper left", ncol=3, handlelength=1.4, columnspacing=1.2)
save(fig, "fig6_flood_limits")
print("wrote", len(list(OUT.glob("*.png"))), "figures to", OUT)
