---
id: 014
title: "GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks"
authors: "Muhammad Sohail Danish, Muhammad Akhtar Munir, Syed Roshaan Ali Shah, Kartik Kuckreja, Fahad Shahbaz Khan, Paolo Fraccaro, Alexandre Lacoste, Salman Khan"
year: 2024
venue: "ICCV 2025 (per official GitHub README); arXiv v2 dated 12 Mar 2025 does not state a venue"
link: https://arxiv.org/abs/2411.19325
code: https://github.com/The-AI-Alliance/GEO-Bench-VLM
category: rs-benchmark
era: recent
tags: [benchmark, mcq, counting, referring-detection, segmentation, temporal, sar, multi-task, open-vlm, gpt-4o]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2411.19325 and https://github.com/The-AI-Alliance/GEO-Bench-VLM; 2026-10-14 full-text read via raw arXiv HTML (arxiv.org/html/2411.19325, v2) converted to text (sections read: abstract, 1-7 incl. Tables 1-5 and figure captions, supplementary S1-S6 incl. Table A1)"
takeaway: "Best model reaches only 41.7% average MCQ accuracy (five options, so chance is 20%) and the best referring-detection precision at IoU 0.5 is 34% (Sphinx; GPT-4o 0.9%), which justifies tool grounding plus abstention; reuse its task taxonomy"
---

# GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks

## Problem
General VLM benchmarks do not test what geospatial work needs (tiny-object counting, fine-grained categories, localization, temporal change, non-optical data), and earlier RS benchmarks cover few tasks each. The authors single out VLEO-Bench (entry 013) for lacking temporal, non-optical and segmentation tasks and RS-specific models.

## Approach
A benchmark of mostly multiple-choice questions built from open datasets with a human-verified pipeline. GPT-4o writes five-option questions: one correct answer, one semantically close distractor (checked manually) and three plausible alternatives. Counting questions use distractors at plus or minus 20% and 40% of the true count. Spatial relations are manually annotated with cross-checking; captions are GPT-4o drafts refined by hand. Referring detection is scored by precision at IoU 0.5 and 0.25, segmentation by mIoU, captions by BERTScore, everything else by accuracy. Thirteen models: LLaVA-1.5, LLaVA-NeXT, LLaVA-OneVision, Sphinx, Ferret, InternVL2, Qwen2-VL, GPT-4o, and RS-specific GeoChat, RS-LLaVA, SkySenseGPT, EarthDial and LHRS-Bot-Nova.

## Data and benchmarks
- Over 10,000 manually verified instructions, 8 categories, 31 sub-tasks: scene understanding, object classification, localization and counting, event detection, captioning, semantic segmentation, temporal understanding, non-optical.
- Sources (Table A1) include RESISC45, PatternNet, AiRound, FireRisk, FGSCR, FAIR1M, DIOR, DOTA, COWC, RarePlanes, NASA Marine Debris, fMoW, xBD, PASTIS (Sentinel-2), FPCD farm ponds, GVLM, DeepGlobe, GeoNRW, So2Sat (SAR and multispectral) and QuakeSet (Sentinel-1 SAR).
- Supplement S5 claims global coverage; there is no India-specific analysis.

## Key results
- Overall average accuracy is stated in text only for the best model: LLaVA-OneVision 41.7%, slightly ahead of GPT-4o, about double chance (abstract and Fig. 4 caption). Overall scores for other models appear only in the Fig. 4 chart and could not be read from the text.
- Category accuracies (Table 2): counting best LLaVA-OneVision 0.4377 (GPT-4o 0.3965); object classification best GPT-4o 0.5863; scene understanding best EarthDial 0.7705; event detection best EarthDial 0.5418; captioning BERTScore best Sphinx 0.6451. Ferret is lowest on most categories.
- Referring expression detection, precision at IoU 0.5 (Table 4; the text mislabels it Table 5): Sphinx 0.3408, EarthDial 0.2429, Qwen2-VL 0.1518, GeoChat 0.1151, SkySenseGPT 0.1082, Ferret 0.0943, LHRS-Bot-Nova 0.0930, GPT-4o 0.0087. At IoU 0.25 Sphinx reaches 0.5289.
- Referring segmentation: no RS model supports it; GLaMM gives mIoU 0.1411.
- Temporal tasks (Table 3): GPT-4o best on disaster type (0.63) and damaged-building counting (0.5667); farm-pond change detection only 0.17 to 0.21 and crop type 0.11 to 0.22 for all four models tested.
- Non-optical (Table 5): earthquake magnitude from SAR best Qwen2-VL 0.2734, GPT-4o 0.0827; SAR land-use classification 0.25 to 0.33. Flood detection is listed as a non-optical task, but no flood score is reported.
- Analyses: counting accuracy is sensitive to how close the distractors are to the true count, and no model stays stable as the gap changes (Fig. 7); accuracy changes with prompt wording, most for GPT-4o and InternVL2 (Fig. 8); feeding Sentinel-2 bands squeezed into three channels lowers accuracy sharply compared with RGB (S3).

## Limitations
- Multiple-choice with a forced pick can overstate ability relative to free-form answers, and distractor spacing (20%, 40%) shapes counting scores, as the paper's own Fig. 7 analysis shows.
- Per-model overall averages other than 41.7% are only in a chart.
- Non-optical coverage is thin (two SAR tasks with results); no Indian geography analysis.
- Venue is taken from the README, not the paper.

## What it means for EvidEO
- Even the best open VLM is weak on geospatial tasks, so the VLM must not be our only source of truth; tool-grounded pipelines plus abstention are justified.
- The referring-detection table is the best single citation for "VLMs cannot localise reliably": 34% at IoU 0.5 for the best model, under 1% for GPT-4o.
- LLaVA-OneVision and Qwen2-VL are strong open candidates for a LoRA base; check CPU feasibility of small variants.
- Adopt the task taxonomy and the chance baseline in our evaluation table.
- Its S3 result (multispectral squeezed to RGB hurts) supports keeping spectral indices in the instrument, not the VLM.

## Full-text check (2026-10-14)
- Changed: added Kartik Kuckreja to the author list; added the MCQ construction details (five options, so 20% chance), the 13 model names, dataset sources, and table-referenced numbers for categories, referring detection, temporal and non-optical tasks. Confirmed that only LLaVA-OneVision's 41.7% overall is given in text; others are chart-only. Noted the Table 4/5 mislabel in the text and that flood detection has no reported score.
- Refusal and calibration: none. Questions are forced-choice, there is no abstain option, no confidence elicitation and no calibration metric. The only "ECE" match in the text is an author first name in a reference.
