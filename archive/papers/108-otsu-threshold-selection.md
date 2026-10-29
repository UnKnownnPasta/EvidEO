---
id: 108
title: "A Threshold Selection Method from Gray-Level Histograms"
authors: "Nobuyuki Otsu"
year: 1979
venue: "IEEE Transactions on Systems, Man, and Cybernetics, 9(1): 62-66"
link: https://doi.org/10.1109/TSMC.1979.4310076
code: "none found (implemented in scikit-image threshold_otsu and OpenCV THRESH_OTSU)"
category: historical
era: historical
tags: [thresholding, histogram, otsu, unsupervised, binarization, water-mapping-baseline]
verified: "2026-10-29 full text of 1979 paper (Purdue copy); earlier 2026-10-06 via Crossref"
takeaway: "The default automatic threshold that EvidEO must benchmark Kittler-Illingworth against, and a cheap fallback when the two-Gaussian fit fails"
read_depth: "abstract (abstract page, metadata, README or official page only; some summaries partly from background knowledge (see verified)"
---

# Otsu thresholding

## Problem
Picking a gray-level threshold that separates object from background usually needed manual tuning or assumptions about histogram shape. Otsu wanted a nonparametric, unsupervised rule computed only from the image histogram.

## Approach
- Treat every candidate threshold as splitting the histogram into two classes.
- Choose the threshold that maximizes the between-class variance (equivalently minimizes within-class variance), using only zeroth and first order cumulative moments.
- A single pass over the histogram suffices, and the method extends to multiple thresholds.
- The maximum of the separability measure gives a by-product score of how bimodal the histogram is.

## Data and benchmarks
The paper illustrates the method on a small set of gray-level images and their histograms rather than on a benchmark; no remote sensing data are involved.

## Key results
- Stable, fast, parameter-free threshold selection that became the de facto default in image processing.
- The separability score indicates when a threshold is meaningful at all.

## Limitations
- Biased toward splitting classes of similar size and variance; when water is a small fraction of a tile, the threshold drifts into the land mode.
- Assumes a bimodal histogram; returns a number even on unimodal tiles, which can fabricate water.
- No explicit noise model, so it ignores SAR speckle statistics.

## What it means for EvidEO
- Implement Otsu alongside Kittler-Illingworth on gamma0 dB tiles and record both thresholds in the evidence card receipt; large disagreement is a signal to lower confidence.
- Use Otsu's separability score (or a bimodality test) as a gate: if a tile is not bimodal, do not threshold it, and let the split-based tile selection skip it.
- Never apply Otsu to a whole district histogram where water is a few percent of pixels; that is exactly the small-class failure case.

## Full-text check (2026-10-29)
Read the full 1979 paper (Purdue-hosted copy of the IEEE scan; OCR text, six pages).
- Confirmed: threshold chosen to maximise between-class variance, equivalent to the two other discriminant criteria; extends to several thresholds.
- The paper also defines a separability measure eta* in (0, 1], invariant to shift and scale of the grey levels, as a measure of the "bimodality of the histogram". EvidEO gates tiles with Ashman's D instead; eta* is a cheaper per-tile signal to test.
- It shows the method still returns a threshold on a unimodal histogram (its Fig. 2) and admits it has no proof that the criterion is unimodal. Nothing in it concerns radar or water.
