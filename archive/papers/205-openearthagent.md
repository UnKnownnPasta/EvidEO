---
id: 205
title: "OpenEarthAgent: A Unified Framework for Tool-Augmented Geospatial Agents"
authors: "Akashah Shabbir, Muhammad Umer Sheikh, Muhammad Akhtar Munir, Hiyam Debary, Mustansar Fiaz, Muhammad Zaigham Zaheer, Paolo Fraccaro, Fahad Shahbaz Khan, Muhammad Haris Khan, Xiao Xiang Zhu, Salman Khan"
year: 2026
venue: "ECCV 2026 (per arXiv comment); arXiv:2602.17665 (v1 February 2026, v4 July 2026)"
link: https://arxiv.org/abs/2602.17665
code: "https://github.com/mbzuai-oryx/OpenEarthAgent (stated in the paper as code, data and models; repository not inspected)"
category: eo-agents
era: recent
tags: [tool-registry, deterministic-replay, trajectory-sft, qwen3-4b, ndvi, nbr, ndbi, google-earth-engine, gis-tools, sar, agent-benchmark]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2602.17665 (title, authors, dates, ECCV 2026 comment, abstract) and curl of https://arxiv.org/html/2602.17665v4 (tool categories, replay validation, data sources, Tables 3, 4 and 6 numbers, conclusion, tool memory footprint); WebFetch of arxiv.org was rate limited; 2026-10-14 full-text read via curl of https://arxiv.org/html/2602.17665v4 converted to text (sections read: Abstract, 1 Introduction, 2 Related Work, 3.1 Dataset Curation with Tables 1 and 2, 3.2 Methodology, 4 Experiments incl. Tables 3 to 6, 5 Conclusion, Supplementary S1 ablations Tables A1 to A5, S2 model selection Table A6, S3 error analysis, S4 domain breakdown, S5 qualitative cases, S6 tool list Table A7 and implementations, S7 judge prompt and open-judge check, S8 curation components)"
read_depth: "full"
takeaway: "A 4B agent (Qwen3-4B fine-tuned on 14.5k replay-validated tool trajectories) that runs NDVI/NBR/NDBI change via Google Earth Engine, GIS and detection tools through one executable schema; end-to-end answer accuracy 45.26 vs 13.72 for its base model and 39.22 for GPT-4o; its cached, replayable tool traces are close to EvidEO's receipts, but there is no confidence, abstention or scene-level provenance"
---

# Shabbir et al. 2026, OpenEarthAgent

## Problem
EO agents (ThinkGeo, entry 92; Earth-Agent, entry 94) plan tool chains but mis-order calls, pass wrong arguments and give outputs that cannot be verified. The authors want a trainable agent whose every step executes and can be replayed (Sec 1, 2).

## Approach
- A unified tool registry with one JSON callable schema (Sec 3.2, Table A7): perception tools (TextToBbox, ObjectDetection with LAE-DINO, counting, pixel segmentation, ChangeDetection with TEOChat, region description and image captions with Qwen3-VL-7B), GIS tools (GetAreaBoundary by place name or box, AddPoisLayer from OpenStreetMap, ComputeDistance with OSMnx and NetworkX), spectral tools (AddIndexLayer, ComputeIndexChange, ShowIndexLayer for NDVI, NBR, NDBI, computed through Google Earth Engine and geemap for an area and year), georeferenced raster tools and utilities (calculator, sympy solver, plot, OCR, GoogleSearch).
- A tool execution cache stores intermediate layers so a trajectory can be deterministically replayed.
- Every training trajectory is re-executed before use to check argument format, coordinates, geometry and full-chain executability; test samples also get manual inspection (Sec 3.1, S8).
- Supervised fine-tuning of Qwen3-4B-Instruct-2507 on the validated trajectories (four A100 40 GB GPUs, one epoch, Unsloth); tool observations are masked from the loss (Sec 3.2, 4).

## Data and benchmarks
- 14,538 training and 1,169 evaluation instances; 100,656 training steps (6.92 per query) and 7,064 test steps (Sec 3.1).
- Sources (Table 2): optical DOTA, DIOR, NWPU-VHR-10, UCAS-AOD, AID, iSAID, xBD, FloodNet, Global-Dumpsite; SAR SSDD, SADD, SIVED (ship, aircraft and vehicle detection); OpenStreetMap POIs; Google Earth Engine index layers at 10 to 30 m. Index samples are mined from temporal changes such as vegetation loss, burn severity or flooding (S8).
- Queries and trajectories are synthesised by an LLM pipeline from templates and one-shot exemplars, then validated by execution (Sec 3.1, S8).
- Two protocols: step-by-step (no execution) and end-to-end with live tool calls. Non-generation answers are scored by gpt-4o-mini with plus or minus 10% numeric tolerance, IoU thresholds for spatial outputs, and zero for missing or fabricated outputs (S7); swapping in Qwen3-30B as judge raises scores slightly but keeps the ranking.

## Key results
- Step-by-step (Table 3): instruction, tool, argument-name and argument-value accuracy 99.51 / 97.18 / 96.08 / 62.10, the best in the table; frontier models score higher on final summary accuracy (o4-mini 89.48, gpt-5 87.02 vs 83.64).
- End-to-end (Table 4): answer accuracy 45.26 vs 13.72 for the Qwen3-4B base, 39.22 for GPT-4o and 43.88 for GPT-5; tool-order accuracy about 67 to 72%; GIS tool F1 98.52.
- In-context learning with 15 examples lifts the base model only to 33.06 answer accuracy (Table A2); a minimal tool schema drops OpenEarthAgent to 8.44 (Table A3), so the gains depend heavily on full JSON tool examples.
- Earth-Agent benchmark, step-by-step (Table 5): argument-value accuracy 44.44 vs 48.11 for GPT-4o, so it trails GPT-4o there. ThinkGeo answer accuracy 16.35 vs 9.78 reported (Table 6 left).
- On a 60-query subset of the Earth-Agent benchmark vs a general GPT agent: 60.04 vs 21.75 overall (spectrum 90.46 vs 14.67), about 22 s per query vs about 934 s (Table 6 right).
- Index tasks about 79% for OpenEarthAgent, gpt-4o and gpt-5 alike; GIS tasks 55.77% (Fig 7 text).
- Full tool stack needs about 45 GB of runtime memory during evaluation (S6).

## Limitations
- Still under half of end-to-end answers correct on its own benchmark.
- Training data and questions are synthesised by an LLM pipeline from existing datasets. Index tools do fetch Google Earth Engine layers by area and year, but answers do not name scenes or acquisition dates.
- No confidence, calibration or abstention; the judge scores fabricated or missing outputs as zero but the agent never declines.
- Deterministic replay checks that a trajectory runs, not that its answer is right (a point also made by the survey in entry 209), and the paper reports no re-run test of final answers.
- Answer accuracy is LLM-judged with 10% tolerance, not exact numeric match.
- The 45 GB tool stack, Qwen3-VL-7B and TEOChat tools, and Google Earth Engine and GoogleSearch calls make CPU-only or offline deployment unlikely without trimming.

## What it means for EvidEO
- Adopt: the single executable tool schema plus a cache of intermediate layers is a good pattern for EvidEO's receipt: store the STAC item IDs, the threshold, the mask hash and the computed numbers so the answer replays exactly.
- Adopt: validate each answer path by re-execution in CI, as they do for training data.
- Beat: EvidEO's fixed instrument chain avoids the tool-ordering errors that dominate their failure analysis, and adds calibrated confidence and abstention, which they lack.
- Novelty: weakens the claim a little. Replayable, tool-grounded NDVI and index-change answers from a small open agent (ECCV 2026) mean "re-runnable receipt" and "index-change instruments" are not new alone. It has no calibrated confidence, abstention, scene-level provenance, SAR fallback or non-expert Indian delivery, so the combination claim stands.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. Object detection returns per-box scores (Table A7), but no per-answer probability or calibration error.
- C2 Threshold abstention with a next step: No. A Terminate tool returns the final answer; there is no decline path (Table A7, S3).
- C3 Scene receipts that reproduce: part. The cache and JSON trajectories make tool chains replayable (Sec 3.2) and file references and spatial metadata are stored (S8), but answers do not list scene IDs or dates and replay is used to validate training data, not to show identical answers on re-run.
- C4 SAR chosen automatically under cloud: No. SAR images are an input modality supplied with the query (Table 2, Fig 5); the agent does not choose sensors or react to cloud.
- C5 CPU or offline deployment: No. 4B controller, but about 45 GB of tool memory, GPU training, and online GEE and GoogleSearch tools (S6).
- C6 Plain-language questions for non-experts: part. Natural-language queries, but LLM-synthesised from templates; no non-expert evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- "Image chips rather than live scene search by date and place" was too strong: GetAreaBoundary takes a place name and AddIndexLayer pulls GEE index layers for an area and year (Table A7). What is missing is scene-level provenance, not live retrieval.
- SAR data are part of the corpus (SSDD, SADD, SIVED), which the entry did not state.
- The 60-query general-agent comparison uses a subset of the Earth-Agent benchmark, not OpenEarthAgent's own test set (Table 6 right).

Novelty implications: two parts (C3, C6), no full Yes. It does not threaten the "no more than two" claim, but it is the closest prior work on replayable tool traces and EvidEO's receipt claim must rest on scene IDs plus a demonstrated identical re-run.
