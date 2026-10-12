# EvidEO paper (formerly SatClip) (IEEE conference format)

- `evideo.tex`, `refs.bib`: the paper (IEEEtran conference class, 6 pages). Build with `latexmk -pdf evideo.tex`.
- `evideo.pdf`: compiled copy.
- `analysis/experiments.py`: every number in the paper, from the committed per-chip rows in `training/calibration/reports/`. Writes `analysis/results.json`. Seeded and deterministic.
- `analysis/figures.py`: all figures in `figures/` (PDF for the paper, PNG for slides).

Rebuild everything: `python paper/analysis/experiments.py && python paper/analysis/figures.py && cd paper && latexmk -pdf evideo.tex`

## Honest assessment (2026-10-12)

**Is it publishable?** Yes as a workshop or short conference paper, not yet as a journal paper.

What carries it:
1. A clear, testable claim at the level of the answer, not the pixel: calibrated abstention cuts wrong published area answers from 45% to 26% on held-out Sen1Floods11 chips at 43% coverage.
2. A new empirical finding: calibration fitted elsewhere is over-confident on every South Asian event (India +20, Pakistan +29, Sri Lanka +10 points) and under-confident on the USA (-31). A few local labels fix the offset, at a large and honest cost in coverage.
3. A working, open, reproducible system (8 of 8 receipts identical).

What a reviewer will attack, and how the paper answers:
- "The detector is weak." Admitted up front: per-chip IoU 0.362 vs 0.359 for the published Otsu baseline (Table I). The claim is about gating answers, not segmentation.
- "Small n, one Indian event." Admitted in Limitations. The fix is labelling chips from two or three more Indian events (Assam, Bihar), which would also turn Fig. 7 into a true cross-event test. This is the single most valuable next experiment.
- "No head-to-head with a VLM on the same questions." True. Running Qwen2-VL-2B or EarthDial on the same 82 test chips with a "how many km2 of water" prompt, on a Colab GPU, would close this gap in a day.
- "No user study." True; noted as the most important missing evidence.

**Suggested venues** (check current deadlines before committing): IEEE IGARSS 2027 (4-page summary, deadline usually mid-January), IEEE InGARSS (India GRSS conference), CVPR 2027 EarthVision workshop (deadline usually March), ICLR or NeurIPS workshops on ML for remote sensing or climate (Tackling Climate Change with ML). Posting to arXiv first is reasonable and timestamps the work.

**On "copyrighting the tech"** (not legal advice; we are not lawyers):
- The code and paper text are already protected by copyright automatically. The repo is under the BSD 2-Clause licence, which lets anyone reuse the code with attribution. If you want to keep commercial control, change the licence for future versions before more people fork it (past BSD releases stay BSD).
- Ideas and methods are not covered by copyright. Patents cover methods, but in India "computer programmes per se" are excluded (Patents Act section 3(k)), the method combines known parts (thresholding, Platt scaling, abstention), and the repo has been public since 4 October 2026, which counts as prior disclosure in most jurisdictions. A patent is therefore unlikely to be worth pursuing.
- What you can protect cheaply: the name "EvidEO" as a trademark (the old name "SatClip" collides with SatCLIP, Klemmer et al., AAAI 2025, archive A226, so it was dropped), and priority as authors by publishing (arXiv now, venue later). Publication is also a defensive move that stops others patenting the same combination.
- If SIH rules or your institute have IP terms for hackathon or student work, check those before licensing decisions.
