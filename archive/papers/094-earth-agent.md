---
id: 094
title: "Earth-Agent: Unlocking the Full Landscape of Earth Observation with Agents"
authors: "Peilin Feng, Zhutao Lv, Junyan Ye, Xiaolei Wang, Xinjie Huo, Jinhua Yu, Wanghan Xu, Wenlong Zhang, et al."
year: 2025
venue: "ICLR 2026"
link: https://arxiv.org/abs/2509.23141
code: https://github.com/opendatalab/Earth-Agent
category: eo-agents
era: recent
tags: [mcp, tool-use, spectral, ndvi, ndwi, landsat, modis, benchmark, parameter-accuracy, tool-hallucination]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2509.23141 (comment: published at ICLR 2026), https://arxiv.org/html/2509.23141 and the ICLR 2026 virtual poster listing found by web search; 2026-10-14 full-text read via curl of https://arxiv.org/html/2509.23141 converted to text (sections read: Abstract, 1 Introduction, 2 Related Work, 3 framework, tool kit and evaluation protocol, 4 benchmark and annotation pipeline, 5 Experiments incl. Tables 1 to 3, 6 Conclusion, ethics and reproducibility statements, Appendix A dataset incl. Tables 4 to 6, quality control and no-tool ablation, B models and metric formulas, C modality breakdown Tables 8 to 10, D error analysis, E latency Table 11, F scalability Table 12, G tool kit list Tables 13 onward (skimmed for scope), H and I figure-only case studies (captions only))"
read_depth: "full"
takeaway: "Most capable EO tool agent of its time (104 MCP tools over local Landsat, MODIS, ASTER and GEE product files) and the closest competitor to EvidEO's instrument idea, yet GPT-5 matches the expert tool-and-argument prefix only about 26% of the time, tool-free LLMs already score about 37%, and there is no calibration, abstention or scene receipt"
---

# Earth-Agent: Unlocking the Full Landscape of Earth Observation with Agents

## Problem
Multimodal LLMs answer RGB perception questions but cannot do quantitative, multi-step Earth science (computing indices, retrieving geophysical parameters, analysing time series over many images). Earlier EO agents are RGB-only, shallow, and lack systematic evaluation; UnivEARTH (entry 204) generates GEE code rather than calling tools (Sec 1, 2).

## Approach
- A ReAct-style agent (formalised as a POMDP) that exposes 104 tools through the Model Context Protocol (MCP), grouped into five kits: Index (NDVI, NDWI, NBR, NDSI and others, batch versions), Inversion (LST by several methods, PWV, emissivity, passive-microwave soil moisture and similar), Perception (classification, detection, segmentation with SAM2-type models), Analysis (trend, seasonality, change point, spatial autocorrelation) and Statistics (preprocessing, Landsat QA cloud masking, batch statistics) (Sec 3, Appendix G).
- Tools operate on local GeoTIFF files supplied with each question; the agent passes file paths (Appendix G.1).
- Two regimes: Auto-Planning (the model plans freely) and Instruction-Following (the query includes step hints, about 150 characters longer).

## Data and benchmarks
- Earth-Bench: 248 expert-curated questions over 13,737 images (the main text says 13,729) in three modalities: Spectrum 100, Products 88, RGB 60 (Table 5). About 400 candidate questions were cut to 248 after senior review; questions with missing or anomalous data were discarded (Appendix A.5).
- Sources (Table 4): Landsat 8/9 (1,684 images), MODIS (10,273), ASTER (110); GEE products LST, NDVI, NDWI, GPM, VIIRS, GHSL, QA_PIXEL, fire MaxFRP; RGB sets AID, DIOR-RSVG, DOTA, NWPU-VHR-10, xBD.
- Annotation: 12 annotators (2 CS, 7 RS, 3 Earth science) wrote 71,664 lines of Python solutions; each solution's tool calls became the reference trajectory and its output the ground-truth answer (Sec 4.2, Appendix A.2).
- Dual-level evaluation (Appendix B.2). End-to-end: accuracy (exact match with the reference answer) and efficiency (predicted over reference call count). Step-by-step: Tool-Any-Order, Tool-In-Order, Tool-Exact-Match (longest common prefix) and Parameter Accuracy (tool and arguments both match, under the prefix rule).
- Earth-Bench-Lite (60 questions, 20 per modality) for comparing against general agents (GPT-Agent, MGX, Manus, Coze).

## Key results
- Auto-Planning answer accuracy (Table 1): GPT-5 65.99, Seed-1.6 52.48, Gemini-2.5-Flash 52.23, DeepSeek-V3.1 51.42, GPT-4o 43.72. Instruction hints lower GPT-5 to 62.35.
- Parameter Accuracy is far lower than answer accuracy: GPT-5 26.11, Gemini-2.5-Flash 17.26, best DeepSeek-V3.1 30.81 under Auto-Planning, so many correct answers come from trajectories whose arguments diverge from the expert's prefix.
- With all tools removed, mainstream LLMs answer about 37% correctly from the query and folder alone (Appendix A.6), which sets a high floor for judging tool benefit.
- By modality (Tables 8 to 10): GPT-5 61% Spectrum, 75% Products, 59% RGB; RGB errors often come from the expert perception models even when the right tool is called.
- Error taxonomy (Appendix D): not recognising when to stop, tool hallucination, file hallucination, invalid parameters, system errors. GPT-5 made the most errors, mainly invalid parameters and no tool hallucinations; for the open models about 60% of errors were hallucinations or missed termination. The authors suggest RL-trained open models are more exploratory.
- Accuracy peaks for tasks needing roughly 3 to 14 tool calls and falls for longer chains (Table 12).
- Earth-Bench-Lite (Table 2): Earth-Agent with GPT-5 55.83 average vs GPT-Agent 40.42, Manus 26.14, MGX 18.60, Coze 15.30; Earth-Agent took 158 min for the 60 questions, GPT-Agent about 300 min. Most latency is LLM calls, not tools (Table 11).
- Against RS MLLMs (Table 3): AID 93.42, DOTA detection 60.88 vs about 17 for MLLMs.

## Limitations
- Answers have no confidence, no abstention, and no stated provenance record for end users; tasks with missing data were removed, so every task is answerable.
- No SAR data in the benchmark (the toolkit has passive-microwave inversion functions but no radar inputs), which matters for monsoon cloud cover.
- Inputs are pre-downloaded local files; the agent does not search or acquire scenes (the follow-up, entry 166, adds this and describes Earth-Bench as multiple-choice).
- Low parameter accuracy means results can be right for the wrong reasons; reruns may not reproduce.

## What it means for EvidEO
- This is the work that most challenges EvidEO's novelty claim on instruments: it grounds numbers in real spectral tools (NDVI, NDWI, LST retrievals) rather than LLM guesses. EvidEO's claim should be narrowed to the combination Earth-Agent lacks: SAR-first flood instruments, calibrated confidence, abstention below threshold, and a re-runnable receipt with scene IDs.
- Adopt its four trajectory metrics, especially Parameter Accuracy, for EvidEO's router evaluation; with a small fixed instrument set EvidEO should aim far above 26%.
- Adopt the no-tool baseline (Appendix A.6): EvidEO's evaluation should report how often a bare LLM already gets the answer.
- Its failure taxonomy (tool, file and parameter hallucination, no stop condition) is a ready checklist of things EvidEO's typed router and schema validation must make impossible, and our evaluation should count each one.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. Only accuracy, efficiency and trajectory metrics (Appendix B.2).
- C2 Threshold abstention with a next step: No. The loop runs until a stop condition or step limit (Sec 3.1); no decline path; unanswerable tasks were filtered out (Appendix A.5).
- C3 Scene receipts that reproduce: part. The paper says the loop yields a reproducible tool-call trajectory (Sec 3.1) and promises released logs, but answers do not cite scene IDs or dates and no identical re-run is shown.
- C4 SAR chosen automatically under cloud: No. Inputs are supplied files; no sensor choice and no SAR data (Table 4). A Landsat QA cloud-mask tool exists, but it masks rather than switches sensor.
- C5 CPU or offline deployment: No. All 13 backbones are called through hosted APIs (Table 7). The tools themselves are local Python, but the answer path needs an LLM service.
- C6 Plain-language questions for non-experts: part. Natural-language queries, but written by experts around local file folders, averaging about 390 characters; no non-expert evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- "Gemini-2.5" is Gemini-2.5-Flash (Table 7).
- The best Auto-Planning parameter accuracy is DeepSeek-V3.1 (30.81), not GPT-5.
- Image count is 13,737 in Table 4 against 13,729 in the main text.
- The earlier entry missed the no-tool baseline of about 37% and the fact that inputs are pre-staged local files.

Novelty implications: two parts (C3, C6), no full Yes. It does not threaten the "no more than two" claim; its strength is the instrument library, which EvidEO should cite rather than claim.
