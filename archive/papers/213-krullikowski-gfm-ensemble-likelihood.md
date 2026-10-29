---
id: 213
title: "Estimating Ensemble Likelihoods for the Sentinel-1-Based Global Flood Monitoring Product of the Copernicus Emergency Management Service"
authors: "Christian Krullikowski, Candace Chow, Marc Wieland, Sandro Martinis, Bernhard Bauer-Marschallinger, Florian Roth, Patrick Matgen, Marco Chini, Renaud Hostache, Yu Li, Peter Salamon"
year: 2023
venue: "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing (JSTARS), 16, 6917-6930 (2023), DOI 10.1109/JSTARS.2023.3292350; preprint on TechRxiv, DOI 10.36227/techrxiv.22688101"
link: https://doi.org/10.1109/JSTARS.2023.3292350
code: "Not released; the likelihood layer is distributed operationally as part of Copernicus GFM"
category: trust-calibration
era: recent
tags: [gfm, copernicus, ensemble, likelihood, uncertainty, sentinel-1, flood-mapping, user-communication, exclusion-mask, majority-vote]
verified: "2026-10-09 via curl to api.crossref.org (JSTARS record: title, 11 authors, volume, pages, DOI; TechRxiv preprint record with full abstract; the preprint lists 10 authors, without Renaud Hostache); WebFetch of the GFM Product Definition wiki at extwiki.eodc.eu (likelihood layer range and the 50 cut-off, LIST/DLR/TUW algorithms, TUW uncertainty flipped). IEEE Xplore and TechRxiv full text did not render, so harmonisation formulas and any numeric accuracy were not read; 2026-10-14 full-text read via the open-access published PDF on DLR eLib (elib.dlr.de/196314, located through the OpenAlex record) converted with pdftotext (sections read: Abstract, I Introduction, II Algorithm Likelihoods A to D, III Ensemble Likelihoods incl. eqs 4 and 5 and the quantile-quantile evaluation, IV Datasets, V Results, VI Discussion A to D, VII Conclusion); 2026-10-29 second full-text read from the PDF (see the 2026-10-29 section below)"
read_depth: "full"
takeaway: "Copernicus GFM gives every valid Sentinel-1 flood pixel a 0 to 100 likelihood by rescaling and averaging the uncertainty outputs of three independent algorithms, with majority voting deciding the class; a single-site quantile-quantile check shows the values are only roughly reliable (mostly over-predicting flood), so EvidEO can mimic the agreement layer cheaply but must calibrate before calling it a probability"
---

# Krullikowski et al. 2023, GFM ensemble likelihoods

## Problem
The Copernicus Global Flood Monitoring (GFM) service produces a flood mask for every new Sentinel-1 IW GRD scene worldwide by combining three independently developed algorithms (from DLR, LIST and TU Wien). Each algorithm expresses uncertainty differently, so the service needed a single, comparable per-pixel likelihood to communicate confidence to users. The authors deliberately say "likelihood" rather than "uncertainty" because users grasp it more intuitively (Sec I-A).

## Approach
- Individual uncertainty outputs (Sec II): DLR averages three fuzzy memberships (backscatter near the threshold, slope, size of the connected water body) on 0 to 100 with a cut at 60; LIST uses change detection against a same-orbit reference scene and takes the minimum of water-class and change-class posterior probabilities; TU Wien uses Bayesian inference on a Sentinel-1 data cube and outputs the conditional error (0 to 0.5, rescaled to 0 to 100), with its own mask for errors above 0.2.
- Harmonisation (Sec III-A, eqs 4 and 5): DLR fuzzy values are stretched above 60 (100 minus 1.25 times the gap to 100) and divided by 1.2 below 60, so 50 becomes the shared cut; TU Wien uncertainty is inverted for flood pixels; LIST probabilities are used as is.
- Ensemble likelihood is the unweighted mean of the available layers. The class comes from majority voting; split situations (one algorithm nodata, two disagree) are set to non-flood. Flooded pixels later removed by exclusion masks or blob removal get likelihood 49; reference water gets 0.
- The exclusion layer marks pixels where flood mapping is not possible (radar shadow, dense vegetation, permanent low backscatter, terrain not prone to flooding) as nodata in both flood and likelihood layers.

## Data and benchmarks
- Myanmar flood event: Sentinel-1 scene of 2019-07-16, about 90% agriculture; validated against a manually mapped Sentinel-2 L1C flood extent from 2019-07-15.
- Somalia non-flood monitoring case: Sentinel-1 scene of 2019-03-16, about 90% shrubs and 10% agriculture, chosen as hard for SAR (dry soil look-alikes).
- All inputs resampled to 20 m in Equi7Grid; Copernicus Land Cover 2019 (100 m) for stratification.

## Key results
- Quantile-quantile plot of predicted vs empirical flood probability in ten bins for Myanmar (Fig 5): low and high values roughly line up, but most samples show predicted probability above empirical (flood over-prediction relative to Sentinel-2), and empirical probability never exceeds 0.9. No ECE or other scalar error is reported.
- Myanmar: about 10% of pixels flagged flooded; full-agreement floods sit at likelihood 80 to 100, majority floods at 50 to 80; split pixels around 50 along seasonal water bodies are reclassified to non-flood (Figs 6 to 8).
- Somalia: no flood classified; split situations along dried river channels (water look-alikes) are removed by the consensus rule, which the authors credit with significantly reducing overdetection (Sec VI-B, VI-C).
- Results are qualitative and figure-based; there are no accuracy tables.

## Limitations
- Averaging rescaled probabilities and fuzzy memberships gives a heuristic confidence index; the authors call it a heuristic (Sec I-B, VII) and their one Q-Q check shows over-prediction, so a likelihood of 70 is not shown to mean 70% of such pixels are flooded.
- Evaluation on one validated site plus one unvalidated site, neither in South Asia; validation data are Sentinel-2 derived, a day apart and affected by cloud.
- Low-confidence split pixels are silently set to non-flood rather than flagged, which can hide misses.
- Running three full algorithms is heavier than a single threshold.

## What it means for EvidEO
- Adopt in sar_water_otsu: run two or three cheap, different water tests on the same scene (Otsu on VV, Otsu on VH, and a change test against a dry reference from sar_logratio_change) and report per-pixel agreement on a 0 to 100 scale, with the 50 cut used for the mask, mirroring GFM.
- Adopt: show the agreement layer in answers ("3 of 3 methods agree on 80% of this area") which a district official can read without statistics; GFM's own discussion suggests users verify low-agreement hotspots with extra data before allocating resources.
- Adopt: where a GFM product exists for the same Sentinel-1 scene, use it as a cross-check and flag big disagreements; and copy the exclusion-layer idea as an explicit "cannot map here" output.
- Avoid: do not call the averaged score a probability until it has been calibrated against labels (entry 212 and the calibration entries such as 131 and 133); GFM's own Q-Q plot shows why.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: part. Every valid pixel carries a 0 to 100 likelihood shown to users, and Sec III-B and Fig 5 compare it with empirical probabilities from labelled Sentinel-2 data; but it is not fitted to labels, no calibration error is reported, the check covers one site, and it is per pixel rather than per answer.
- C2 Threshold abstention with a next step: part. The exclusion layer declines to map pixels for stated reasons (radar shadow, dense vegetation, low backscatter, non-floodable terrain; Sec II, IV), and the discussion advises verifying low-likelihood hotspots with additional data (Sec VI-B). There is no confidence-based abstention: split and low-confidence pixels are converted to non-flood (likelihood 49).
- C3 Scene receipts that reproduce: part. The product is tied to individual Sentinel-1 scenes and the paper names exact acquisition timestamps; no re-run or determinism check is reported.
- C4 SAR chosen automatically under cloud: No. SAR only by design; no sensor choice.
- C5 CPU or offline deployment: No. Not addressed (operational cloud service; TU Wien's step is described as computationally slim).
- C6 Plain-language questions for non-experts: No. No question interface, though the "likelihood" wording was chosen for user intuition.

What the abstract-level entry got wrong or left unconfirmed:
- The reduction of false detections in Somalia comes from majority voting with conservative resolution of split pixels, not from averaging the likelihoods.
- The likelihood was evaluated against labels (a Q-Q plot), which the earlier entry did not know; it shows over-prediction.
- Harmonisation formulas, scene dates, resolution and land-cover shares are now confirmed.

Novelty implications: three parts (C1, C2, C3), no full Yes. Does not exceed two full ingredients, but it is the operational system that comes closest on C1 and C2 together for SAR flood mapping, so EvidEO should cite it as the operational baseline for per-pixel confidence and say clearly that EvidEO adds fitted calibration with a reported error, per-answer aggregation and a question interface.
