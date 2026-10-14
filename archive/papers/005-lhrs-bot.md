---
id: 005
title: "LHRS-Bot: Empowering Remote Sensing with VGI-Enhanced Large Multimodal Language Model"
authors: "Dilxat Muhtar, Zhenshi Li, Feng Gu, Xueliang Zhang, Pengfeng Xiao"
year: 2024
venue: "ECCV 2024"
link: https://arxiv.org/abs/2402.02544
code: https://github.com/NJU-LHRS/LHRS-Bot
category: rs-vlm
era: recent
tags: [vlm, openstreetmap, vgi, curriculum-learning, benchmark, lhrs-bench, llama2, weak-supervision]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2402.02544 and https://github.com/NJU-LHRS/LHRS-Bot; 2026-10-14 full-text read via curl of https://arxiv.org/html/2402.02544 (v4, 16 July 2024) converted to plain text (sections read: abstract, 1 to 5, Tables 1 to 7, Appendix 0.A to 0.H including Tables 8 to 12; keyword grep for calibration, abstention, provenance, SAR, cloud, CPU and plain-language terms)"
takeaway: "Copy the OpenStreetMap/VGI auto-captioning trick for cheap Indian training pairs and the shuffled multiple-choice eval protocol; the authors themselves note OSM is sparse in underdeveloped regions"
---

# LHRS-Bot: Empowering Remote Sensing with VGI-Enhanced Large Multimodal Language Model

## Problem
Remote sensing MLLMs are starved of large, well-aligned image-text data, tend to use only high-level visual features, and there was no thorough benchmark to test their RS understanding across many skills.

## Approach
LHRS-Bot uses volunteered geographic information (VGI): OpenStreetMap polygon features overlapping each Google Earth image are filtered to 186 useful tag keys and summarised into captions by Vicuna-v1.5-13B (Sec. 2.1, Appendix 0.B). The model uses a CLIP ViT-L/14 encoder at 224x224, a vision perceiver with learnable queries over three encoder layers (64, 48 and 32 queries, more for shallower layers), and LLaMA2-7B with LoRA rank 128 (Sec. 3.1, 4.1). Task identifiers [CLS], [VQA] and [VG] mark task type. A three-stage curriculum moves from caption alignment (perceiver only) to multi-task instruction data (perceiver plus LoRA) to complex instruction and reasoning data (Sec. 3.2). Training used 8 V100 32GB GPUs (Appendix 0.G).

## Data and benchmarks
- LHRS-Align: about 1.15M image-caption pairs from 1 m Google Earth imagery over 9,259 cities in 129 countries, cut from a 4M pool by semantic balancing; images dominated by ocean or cloud were removed with a trained classifier (Appendix 0.B.1, 0.B.2).
- LHRS-Instruct: about 40k samples, namely 2.9k (RSITMD) and 25k (NWPU) caption-derived conversations plus GPT-4 generated 0.9k reasoning, 4k detailed description and 7k conversation samples with OSM-derived boxes (Sec. 2.2).
- Multi-task instruction set: 42,322 samples from public training splits (Table 8).
- LHRS-Bench: 690 hand-written single-choice questions (2 to 4 options) on 108 Google Earth images, 5 top-level and 11 fine-grained dimensions (Table 1). Each question is asked four times with shuffled options and counts as correct only if all four are right (Sec. 4.3).
- Test sets: seven classification datasets, RSVQA-LR and RSVQA-HR (count and area omitted), RSVG and DIOR-RSVG (Table 9).

## Key results
- Classification average 71.83% over AID, WHU-RS19, NWPU, SIRI-WHU, EuroSAT, METER-ML and fMoW, 27.51 points above the next open model (Table 2). AID 91.26, EuroSAT 51.40, fMoW 56.56.
- RSVQA-LR average 89.19, RSVQA-HR average 92.55 (Table 3). Table 3 also recomputes GeoChat as 91.81 on LR and 70.82 on HR, the plain means of GeoChat's sub-scores.
- Visual grounding acc@0.5: RSVG 73.45, DIOR-RSVG 88.10, average 80.78 (Table 4).
- LHRS-Bench average 39.38, against GPT-4-Turbo 44.56 and Claude-3-Opus 39.08 (Table 5). The text says it matches GPT-4V, but no GPT-4V row appears and GPT-4-Turbo is about 5 points higher.
- Ablation: LHRS-Align beats RS5M and SkyScript as the stage-1 data on most tasks (Table 6).

## Limitations
Authors state the usual LLM hallucination risk (Sec. 5) and that OSM data are scarce for cities in underdeveloped regions (Appendix 0.B.1). Some classification test sets (AID, WHU-RS19, SIRI-WHU) come from Google Earth like LHRS-Align, so overlap cannot be ruled out (Sec. 4.2 footnote). LHRS-Bench's imagery dimension covers only optical (multispectral and panchromatic) images, no SAR (Appendix 0.F). The model is high-resolution RGB only. Qualitative examples show the model verbally hedging when unsure (Sec. 4.4, Fig. 5), but there is no confidence score, calibration or abstention rule. A follow-up, LHRS-Bot-Nova (September 2024), upgrades the base model and data.

## What it means for EvidEO
- Adopt the VGI trick: auto-caption Sentinel-2 tiles over India using OSM plus Bhuvan or district boundary layers to build cheap LoRA training pairs.
- Check OSM density in target districts first; the authors themselves dropped cities with sparse OSM, which will bias captions toward cities.
- Use LHRS-Bench-style multiple-choice questions, including its four-shuffle consistency rule, for our own small evaluation set, since closed answers make calibration measurable.
- A 7B model is beyond our CPU budget; borrow the data and curriculum ideas, not the model.
- Look at LHRS-Bot-Nova before benchmarking, since it supersedes this version.

## Full-text check (2026-10-14)
Ingredients (LHRS-Bot's own system as built and evaluated):
- C1 calibrated per-answer confidence: No. No probability output or calibration analysis.
- C2 threshold abstention with next step: No. Fig. 5 shows the model saying it is uncertain in free text, but there is no stated threshold or suggested fix (Sec. 4.4).
- C3 scene receipts that reproduce: No. LHRS-Align stores resolution and city metadata per training pair (Sec. 2.1), but answers carry no scene IDs or dates; evaluation averages two runs with greedy decoding, which is an eval detail, not a receipt.
- C4 SAR chosen automatically under cloud: No. RGB only; cloud appears only as a training-image filter.
- C5 CPU or offline: No. LLaMA2-7B; no CPU or quantised inference reported.
- C6 plain-language questions for non-experts: part. Free-form conversation with real users is shown (Fig. 5), but benchmark use relies on task identifiers and templated prompts and no non-expert study exists.

Corrections to the abstract-level entry: classification average is 71.83 in v4, not 71.43; added the LHRS-Bench protocol and closed-model comparison (GPT-4-Turbo 44.56 is higher, contrary to the "matches GPT-4V" wording); added instruction-set breakdown, perceiver and LoRA details, hardware, and the authors' own OSM sparsity note.

Novelty impact: none. 0 Yes, 1 part.
