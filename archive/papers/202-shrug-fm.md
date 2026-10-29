---
id: 202
title: "SHRUG-FM: Reliability-Aware Foundation Models for Earth Observation"
authors: "Maria Gonzalez-Calabuig, Kai-Hendrik Cohrs, Vishal Nedungadi, Zuzanna Osika, Ruben Cartuyvels, Steffen Knoblauch, Joppe Massant, Shruti Nath, Patrick Ebel, Vasileios Sitokonstantinou"
year: 2026
venue: "CVPR 2026 EarthVision workshop proceedings (per arXiv comment); arXiv:2511.10370 (v1 November 2025, v2 April 2026)"
link: https://arxiv.org/abs/2511.10370
code: "https://github.com/vishalned/SHRUG-FM (stated in the paper; repository contents not inspected)"
category: trust-calibration
era: recent
tags: [selective-prediction, abstention, ood-detection, geospatial-foundation-model, flood-mapping, worldfloods, risk-coverage, decision-tree, ssl4eo-s12, sentinel-2]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2511.10370 (title, authors, dates, EarthVision 2026 comment, abstract), WebFetch of https://arxiv.org/html/2511.10370v2 (signals, datasets, failure thresholds, metrics, key numbers, binary accept/reject output) and curl of the same HTML page (Limitations and Conclusions sections, dataset split sizes); 2026-10-14 full-text read via curl of https://arxiv.org/html/2511.10370v2 converted to text (sections read: Abstract, 1 Introduction, 2 Related Work, 3 Methodology, 4 Data and Experimental Setup, 5 Results incl. Limitations and Deployment considerations, 6 Conclusions, Appendices 7 to 9 with Tables 1 to 5)"
read_depth: "full"
takeaway: "Abstention for EO segmentation that fuses input-space OOD (HydroATLAS and DEM attributes vs pretraining data), embedding OOD and ensemble uncertainty in a depth-3 decision tree; it lowers risk on kept burn-scar, flood and landslide tiles but outputs an uncalibrated binary keep/abstain with only a generic 'inspect by hand' next step; the closest prior art for EvidEO's abstain step"
---

# Gonzalez-Calabuig et al. 2026, SHRUG-FM

## Problem
Geospatial foundation models fail quietly in places unlike their pretraining data. For rapid mapping (floods, burn scars, landslides) users need the model to say when not to trust a prediction.

## Approach
- Three reliability signals per image tile (Sec 3):
  - Input-level OOD: percentile ranks of 21 physical covariates (HydroATLAS hydro-environmental and land-cover attributes, including average slope, plus Copernicus DEM mean, min and max elevation; Table 5) relative to the pretraining set, plus a kernel density estimate of pretraining locations.
  - Embedding-level OOD: normalised distance to the nearest of 64 k-means prototypes of pretraining embeddings, and the Nearest Centroid Distance Deficit (NCDD).
  - Task uncertainty: ensemble mutual information and average entropy, averaged over the predicted event area (pixels above a probability threshold between 0.05 and 0.5).
- Feature selection: drop correlated features, prune input covariates to the 7 most informative, then recursive feature elimination over inputs plus OOD and UQ scores; a shallow decision tree (max depth 3) then maps the selected signals to accept or reject (Sec 3, Appendix 8).
- Failure is defined per task as tile F1 below a cutoff (0.6 for burn scars and floods, 0.5 for landslides), giving test failure rates of 0.33, 0.21 and 0.53.
- Backbone: a ViT-S/16 (about 23M parameters) pretrained with MoCo on SSL4EO-S12, with a deep CNN decoder (about 41M parameters); bootstrap ensemble for burn scars, standard ensembles for floods and landslides.

## Data and benchmarks
- Burn scars: ExEBench, Harmonized Landsat Sentinel-2 imagery over the US 2018 to 2021, 6 bands at 30 m; 804 images split 485 / 54 / 263.
- Floods: WorldFloods, 509 Sentinel-2 L1C flood scenes 2016 to 2019, cut into 256 px patches with at most 10% cloud; 39,060 / 1,854 / 1,936 patches.
- Landslides: Event Reference Data, 28 events from July 2015 on, Sentinel-2 bands in 64 px patches; 225 / 41 / 68 patches.
- Metrics: risk-coverage curves and AURC, discard-performance curves and AUDP, Risk at coverage 0.5 and 0.75; curves averaged over 100 score permutations and 30 training seeds.

## Key results
- Table 2 (lower is better):
  - Burn scars: AURC 0.160 vs 0.224 for the best single signal (normalised distance); Risk@0.5 0.090 vs 0.137 for mutual information.
  - Floods: AURC 0.115 vs 0.159 for mutual information; Risk@0.5 0.107 vs 0.108 (essentially tied); Risk@0.75 0.149, slightly worse than mutual information at 0.139.
  - Landslides: AURC 0.392 vs 0.451 for NCDD (the paper compares against 0.526 for aleatoric uncertainty).
- Ablation (Table 3): removing UQ signals drops flood classifier ROC AUC from 0.725 to 0.524. Removing the input features raises burn-scar ROC AUC from 0.791 to 0.84 (the authors' "input paradox"), and a UQ-only tree matches or beats the full tree on burn scars and floods (risk-coverage AUC 0.138 vs 0.16 and 0.104 vs 0.114).
- Feature persistence (Table 4): mutual information appears in 100% of trees for every task; spatial density in 100% of flood trees.
- The tree gives readable thresholds (Fig 4 example uses NCDD then mutual information).

## Limitations
- Output is binary accept or reject. The authors state probabilities and ensemble scores are used only as relative signals and are not calibrated (Sec 3), so there is no probability to show a user.
- Needs access to the foundation model's pretraining data and attribute alignment, which many providers do not release; ensembles are computationally heavy.
- Failure definitions, feature choice and tree settings are task-specific and sensitive in low-data settings; the authors recommend periodic recalibration with new labels under shift.
- The full fusion adds little over uncertainty alone in two of three tasks (Table 3), so most of the gain comes from ensemble mutual information.
- Flood evaluation is optical Sentinel-2 only (pretraining saw Sentinel-1, the downstream tasks do not), and is tile-level rather than per question.

## What it means for EvidEO
- Adopt: the idea of an input-space OOD check using physical attributes. EvidEO can flag districts or dates whose terrain, slope, or backscatter statistics fall outside the range where the Otsu threshold was validated, and feed that into abstention. Note their own ablation shows such features can add noise in small data, so test it.
- Adopt: risk-coverage curves and AURC as the evaluation format for EvidEO's abstain-below-threshold rule, and report a single strongest-signal baseline alongside the fused rule.
- Beat: EvidEO should map its signals to a calibrated probability (entries 26, 126, 127) rather than a bare keep/reject, and show that number with the scene receipt.
- Novelty: weakens the claim modestly. It shows abstention for EO flood mapping is already published (CVPR EarthVision 2026), so EvidEO cannot claim abstention for satellite flood products as new. It does not provide calibrated confidence, a question interface, scene receipts, live retrieval or SAR fallback, so the combination claim survives; EvidEO should cite it as the nearest abstention prior art.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. Sec 3 says the scores are relative signals and are deliberately not calibrated; no ECE or reliability diagram anywhere.
- C2 Threshold abstention with a next step: part. A learned depth-3 tree with readable thresholds abstains per tile (Sec 3, Fig 4); the only next step is generic (the abstain label signals the user to inspect the prediction by hand, Sec 3). The deployment section recommends showing the top contributing signals and routing to analysts, but this is advice, not built or evaluated.
- C3 Scene receipts that reproduce: No. Results are averaged over seeds and permutations; no per-answer scene IDs, dates or re-run record.
- C4 SAR chosen automatically under cloud: No. Downstream tasks use optical HLS or Sentinel-2 only; cloudy WorldFloods patches above 10% are filtered out.
- C5 CPU or offline deployment: No. Not addressed; ensembles of a 23M encoder plus 41M decoder, which the authors call computationally demanding.
- C6 Plain-language questions for non-experts: No. No question interface.

What the abstract-level entry got wrong or left unconfirmed:
- Slope comes from HydroATLAS, not the Copernicus DEM (the DEM supplies elevation statistics only).
- "About seven selected features" was imprecise: input covariates are pruned to 7, then RFE selects the final tree features with the OOD and UQ scores.
- The flood headline (AURC 0.115) hides that at fixed coverage the fused tree ties or slightly trails mutual information alone (Risk@0.75 0.149 vs 0.139, Table 2), and Table 3 shows UQ-only matches the full fusion.
- Burn-scar split sizes, landslide split sizes and test failure rates are now confirmed.

Novelty implications: one ingredient at most partly delivered (C2). Does not threaten the "no more than two" claim. It does strengthen the case that EvidEO must add calibration and an actionable next step, since the strongest EO abstention prior art has neither.
