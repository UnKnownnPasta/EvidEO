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
verified: "2026-10-29 full text of arXiv PDF; earlier 2026-10-04 via arXiv and GitHub"
takeaway: "Copy the OpenStreetMap/VGI auto-captioning trick for cheap Indian training pairs and multiple-choice evals; check rural OSM sparsity"
---

# LHRS-Bot: Empowering Remote Sensing with VGI-Enhanced Large Multimodal Language Model

## Problem
Remote sensing MLLMs are starved of large, well-aligned image-text data, and there was no thorough benchmark to test their RS understanding across many skills.

## Approach
LHRS-Bot uses volunteered geographic information (VGI) to generate captions at scale: OpenStreetMap features overlapping each image are turned into text. The model (LLaMA2-7B-Chat language model) is trained with a multi-level vision-language alignment strategy and a curriculum that moves from simple alignment to harder instruction and reasoning data.

## Data and benchmarks
Three resources are introduced. LHRS-Align has about 1.15M image-caption pairs from 1 m Google Earth imagery over 9,259 cities in 129 countries, captioned using OpenStreetMap. LHRS-Instruct (roughly 40k samples) mixes reformatted RSITMD and NWPU data with visual reasoning, detailed description and conversation samples. LHRS-Bench has 690 single-choice questions on 108 images, across 5 top-level and 11 fine-grained dimensions.

## Key results
From the PDF: 71.43% average classification accuracy over seven datasets, 89.19% on RSVQA-LR and 92.55% on RSVQA-HR, about 80.78% average visual grounding accuracy on RSVG and DIOR-RSVG, and 39.38% overall on LHRS-Bench, ahead of the open-source models compared.

## Limitations
The LHRS-Bench score shows that fine-grained RS reasoning remains hard even for the best model tested. OSM-derived captions inherit OSM coverage gaps, which are larger in rural regions. Imagery is high-resolution optical only, with no SAR input, and no calibration or abstention (a qualitative figure says it can express uncertainty). A follow-up, LHRS-Bot-Nova (September 2024), upgrades the base model and data.

## What it means for EvidEO
- Adopt the VGI trick: auto-caption Sentinel-2 tiles over India using OSM plus Bhuvan or district boundary layers to build cheap LoRA training pairs.
- Check OSM density in target districts first; sparse rural tagging will bias captions toward cities.
- Use LHRS-Bench-style multiple-choice questions for our own small evaluation set, since closed answers make calibration measurable.
- A 7B model is beyond our CPU budget; borrow the data and curriculum ideas, not the model.
- Look at LHRS-Bot-Nova before benchmarking, since it supersedes this version.

## Full-text check (2026-10-29)
Read the full arXiv PDF text; the LHRS-Bench table was checked on the rendered page because the text layout interleaved its rows.
- Confirmed: RSVQA-LR average 89.19, RSVQA-HR 92.55, grounding average 80.78, LHRS-Bench average 39.38. Area and count questions are left out of the VQA tables.
- LHRS-Bench (Table 5): GPT-4-Turbo 44.56 and Claude-3-Opus 39.08, so LHRS-Bot is level with Claude and about 5 points below GPT-4-Turbo, although the text says it "matches GPT-4V". Its weakest dimensions are Quantity 18.25 and Area 25.33. Scoring is strict: an answer counts as wrong if any of four shuffled attempts is wrong.
- GeoChat is shown at 91.81 on LR here, against 90.70 printed in its own paper.
- LHRS-Bench names multispectral and panchromatic images; SAR is stated as not included. The conclusion admits susceptibility to hallucination.
