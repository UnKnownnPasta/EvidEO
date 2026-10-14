---
id: 092
title: "ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks"
authors: "Akashah Shabbir, Muhammad Akhtar Munir, Akshay Dudhane, Muhammad Umer Sheikh, Muhammad Haris Khan, Paolo Fraccaro, Juan Bernabe Moreno, Fahad Shahbaz Khan, Salman Khan"
year: 2025
venue: "arXiv preprint (GitHub README lists CVPR 2026 MONTI workshop; not confirmed on a proceedings page, and the v3 HTML carries no venue header)"
link: https://arxiv.org/abs/2505.23752
code: https://github.com/mbzuai-oryx/ThinkGeo
category: eo-agents
era: recent
tags: [benchmark, tool-use, react, step-wise-evaluation, argument-accuracy, sar, flood, failure-analysis]
read_depth: "full"
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2505.23752, https://arxiv.org/html/2505.23752 (v3, April 2026) and https://raw.githubusercontent.com/mbzuai-oryx/ThinkGeo/main/README.md; 2026-10-14 full-text read via curl of https://arxiv.org/html/2505.23752 (v3, 2 April 2026) converted to text (sections read: 1 to 6, Tables 1 to 3, Supplementary S1 to S7 with Tables A1 to A4)"
takeaway: "RS tool-agent benchmark (486 tasks, 14 tools, MBZUAI and IBM) where even GPT-4o gets tool arguments right only about a third of the time (ArgAcc 34.75) and final answers right under 10% end to end; the strongest published case for EvidEO's fixed instruments and exact tool-call scoring"
---

# ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks

## Problem
General tool-use benchmarks (ToolBench, API-Bank, GAIA, GTA) do not test remote sensing, and earlier RS agents (Remote Sensing ChatGPT, RS-Agent) report mostly final-answer accuracy with no step-level attribution of where the agent went wrong.

## Approach
A benchmark of human-curated, tool-implicit queries grounded in real optical and SAR imagery, solved by an agent in a ReAct loop over 14 executable tools built on AgentLego plus two added tools (ChangeDetection, SegmentObjectPixels): perception (TextToBbox, object detection, counting, segmentation, change detection), logic (Calculator, Solver, Plot) and operation tools (DrawBox, AddText, GoogleSearch) (Section 4). Queries were built by annotators with a GPT-API-assisted script using image metadata (GSD, boxes), then checked by experts and scripts (Section 3.3); about 500 annotation hours by four people (S6). Two evaluation modes:
- Step-by-step, adopted from GTA: instruction following (InstAcc), tool selection (ToolAcc), argument correctness (ArgAcc) and summary quality (SummAcc), against expert annotated chains.
- End-to-end: per-category tool accuracy and final answer accuracy, judged by GPT-4o-mini against curated check questions because exact string matching misjudged paraphrases, plus an image-grounded variant (Ans_I).

## Data and benchmarks
- 486 tasks, 1,778 expert-verified reasoning steps; 436 optical RGB tasks (main evaluation) and 50 SAR tasks with 244 steps (Supplementary S1).
- Seven use cases: urban planning, disaster assessment and change analysis (148 tasks, the largest), environmental monitoring, transportation, aviation, recreational and industrial sites (Table A3); 281 easy and 155 hard optical tasks.
- Optical sources: DOTA, NWPU-VHR-10, UCAS-AOD, iSAID, AID, xBD, FloodNet (1.5 to 2 cm UAV imagery) and a global dumpsite dataset. SAR sources: SSDD (ships), SADD (aircraft) and SIVED (vehicles) (Table 2).

## Key results
- Table 3: GPT-4o ToolAcc 67.73, ArgAcc 34.75, end-to-end answer accuracy 9.78 (20.40 with image grounding). GPT-4-1106 ArgAcc 36.96, answer 5.16. Claude-Sonnet ArgAcc 0.00 and answer 8.97. Open 6B to 8B models answer 3.26 to 8.15.
- Format errors (Table A2): LLaMA3.1-8B and Qwen1.5-7B produce "Invalid JSON" in 82.36% and 92.52% of cases; Qwen1.5-7B, Qwen2.5-7B and Phi-3 often skip straight to a final answer (78.44%, 69.27%, 58.49%).
- Tool-call error rates for the best proprietary models are 44.46% (GPT-4o) and 30.86% (GPT-4-1106), which the authors still describe as relatively low (Section 5, Figure 6).
- Tool selection accuracy correlates most strongly with final answer accuracy (Figure 5).
- SAR subset (Table A1): final answer accuracy stays below 6% for every model.
- Runtime (Table A4): GPT-4o about 12 s per query end to end; open models 7 to 27 s.
- Related work it cites: UnivEARTH reports over 58% of generated Google Earth Engine code failing to run.

## Limitations
- Mostly high-resolution object-centric optical imagery; SAR is a small object-detection subset (ships, aircraft, vehicles) with no flood or Sentinel-1 content; flood content comes from FloodNet UAV imagery and xBD.
- LLM-as-judge for final answers adds its own error.
- No measurement of calibration or of an agent's ability to decline; every task is answerable.

## What it means for EvidEO
- Adopt the step-wise protocol directly: score EvidEO's router on tool selection and on exact argument match (AOI, dates, polarisation, threshold), separately from the final number. This is cheap because EvidEO's arguments are typed.
- Strong evidence for not letting the LLM choose free parameters: argument errors, not tool choice, are where frontier agents fail most.
- Gap EvidEO can fill: ThinkGeo never asks whether the agent knows when it is wrong. Add an abstention track (unanswerable or cloudy-scene questions) and report calibration error.

## Full-text check (2026-10-14)
ThinkGeo is a benchmark; it measures off-the-shelf LLM agents and implements no system of its own beyond the tool environment. Verdicts say what it implements or measures:
- C1 calibrated per-answer confidence: No. Not implemented or measured.
- C2 threshold abstention with next step: No. All tasks are answerable; declining is not scored.
- C3 scene receipts that reproduce: No. Answers are not tied to scene IDs; no repeat-run study.
- C4 SAR chosen automatically under cloud: No. SAR tasks are a separate subset with SAR given as input.
- C5 CPU or offline: No. Measures latency only (Table A4); top results come from hosted GPT-4 models.
- C6 plain-language questions for non-experts: part (measured). Queries are concise natural language without tool names (Section 3.1), written by annotators for analyst-style use cases; no non-expert study.
Corrections to the earlier entry: the SAR subset is ship, aircraft and vehicle detection from SSDD, SADD and SIVED, not flood; SAR answer accuracy is below 6%; exact error rates are 44.46% and 30.86%; the tool suite extends AgentLego; the venue is still unconfirmed in the paper itself.
Novelty: no ingredient delivered, so no threat to EvidEO's "no more than two" claim. It remains the best evidence that free argument choice is the weak point, which supports EvidEO's typed instruments.
