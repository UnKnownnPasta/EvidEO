---
id: 227
title: "Land cover and flood type govern the detection limits of satellite-based flood mapping across diverse global flood events"
authors: "Venkatesh Kolluru, Rajat Shinde, Abdelhak Marouane, Caden Helbling, Deepak Shah, Othneil Drew, Iksha Gurung, Manil Maskey, Rahul Ramachandran"
year: 2026
venue: "arXiv preprint (arXiv:2606.07780, v1 5 June 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.07780
code: "none found in the abstract page"
category: upcoming
era: upcoming
tags: [flood-mapping, prithvi-eo-2, land-cover, flood-type, gfm, opera-dswx, failure-modes, reference-disagreement]
verified: "2026-10-12 via WebFetch of arxiv.org/abs/2606.07780 (title, nine authors, abstract numbers) and curl to export.arxiv.org/api/query?id_list=2606.07780 (published 2026-06-05); body text read only as summarised by the fetch tool"
takeaway: "Across 19 unseen flood events, Prithvi-EO-2.0 detection depends on land cover and flood type (cropland IoU 52%, tree cover and built-up about 4%, riverine F1 0.69 vs flash and cyclone about 0.55); a plausible mechanism for EvidEO's region-dependent over-confidence, and support for per-regime calibration"
---

# Kolluru et al. 2026, detection limits of satellite flood mapping

## Problem
Flood mapping models are usually scored on benchmark splits drawn from the same events they were trained near. How they behave on new events, climates and flood mechanisms is less known.

## Approach
Run Prithvi-EO-2.0 (an optical geospatial foundation model) on 19 flood events from 2017 to 2025 that were outside its fine-tuning data, spanning six continents, eight climate zones and six flood mechanisms. Compare against two reference products, the SAR-based Copernicus GFM and the optical OPERA DSWx-HLS, and break agreement down by land cover and flood type.

## Data and benchmarks
19 events; references GFM and DSWx-HLS; land cover strata and flood mechanism labels.

## Key results
- Cropland had the highest agreement (IoU 52%); tree cover and built-up areas were near zero (about 4%) whatever the flood mechanism.
- Riverine floods were detected best (F1 0.69); tropical cyclone (0.56) and flash floods (0.55) were lower (body text, as summarised by the fetch tool).
- Part of the apparent error came from the two reference products defining floods differently.
- The authors list 23 pipeline failure modes and conclude that pipeline engineering, more than model capacity, drove initial error.

## Limitations
Optical model only, so it does not measure SAR misses directly. References are themselves products, not hand labels. Preprint.

## What it means for EvidEO
1. **Mechanism for our transfer result.** Our paper draft finds global answer calibration over-confident on South Asian events. Land cover (paddy, vegetated and built-up flooding) and flood type changing detection quality is a plausible cause; it argues for calibration offsets per land-cover and flood-type regime, not only per region.
2. **Pipeline over model.** Their finding that engineering failures dominated matches ours (GDAL decimation non-determinism, silent tile drop-outs). Keep receipts and failure logging central.
3. **Reference disagreement.** When we validate district cards against NRSC or GFM maps, disagreements may be definitional; report them as such.
