"""Draw docs/figures/workflow.png: the six steps from a question to an evidence card, one slide wide.
Usage: python tools/make_workflow_figure.py   (needs matplotlib)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

STEPS = [
    ("1  Ask", "#7c6cf0", ["Plain words, any district,", "two dates. English, Hindi", "or Hinglish.", "\"How much of Barpeta was", "under water on 11 July?\""]),
    ("2  Configure", "#5b8def", ["Rules read place, dates and", "question type.", "Shown as an editable", "configuration; nothing runs", "until you confirm."]),
    ("3  Find scenes", "#2fa4a0", ["Public Sentinel catalogues.", "Monsoon: radar first", "(sees through cloud).", "Only the district's pixels", "are read, not whole scenes."]),
    ("4  Measure", "#3aa66a", ["District cut into 5 km tiles,", "run in parallel.", "Fixed, versioned instrument:", "threshold the radar signal,", "optional: skip steep or high ground."]),
    ("5  Trust check", "#e0a030", ["Confidence fitted on", "hand-labelled flood maps.", "Below 0.60: no number,", "instead \"insufficient", "evidence\" and what helps."]),
    ("6  Evidence card", "#d6604d", ["Number, map overlay,", "scene IDs and dates,", "confidence, caveats.", "Receipt that re-runs to", "the same result."]),
]

fig, ax = plt.subplots(figsize=(16.7, 6.2))
ax.set_xlim(0, 16.7); ax.set_ylim(0, 6.2); ax.axis("off")
fig.patch.set_facecolor("#f5f6fd")
ax.text(0.3, 5.8, "From a question to an evidence card", fontsize=20, fontweight="bold", color="#23264a", va="center")
w, gap, x0 = 2.6, 0.15, 0.3
for i, (title, col, lines) in enumerate(STEPS):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, 3.75), w, 1.15, boxstyle="round,pad=0.02,rounding_size=0.18", fc=col, ec="none"))
    ax.text(x + w / 2, 4.32, title, ha="center", va="center", fontsize=15, fontweight="bold", color="white")
    ax.add_patch(FancyBboxPatch((x, 0.55), w, 2.9, boxstyle="round,pad=0.02,rounding_size=0.18", fc="white", ec="#d9dcf2", lw=1.5))
    for j, t in enumerate(lines):
        ax.text(x + 0.15, 3.05 - j * 0.5, t, fontsize=9.6, color="#23264a", va="center")
    if i < len(STEPS) - 1:
        ax.annotate("", xy=(x + w + gap + 0.02, 4.32), xytext=(x + w - 0.02, 4.32), arrowprops=dict(arrowstyle="-|>", color="#23264a", lw=2))
ax.text(0.3, 0.2, "The language layer only reads the question and words the answer. Every number comes from step 4.",
        fontsize=11.5, color="#555a85", va="center", style="italic")
fig.savefig("docs/figures/workflow.png", dpi=110, facecolor=fig.get_facecolor())
