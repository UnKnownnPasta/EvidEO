---
id: 001
title: "GeoChat: Grounded Large Vision-Language Model for Remote Sensing"
authors: "Kartik Kuckreja, Muhammad Sohail Danish, Muzammal Naseer, Abhijit Das, Salman Khan, Fahad Shahbaz Khan"
year: 2024
venue: "CVPR 2024"
link: https://arxiv.org/abs/2311.15826
code: https://github.com/mbzuai-oryx/geochat
category: rs-vlm
era: recent
tags: [vlm, grounding, referring-detection, vqa, scene-classification, llava, instruction-tuning, optical-rgb]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2311.15826; 2026-10-14 full-text read via curl of https://arxiv.org/html/2311.15826 (v1, the only arXiv version; no appendix or limitations section exists in it) converted to plain text (sections read: abstract, 1 to 6 in full, Tables 1 to 10, references; keyword grep for calibration, abstention, provenance, SAR, cloud, CPU and plain-language terms); 2026-10-29 second full-text read from the PDF (see the 2026-10-29 section below)"
takeaway: "Baseline RS chat model (RGB only, 7B, LoRA on LLaVA-1.5); reuse its task-token routing and dataset-to-instruction recipe, but do not trust VLM-emitted boxes (10.6% referring detection acc@0.5, Table 7)"
---

# GeoChat: Grounded Large Vision-Language Model for Remote Sensing

## Problem
General-purpose vision-language models answer satellite queries poorly and can fabricate details. Remote sensing scenes are high resolution, span many scales and contain many small objects, so useful answers need region-level reasoning and spatial grounding, not just a whole-image caption. Earlier RS VQA models treated answering as classification over fixed answers.

## Approach
GeoChat follows the LLaVA-1.5 design: a frozen CLIP ViT-L/14 encoder, a frozen two-layer MLP adaptor (pretrained by LLaVA), and Vicuna-v1.5 7B fine-tuned with LoRA (rank 64 on the query and value matrices). Three task tokens ([grounding], [identify], [refer]) switch between grounded conversation, region captioning and referring detection; VQA and classification use a "single word or phrase" prompt suffix instead. Boxes are written as text, normalised to 0 to 100, with a rotation angle. Positional encodings are interpolated so the encoder runs at 504x504 (1296 patches) instead of 336x336. Training: one epoch on all data (2400 steps), then 1600 more steps on grounding data only (Sec. 3, 5.1).

## Data and benchmarks
About 318k instruction pairs (306k train, 12k test; Table 1) built from SAMRS (DOTA, DIOR, FAIR1M), NWPU-RESISC-45, RSVQA-LRBEN and FloodNet (Table 2). Missing classes such as buildings, roads and trees were pseudo-labelled with a ViTAE-RVSA model trained on LoveDA; attributes (colour, relative size, 3x3 position, relations) were extracted by rule and turned into referring expressions with templates; Vicuna wrote conversations from text descriptions alone (Sec. 4). Evaluation: scene classification on UCMerced (full set) and AID (20% split), VQA on RSVQA-LRBEN test and RSVQA-HRBEN test set 2 (count and area questions omitted), plus a new grounding benchmark from the SAMRS validation set (7653 [refer], 758 [grounding], 555 grounding-description questions).

## Key results
- Zero-shot scene classification: 84.43% UCMerced, 72.03% AID (Table 5).
- RSVQA-LRBEN: presence 91.09, comparison 90.33, rural/urban 94.00, printed average 90.70 (Table 6). The plain mean of the three sub-scores is 91.81; the printed 90.70 lies inside the sub-score range, so it may be a question-weighted overall figure, but the paper does not say. LHRS-Bot (entry 005, Table 3) reprints GeoChat as 91.81, EarthDial (entry 003, Table 10) reprints 90.70. Note LRBEN training data (56k pairs) is in GeoChat's instruction set, so this is not zero-shot.
- RSVQA-HRBEN zero-shot: presence 58.45, comparison 83.19, average 72.30 (Table 8).
- Referring detection acc@0.5: small 2.9, medium 13.6, large 21.7, single-object 16.0, multi-object 4.3, overall 10.6 (Table 7).
- Grounding description: acc@0.5 11.7, METEOR 48.9 (Table 9). Region captioning ROUGE-1 87.3 (Table 10).

## Limitations
The paper has no limitations section; it only notes grounding performance is low for small objects and multiple boxes (Sec. 5.4). From the results: grounding is the clear weak spot (Table 7). Inputs are RGB optical only, single date. The 504x504 interpolation is a workaround for large tiles, not a tiling scheme (our reading). The RSVQA-LR number mixes in-distribution training data with a "zero-shot" framing. No calibrated confidence, no abstention, no data provenance.

## What it means for EvidEO
- Treat GeoChat as the baseline "RS chat" reference: its 7B LLaVA stack is too heavy for our CPU prototype, but its task-token idea (separate modes for classify, caption, VQA, ground) maps cleanly onto our query router.
- Do not rely on VLM-emitted boxes for object detection: its grounding numbers are low, so pair the language layer with a dedicated detector and report detector confidence.
- RGB only means it cannot serve monsoon-season flood queries; EvidEO must keep a Sentinel-1 path that does not depend on this model family.
- Its instruction-pair recipe (convert existing labelled datasets into templated Q and A) is a cheap template for our planned LoRA fine-tune data.
- Benchmark against its UCMerced/AID zero-shot numbers when reporting RemoteCLIP scene classification, so judges can compare like for like. When citing its RSVQA-LR figure, say which average (90.70 printed or 91.81 unweighted) is used.

## Full-text check (2026-10-14)
Ingredients (GeoChat's own system as built and evaluated):
- C1 calibrated per-answer confidence: No. No probability is attached to answers; no calibration analysis anywhere (whole text grepped; the only "uncertainty" hit refers to ambiguity between tasks, Sec. 3.1).
- C2 threshold abstention with next step: No. No refusal or decline behaviour is described.
- C3 scene receipts that reproduce: No. Inputs are image chips; no scene IDs, dates or re-run checks.
- C4 SAR chosen automatically under cloud: No. RGB only (Table 2); no SAR or cloud handling.
- C5 CPU or offline: No. 7B Vicuna plus CLIP; no CPU or quantised inference reported.
- C6 plain-language questions for non-experts: part. Free-form natural-language dialogue is supported (Fig. 1, Sec. 3), but grounding modes need task tokens and VQA needs constrained prompts; no non-expert users or user study.

Corrections to the abstract-level entry: added the RSVQA-LR average discrepancy (90.70 printed vs 91.81 unweighted) and that LRBEN training data is in the instruction set; added HRBEN, grounding-description and region-captioning numbers with table refs; noted LoRA rank, frozen encoder and adaptor, two-stage schedule; clarified that the paper has no limitations section, so the "workaround" remark is our reading.

Novelty impact: none. GeoChat scores 0 Yes and 1 part, so it does not threaten EvidEO's "no prior system combines more than two of C1 to C6" claim.

## Full-text check (2026-10-29)
Read the full arXiv v1 PDF (10 pages).
- The 90.70% on RSVQA-LRBEN covers presence, comparison and rural/urban questions only. The paper omits area and count questions "because the responses are numerical". Those are the questions EvidEO cares about.
- Table 6 prints an average of 90.70 for GeoChat, but its three columns (91.09, 90.33, 94.00) average 91.81, which is the figure LHRS-Bot's paper reports for it. The printed average is internally inconsistent. GeoChat is not best on LR (RSGPT 92.29, which was fine-tuned on the target data).
- Zero-shot RSVQA-HRBEN average is 72.30 (presence 58.45, comparison 83.19).
- 10.6% overall acc@0.5 (Table 7): small 2.9, medium 13.6, large 21.7; multi-object 4.3; [refer] 10.5, [grounding] 11.8. The benchmark is built by the authors from SAMRS validation images with templated expressions and pseudo-labelled classes, so it is not human-written referring expressions.
- FloodNet (aerial, post-flood) is in the training mix and Fig. 5 shows a confident flood answer ("three buildings are flooded"), with no flood-specific score.
- No confidence, calibration or abstention anywhere in the text. Venue (CVPR 2024) is not in this v1 PDF.
