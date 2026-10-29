# How NRSC produces SAR flood answers: method and published results

Review date: 2026-10-29. Sources read in full text unless noted. Figures were viewed only where stated; supplements were not read.

| Source | What it is | Read how |
|---|---|---|
| NRSC, Flood Affected Area Atlas of India, technical document (ndem.nrsc.gov.in, 6 pages) | NRSC's own method description for the national atlas | Full text; pages 2 and 3 viewed as images. Its Figures 2 and 3 (flowcharts) are not in the PDF |
| Suresh Babu et al., Current Science 126(9), 2024, "Effective utilization of RISAT-1A multi-mode satellite data for near real time flood mapping and monitoring" (NRSC authors) | Operational method and validation | Full text PDF; Figures 1 to 4 not viewed |
| Chimata et al., NHESS 25, 2455 (2025), "Automated rapid estimation of flood depth using a DEM and EOS-04-derived flood inundation" (NRSC authors, CC BY, peer-reviewed) | Newer automated method and validation | Full text PDF; figures not viewed; tables recomputed |
| NDEM map sheet, Odisha DANA cyclone, 26.10.2024 | One output sheet | Text only |

## The operational method (Current Science 2024, atlas document)
- Sensor: RISAT-1A / EOS-04 (C-band; HH and HV, not Sentinel-1's VV and VH) in three modes, plus foreign SAR and optical sensors. The paper says RISAT-1A met 40% of the microwave data need from indigenous missions (80% with RISAT-1B).
- Processing: geometric and terrain correction, **Lee speckle filter**, sigma-nought in dB.
- Thresholds: about 200 sample pixels per class (river, flood, urban, forest, agriculture) are read by an analyst from each mode; the resulting dB ranges (their Table 2) set the thresholds. The paper says one threshold cannot be used across areas, seasons and conditions, so a **variable threshold per scene** is used and "validated through ground reports".
- Context steps done by people: land-use/land-cover layer to remove non-water pixels, pre- and post-flood image comparison, river levels and rainfall, visual interpretation. The atlas document adds a state mask, hill mask and hill-shadow mask, removal of isolated pixels, and a pre-flood reference layer of river channel and permanent water.
- Their own dB ranges overlap: for example fine-resolution flood HH runs -32.1 to -14.9 dB while agriculture runs -19.0 to -1.3 dB. That is why the land-use and visual steps exist.
- Scale: 67 maps in 2022 and 91 in 2023 from about 400 scenes across 14 states (their Table 3). Delivered as PDF sheets on NDEM, marked preliminary and for official use.

## Their reported accuracy (Current Science 2024)
Three scenes, one per mode, each compared with an optical map from the same day:

| Scene | SAR area | Optical area | Ratio |
|---|---|---|---|
| Munger, Bihar (FRS vs Cartosat-2E) | 302 ha | 321 ha | 94% |
| Sangrur, Punjab (MRS vs Resourcesat-2 LISS-III) | 7,121 ha | 7,560 ha | 94% |
| Goalpara, Assam (CRS vs Sentinel-2B) | 1,792 ha | 1,969 ha | 91% |

- "Accuracy" here is the ratio of two total areas. It does not say the flooded pixels sit in the same places, and no IoU, F1 or kappa is given.
- The optical reference is itself made by "manual unsupervised/supervised classification and visual interpretation", not surveyed on the ground.
- All three SAR totals are below the optical ones (by 6%, 6% and 9%): a consistent undercount, matching our finding that area answers mostly undercount.
- Scenes were chosen because cloud-free optical imagery existed on the same day (the paper says such pairs are hard to find). That selects the easy conditions.
- On our own criterion (area within 20% of the reference) all three would count as correct, but n = 3.

## The newer automated method (NHESS 2025)
- **It is the same family as our instrument:** automatic tile-based segmentation after Martinis et al. (tiles chosen where the mean backscatter is below the image mean and the standard deviation is above 95% of the image's), a threshold per tile, and the average of tile thresholds applied globally. They use **Otsu**; we use Kittler-Illingworth on bimodal blocks.
- **It adds what we lack:** a HAND mask (flooded pixels kept up to HAND 15 m) and subtraction of a permanent river mask. NRSC says it is the first application of this method and HAND to EOS-04.
- Validation: two scenes only. Bihar against Resourcesat-2 LISS-4 (3 Sep 2023) and Uttar Pradesh against Landsat-8 (15 Aug 2023), reference made by unsupervised classification in ERDAS.
- **Its own tables disagree.** Table 5 (confusion matrices) gives, recomputed: Bihar precision 94.3%, recall 98.7%, F1 96.4%, IoU 93.1%, overall accuracy 94.4%; Uttar Pradesh precision 93.8%, recall 96.5%, F1 95.1%, IoU 90.7%, accuracy 92.2%. Table 6 reports Bihar 95/80/87/94% and Uttar Pradesh 86/76/81/92% (precision/recall/F1/accuracy). Only accuracy matches. Swapping the matrix's rows and columns does not fix it. The text calls the gap "discrepancies due to the characteristics of microwave data", which does not explain it. I cannot say which table is right.
- Both areas are flood-dominated (about 77 to 79% of pixels are flood), so overall accuracy flatters.
- Stated limitations: shallow flowing water classified as dry; moist soil classified as flooded (overestimation); best when the whole scene is covered; hill slopes need the HAND/slope mask. Flood depth uses a different method and was checked against CWC gauge levels (RMSE 0.805 for the TSA method per the abstract; not studied further here).

## What this means for EvidEO
1. **The expert bottleneck is real and visible.** The operational process is analyst-in-the-loop, scene by scene (sample pixels, variable thresholds, land-use clean-up, visual checks). About 67 to 91 maps a year from RISAT-1A, as PDFs for officials. Turning those steps into fixed, versioned, re-runnable instruments is a real gap, and it is the project's core argument.
2. **On method we are at parity, not ahead.** NRSC's newest automated method is tile-based Otsu plus HAND. Ours is tile-based thresholding without HAND, without a permanent-water layer and without a Lee-type filter. The HAND mask is now the highest-value missing step, and it also matches the radar-shadow error in Sindhudurg (PLOS ONE, entry 31).
3. **Their published accuracy is thin, ours is thicker but not comparable.** Their evidence is 2 or 3 scenes with optical references and an area-ratio or a flood-dominated confusion matrix, with one internal inconsistency. Ours is 82 held-out chips, leave-one-event-out, and an answer-level test, on mostly small-water chips. The numbers (their 91 to 94% against our 55% wrong on Indian chips) must not be set side by side: different metric, different scene selection, different sensor.
4. **The honest advantage is not accuracy. It is access, provenance and a stated confidence.** NRSC's sheets carry a disclaimer but no per-answer probability and no re-runnable receipt. Our card has both. Whether our number is as good as theirs for the same flood is untested.
5. **The experiment that settles it:** run our instrument on an Indian event where NRSC published a map (for example the Assam June 2024 maps or the Odisha DANA sheet) and compare extents and areas, with the caveat that NRSC's map is itself an analyst product and the only reference.

## Not done
- Not found: a published NRSC validation with more than a few scenes. Leads not read: Arora et al., J. Earth System Science 2023 (Sentinel-1, Ghaggar basin, validated against an NRSC map; PDF not obtained), Bhatt et al. NRSC reviews, Gupta et al. Current Science 2024 on EOS-04, Sai Bhageerath et al. 2025 (EOS-04 with machine learning).
- Other agencies (CWC, state remote-sensing centres) not reviewed.
