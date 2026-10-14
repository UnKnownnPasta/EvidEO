---
id: 174
title: "GeoDisaster: Benchmarking Orchestrated Agents for Operational Disaster Geo-Intelligence"
authors: "Maram Hasan, Aman Verma, Savitra Roy, Hariseetharam Gunduboina, Daksh Jain, Muhammad Haris Khan, Subhasis Chaudhuri, Biplab Banerjee"
year: 2026
venue: "arXiv preprint (arXiv:2606.17246, v1 15 June 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.17246
code: "https://github.com/VIMAGE-IITB/GeoDisaster (linked in the HTML full text; not fetched)"
category: upcoming
era: upcoming
tags: [benchmark, eo-agents, disaster, sentinel-1, sar-flood, sen1floods11, tool-use, multi-agent, grpo, iit-bombay, executable-ground-truth]
read_depth: "full"
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2606.17246v1 (task table, metrics, main results text, conclusion, code link); WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2606.17246v1 converted to text (sections read: 1 to 6, Tables 1 to 9, Supplementary S1 to S3 with Tables S1 to S3, training setup and LLM-as-judge protocol)"
takeaway: "An Indian (IIT Bombay) 2026 benchmark of 2,921 instances whose answers come from executable geospatial workflows, including a 500-item Sentinel-1 SAR flood family, where a contract-driven Qwen2.5-7B multi-agent system reaches 90.11 answer accuracy; a ready external test for EvidEO, and its authors name uncertainty-aware reasoning as the open gap EvidEO targets"
---

# Hasan et al. 2026, GeoDisaster benchmark and RCEA agents

## Problem
RS VLMs interpret images and follow instructions, but operational disaster work needs tool-grounded spatial reasoning and structured, evidence-backed decisions. Earlier agent benchmarks use one monolithic agent, judge mostly the final outcome, and give sub-agents no checkable obligations.

## Approach
- Benchmark: 2,921 verified instances, 43 question types, five families (Table 2): deforestation monitoring (384; Sentinel-2, Sentinel-1 VV/VH, Hansen GFC), multi-hazard analysis (432; MODIS, VIIRS/FIRMS, Landsat, Sentinel-2/5P, Dynamic World, GHSL, WorldCover, CHIRPS, ERA5-Land, WorldPop, OSM), building damage (1,005; xBD), flood-safe routing (600; Sentinel-2, Copernicus EMS, OSM road graphs) and Sentinel-1 SAR flood monitoring (500; Sen1Floods11 chips, Sentinel-2 previews, JRC surface water).
- Ground truth comes from executable geospatial workflows and deterministic consistency checks, not LLM annotation (Section 3).
- Agent system (Section 4): an orchestrator plus geospatial-analysis, visual-reasoning and planning agents sharing 18 tools (Table S2: ReadData, MapFlood, DescribeFlood, CompareSources, PlanRoutes, RenderMap and others). Each orchestrator call to a specialist is a typed six-part execution contract (subgoal, context, output type, required evidence, schema, completion and failure conditions), so violations are checkable per step.
- RCEA alignment: failure-aware SFT (recovery actions kept only if they pass deterministic replay and match the reference artifact, S2.1) followed by GRPO with a per-step contract-satisfaction reward, an efficiency penalty and role-wise advantage normalisation. Default backbone Qwen2.5-7B-Instruct with LoRA (rank 32), trained on three RTX PRO 6000 Blackwell GPUs (S2.3). Training also mixes in OpenEarthAgent data.

## Data and benchmarks
Train/test split 2,629/292 (Table 3). Metrics: tool-sequence fidelity (ToolAnyOr, ToolSameO, ToolUni), task success (TSR), answer accuracy (Ans), generative quality, contract satisfaction (CSR), strict episode completion (ESR), plus step-wise instruction, tool, argument-name, argument-value and summary scores. GPT-5.5 scores them, computing trace metrics deterministically and semantic metrics by judgement; the judge prompt was tuned on 50 manually reviewed cases (S3.3). Baselines: GPT-5.5, GPT-5, GPT-4o, o4-mini and open 4B to 8B LLMs and VLMs; generalisation tested on OpenEarthAgent.

## Key results
- Open-source LLMs prompted alone nearly fail (answer accuracy 0.25 to 2.53, Table 4).
- GPT-5.5 has the best single-model answer accuracy (61.99) but ToolAnyOr only 20.93, so many correct answers do not come from valid tool chains.
- Multi-agent without alignment: 22.93 Ans; plus SFT: 82.43 Ans, ToolAnyOr 98.75; plus GRPO: 90.11 Ans and 94.24 TSR (Table 4).
- Backbones (Table 7): Qwen3-4B reaches 77.28 Ans after SFT plus GRPO (83.29 after SFT alone, Table 9), Mistral-7B 73.97, Llama-3.1-8B 67.41.
- On OpenEarthAgent (Table 5) the full system lifts answer accuracy from 45.26 to 85.16 over the OpenEarthAgent baseline.
- GRPO cuts latency per success from 57.64 s to 30.67 s (Table 9). Remaining errors are tied to ambiguous evidence, metric-selection mistakes (for example ranking by building count instead of footprint area, Figure S6) and constraint-aware synthesis (S2.2).

## Limitations
- All reported metrics pass through GPT-5.5 as judge, validated only on 50 cases.
- Test set is small (292 items across five families).
- No calibrated confidence or abstention is evaluated; the authors list uncertainty-aware reasoning over incomplete or inconsistent multi-source evidence as future work (S1.3, S2.2, Section 6).
- SAR flood items are Sen1Floods11 chips handed to the agent, not live scene retrieval; the stack was trained and run on large GPUs.

## What it means for EvidEO
- Adopt: run EvidEO on the SAR flood monitoring family (flood percentage, area, polygons, grid concentration, known-water separation) as an external, deterministic test; its executable answers fit EvidEO's receipts.
- Adopt: explicit execution contracts between parser and instruments, so each step's inputs and outputs are checked and logged.
- Beat: add what GeoDisaster lacks: a calibrated confidence per answer and a scored abstain option, measured with a risk and coverage curve rather than an LLM judge.
- Watch: same Indian research community (IIT Bombay VIMAGE lab, with an MBZUAI co-author); a potential collaborator or a close competitor if they add abstention.

## Full-text check (2026-10-14)
Ingredient verdicts for the paper's own multi-agent system:
- C1 calibrated per-answer confidence: No. No probability per answer and no calibration metric in Tables 4 to 9.
- C2 threshold abstention with next step: No. No abstain action or threshold; premature termination is scored as an error (TermErr, AbortErr, Table 8).
- C3 scene receipts that reproduce: part. Answers rest on artifact handles and path references (3.51 handles, 16.72 paths per case, Table 3) and SFT data is checked by deterministic tool and state replay (S2.1); but answers do not report scene IDs and dates to a user, and run-to-run identity of outputs is not tested.
- C4 SAR chosen automatically under cloud: No. SAR enters as given inputs in the SAR flood and deforestation families; the agent never chooses radar because optical is clouded.
- C5 CPU or offline: No. Open 7B backbone with no hosted LLM needed at inference, but everything runs on GPUs and evaluation depends on GPT-5.5; no CPU run.
- C6 plain-language questions for non-experts: part. Natural-language tasks (Table S1), but phrased for disaster analysts, with no non-expert evaluation.
Corrections to the earlier entry: the test split is only 292 items; the judge computes trace metrics deterministically and semantic ones by judgement rather than judging everything freely; training mixes in OpenEarthAgent data; Qwen3-4B results and the latency gains were not recorded before.
Novelty: at most partial C3 and C6, so no threat to EvidEO's "no more than two" claim. It strengthens the case that SAR flood questions with executable answers are an accepted evaluation setting, and its authors explicitly leave uncertainty-aware reasoning open.
