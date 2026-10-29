---
id: 227
title: "Land cover and flood type govern the detection limits of satellite-based flood mapping across diverse global flood events"
authors: "Venkatesh Kolluru, Rajat Shinde, Abdelhak Marouane, Caden Helbling, Deepak Shah, Othneil Drew, Iksha Gurung, Manil Maskey, Rahul Ramachandran"
year: 2026
venue: "arXiv preprint (arXiv:2606.07780, v1 5 June 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.07780
code: "Paper points to the general Prithvi-EO-2.0 repository (github.com/NASA-IMPACT/Prithvi-EO-2.0) and a web app (explore.fm.odsi.io); no separate pipeline repository stated"
category: upcoming
era: upcoming
tags: [flood-mapping, prithvi-eo-2, land-cover, flood-type, gfm, opera-dswx, failure-modes, reference-disagreement, red-teaming, hls]
verified: "2026-10-12 via WebFetch of arxiv.org/abs/2606.07780 (title, nine authors, abstract numbers) and curl to export.arxiv.org/api/query?id_list=2606.07780 (published 2026-06-05); body text read only as summarised by the fetch tool; 2026-10-14 full-text read via curl of https://arxiv.org/pdf/2606.07780 (HTML version returned 404) converted with pdftotext (sections read: Abstract, Introduction, Results incl. per-event, postprocessing, stratified, patch-level, visual, land cover, red-teaming and computational sections, Discussion and Conclusions, Data and Methods, Tables 1 to 4, Data and Code Availability)"
read_depth: "partial (main text, methods and Tables 1 to 4 read in full; Supplementary Texts S1 to S6 and Tables S1 and S2, which hold the failure-mode taxonomy details and timing breakdown, are not in the arXiv PDF)"
takeaway: "Across 19 unseen flood events, Prithvi-EO-2.0 on HLS optical imagery reaches mean GFM F1 0.61 and IoU 0.46, with detection governed by land cover and flood type (cropland IoU 52%, tree cover and built-up 4%; riverine F1 0.69 vs cyclone 0.56 and flash 0.55) and worst under heavy cloud (Myanmar F1 0.24); a plausible mechanism for EvidEO's region-dependent over-confidence and support for per-regime calibration"
---

# Kolluru et al. 2026, detection limits of satellite flood mapping

## Problem
Flood mapping models are usually scored on benchmark splits drawn from the same events they were trained near. How they behave on new events, climates and flood mechanisms, and how much error comes from the pipeline rather than the model, is less known.

## Approach
Run the public Prithvi-EO-2.0 600M Sen1Floods11 checkpoint (ViT encoder plus U-Net decoder, threshold 0.5, no further fine-tuning) on HLS 30 m optical imagery for 19 flood events from 2017 to 2025 with no overlap with the 11 Sen1Floods11 training events, spanning six continents, eight climate zones and six mechanisms (riverine, flash, dam breach, typhoon, hurricane, cyclone). Preprocessing masks cloud and shadow with Fmask; postprocessing removes terrain shadow (solar local incidence above 85 degrees and slope above 15 degrees), high-aerosol false water, NDVI above 0.7, and GFM permanent water (Data and Methods). Compare against two reference products, the Sentinel-1 based Copernicus GFM (all 19 events) and the optical OPERA DSWx-HLS (12 events), stratify by size, climate, mechanism and ESA WorldCover class, and analyse 79,885 connected flood patches. A red-teaming process documents pipeline failure modes.

## Data and benchmarks
19 events (Table 1), including South Asian cases (India Patna 2019, Sri Lanka Gampaha 2025, Myanmar Magway 2024); references GFM and DSWx-HLS; WorldCover 2021 land cover; Köppen-Geiger climate zones.

## Key results
- Per event against GFM (Table 3): F1 0.24 (Myanmar) to 0.88 (Libya), mean 0.61; IoU mean 0.46; recall mean 0.90 but precision mean 0.49, with frequency bias above 1 for all 19 events (systematic overdetection). Against DSWx: mean F1 0.65, precision 0.75, recall 0.60. F1 above 0.7 for 10 of 19 events.
- Out-of-distribution gap: mean IoU 0.46 vs 0.83 on the in-sample Sen1Floods11 test.
- Land cover vs GFM (Fig 8): cropland IoU 52% (F1 69%), wetland 45%, grassland 41%; built-up and tree cover IoU 4% (F1 9%). Built-up stays at 0 to 12% IoU across all flood types (Fig 9).
- Flood type vs GFM (Fig 4): riverine F1 0.69 (n=6), dam failure 0.61 (n=3), tropical cyclone 0.56 (n=7), flash 0.55 (n=3). Tropical climates weakest (F1 0.56, n=8).
- Patch analysis: 70.8% of patches are under 0.01 km2; recall vs GFM rises from 0.69 for patches under 0.1 km2 to 0.86 for 10 to 100 km2. Events with fragmentation index below 5 all had F1 above 0.7; above 15, none exceeded 0.5.
- Postprocessing removed 277.41 km2 in total (mean 3.04% per event, up to 18.93% for Italy; Table 4).
- Red teaming found 23 failure modes; data acquisition and preprocessing caused 42% of interruptions. On Brazil, initial DSWx precision and recall of 4.9% and 4.6% rose to 82% and 72% (F1 0.77) after fixes, so pipeline engineering, not model capacity, drove initial error.
- Runtime: 288.2 s per event sequentially on a V100 GPU, 29.9 s in the optimised web deployment (Table S2, not available).

## Limitations
Optical model only, so it does not measure SAR misses directly; cloud-masked areas become false negatives. References are themselves products, not hand labels, and GFM vs DSWx define floods differently. One model and one fine-tuning configuration. Event-level sample sizes per stratum are small (n=2 to 8). The fragmentation threshold is derived and tested on the same 19 events. Preprint; supplementary material not in the arXiv PDF.

## What it means for EvidEO
1. **Mechanism for our transfer result.** Our paper draft finds global answer calibration over-confident on South Asian events. Land cover (paddy, vegetated and built-up flooding), flood type and cloud cover changing detection quality is a plausible cause; it argues for calibration offsets per land-cover and flood-type regime, not only per region. Their worst events (Myanmar, Philippines) are tropical monsoon cases with heavy cloud.
2. **Pipeline over model.** Their finding that engineering failures dominated matches ours (GDAL decimation non-determinism, silent tile drop-outs). Keep receipts, processing logs and regression re-runs central, as they also recommend.
3. **Reference disagreement.** When we validate district cards against NRSC or GFM maps, disagreements may be definitional; report them as such.
4. **Abstention signal.** Patch fragmentation is a cheap, label-free quality feature worth testing as an input to EvidEO's abstention model.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. The model's flood probability is thresholded at 0.5 and never calibrated; the fragmentation index is proposed as a confidence indicator but is an event-level heuristic (Results, Patch-Level section).
- C2 Threshold abstention with a next step: part. The discussion recommends verifying maps with fragmentation above 5 against independent data and not using the model alone for flash, cyclone, tree-cover or built-up events, pointing to SAR products such as GFM or higher-resolution imagery (Discussion). This is guidance, not an implemented abstention; preprocessing checks do reject non-conforming inputs.
- C3 Scene receipts that reproduce: part. Event dates and bounding boxes are listed (Tables 1 and 2), and regression re-runs of all events after each fix are described (Red-Teaming Methodology); no per-answer granule IDs and no determinism check are reported.
- C4 SAR chosen automatically under cloud: No. HLS optical only; SAR appears only as the GFM reference and as a recommendation for future fusion.
- C5 CPU or offline deployment: No. Inference on an NVIDIA V100 workstation and a hosted web app.
- C6 Plain-language questions for non-experts: No. The web app streamlines download, inference and visualisation; no question interface.

What the abstract-level entry got wrong or left unconfirmed:
- The body numbers previously known only via a fetch-tool summary are confirmed (riverine 0.69, cyclone 0.56, flash 0.55), with sample sizes now attached.
- The model overdetects against GFM (precision 0.49, bias above 1 everywhere), which matters if EvidEO uses GFM as a reference.
- Code availability: only the general Prithvi repository is cited, not the pipeline.

Novelty implications: two parts (C2, C3), no full Yes. Does not threaten the "no more than two" claim; it supports EvidEO's emphasis on receipts and regime-aware calibration.
