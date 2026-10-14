---
id: 176
title: "EO-Gym: A Multimodal, Interactive Environment for Earth Observation Agents"
authors: "Sai Ma, Zhuang Li, Sichao Li, Xinyue Xu, Ruibiao Zhu, Tony Boston, John A. Taylor"
year: 2026
venue: "arXiv preprint (arXiv:2605.01250, v1 2 May 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2605.01250
code: "https://huggingface.co/datasets/paperuploadacount/EO-Gym (dataset link given in the paper; not fetched); the paper says the dataset and EO-Gym-4B are open-sourced (Section 9)"
category: rs-benchmark
era: upcoming
tags: [eo-agents, tool-use, benchmark, gymnasium, sar-optical-switching, temporal-retrieval, lora, qwen3-vl-4b, pass-at-k, xbd, m4-sar]
read_depth: "full"
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2605.01250 (full text: Sections 3 to 8, Tables 2 to 7); WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2605.01250 converted to text (sections read: 1 to 9, Tables 1 to 9, Appendix A.1 to A.3 with Tables 10 and 11, B.1 to B.4 with Table 19, C.1 to C.3, D.1 to D.4)"
takeaway: "Executable EO agent benchmark (660k local files, 35 tools, 9,078 trajectories) where a LoRA-tuned Qwen3-VL-4B learns to fetch older scenes and switch between optical and SAR, reaching 0.74 Pass@3 (base 0.49) above Gemini-2.5-Pro at 0.67; validates EvidEO's small-model-plus-tools design but scores only answer correctness, with no confidence, abstention or cloud-triggered sensor choice"
---

# Ma et al. 2026, EO-Gym interactive environment for EO agents

## Problem
Most EO benchmarks hand the model one fixed image and one question. Real analysts reduce uncertainty by widening the area, pulling older scenes, or switching from optical to radar when clouds or night block the view. No controlled, training-scale benchmark tested that evidence-gathering loop for vision-language agents.

## Approach
- A Gymnasium-style local workspace over more than 660k files indexed by location, time and sensor, built from eight public datasets (xBD, xView, DIOR, FAIR1M, fMoW, DOTA, SARDet-100K, M4-SAR) plus Landsat 8/9 and Sentinel-2 retrieved from Google Earth Engine at FAIR1M locations (Appendix A.1, Table 10). M4-SAR supplies paired Sentinel-1 SAR and Sentinel-2 optical chips.
- 35 EO tools in three data-access paradigms: spatial planning (pan, zoom, crop), temporal fetching (earlier captures, Sentinel and Landsat listings) and cross-modal switching (for example get_optical_from_sar, Table 11). Tools return crops, JSON boxes, masked images and indices such as NDVI and NDWI. All retrieval is a local lookup, so runs do not depend on live cloud platforms (Section 3).
- Three evaluation axes (Appendix A.3): Verified versus Unverified tool outputs, Simple versus Detailed prompt, and task-relevant (Skill) versus full 35-tool (All) schema. Verified mode replaces optical detectors with human-checked ground truth plus a Qwen3-VL-2B target filter; SAR and cross-modal object tools have no detector backend and always run in Verified mode, even in the "Unverified" setting.
- Trajectory synthesis (Section 4, Appendix B.3 and B.4): GPT-4.1 generates MCQ items and tool trajectories (up to 50 calls), a two-layer reviewer (deterministic structural checks, then an LLM committee) rejects unsupported conclusions such as directional claims from tools without coordinates, gpt-oss-120b rewrites traces to ReAct form, MCQs are converted to open text, and a GPT-4.1 rewrite audit fixes resolution-mismatched questions (for example counting small vehicles in 30 m Landsat) by rewording the question or trajectory. About 62% of roughly 15k MCQ items yielded valid traces.
- Reference model EO-Gym-4B: LoRA (rank 16, alpha 32, all linear layers) on Qwen3-VL-4B-Instruct for three epochs via SWIFT, trained and evaluated on four NVIDIA H200 GPUs (Section 5, Appendix C.1).

## Data and benchmarks
EO-Gym-Data: 9,078 trajectories and 34,604 reasoning steps over six task families (temporal reasoning, disaster impact, geospatial reasoning, visual understanding, spatial navigation, object counting) and 18 question types. Test set 1,436 human-verified trajectories; training set 7,642 LLM-validated trajectories; split by source imagery and question type with hashed filenames. Ten function-calling VLMs evaluated (Qwen3-VL 4B/8B Instruct and Thinking, 32B Instruct, GPT-4.1-mini, GPT-4.1, GPT-5.1, Gemini-2.5-Flash and Pro), at most 15 calls per rollout. Answers judged by GPT-4.1-mini against ground truth; on 600 human-labelled outputs the judge reached 0.923 agreement and Cohen's kappa 0.846 (Section 5, Appendix C.3.3).

## Key results
- Main setting (Verified, Simple, Skill; Table 2): EO-Gym-4B reaches 0.65 Pass@1 and 0.74 Pass@3 versus 0.42 and 0.49 for its base; its Pass@3 interval [0.71, 0.76] sits above Gemini-2.5-Pro at 0.67 [0.65, 0.69]. Tool-any 0.760, illegal-call rate 0.003.
- Per task (Table 3, Pass@3): largest gains on temporal reasoning (0.69 vs 0.29) and disaster impact (0.68 vs 0.30). Closed models lead on perception-heavy tasks (Gemini-2.5-Pro 0.86 on spatial navigation, GPT-4.1-mini 0.80 on counting).
- Repeated sampling (Table 5): 0.80 Pass@10 and 0.67 self-consistency for EO-Gym-4B.
- Detailed prompt (Table 6): EO-Gym-4B best Pass@1 (0.60) but GPT-5.1 edges it on Pass@3 (0.70 vs 0.69).
- Unverified outputs with all tools (Table 7): EO-Gym-4B still leads at 0.69 Pass@3, but Tool-any drops for every model.
- GPT-5.1 had a low Tool-any rate (0.368, Table 2), consistent with answering without the reference tools; Qwen3-VL Thinking models made zero tool calls in 32 to 36% of cases (Table 4).
- Transfer (Table 8): training on optical-to-SAR switching and testing on the reverse direction gave +0.058 Pass@3 but a small Pass@1 drop (0.731 to 0.712).
- Renaming every tool at inference left scores essentially unchanged (Table 9).

## Limitations
- Imagery is mostly very-high-resolution object-centric optical data; Sentinel-1 enters only through M4-SAR object chips (bridges, harbours, oil tanks, wind turbines and similar), and flood extent is not a task family.
- Verified mode replaces detector noise with ground-truth-backed outputs, and SAR tools never run unverified, so headline numbers overstate end-to-end reliability, especially for radar.
- Correctness is judged by an LLM; no calibration, confidence or abstention metric. The Detailed prompt explicitly discourages early abstention, so declining is treated as failure.
- Authors' stated limits (Section 8): no strict test of transfer across the three data-access paradigms, a fixed predefined tool set, and fine-tuning only at 4B scale.

## What it means for EvidEO
- Adopt: independent evidence that a LoRA-tuned 4B VLM can learn when to fetch an older scene or switch modality, which is the routing EvidEO needs when Sentinel-2 is clouded. Reuse the Verified versus Unverified split in EvidEO's own eval to separate routing errors from instrument errors.
- Adopt: the resolution-mismatch audit (no counting cars at 30 m) is a cheap, concrete sensor-limits rule; in EO-Gym it is a dataset-cleaning step, but EvidEO's intent parser can encode it per instrument as a refusal rule at run time.
- Beat: EO-Gym rewards any correct final answer and penalises declining; EvidEO should add a selective-risk metric (accuracy at a given coverage) and credit correct abstentions, which this benchmark cannot express.

## Full-text check (2026-10-14)
Ingredient verdicts for EO-Gym's own system (environment plus EO-Gym-4B):
- C1 calibrated per-answer confidence: No. Only dataset-level bootstrap intervals on Pass@k (Section 5, Appendix C.3.1); no per-answer probability or calibration error anywhere.
- C2 threshold abstention with next step: No. No confidence threshold; the Detailed prompt tells the agent not to abstain after one failed detection (Appendix A.3.2). The 30 m counting fix is an offline dataset rewrite (Appendix B.4), not a run-time refusal.
- C3 scene receipts that reproduce: part. Local lookups and a fixed Qwen3-VL-2B filter make the environment deterministic, and model snapshots are listed (Section 3, Appendix A.3.1, C.2); but answers do not cite scene IDs and dates to the user, filenames are hashed, and no re-run identity test is reported.
- C4 SAR chosen automatically under cloud: part. The agent itself chooses cross-modal tools (Table 11, Table 8), but switching is driven by question type on paired M4-SAR chips, not by detecting cloud in the optical scene; cloud cover is never a trigger in any task.
- C5 CPU or offline: part. The data path is offline and the 4B model needs no hosted LLM at inference, but all inference ran on H200 GPUs and no CPU or edge run is reported (Section 5).
- C6 plain-language questions for non-experts: part. Questions are open natural-language text, but they are LLM-generated from dataset labels and aimed at analysts; no non-expert users or study.
Corrections to the earlier entry: Sentinel-1 is a named source (M4-SAR pairs Sentinel-1 with Sentinel-2, Table 10), so "Sentinel-1 is not a named data source" was wrong; the "Unverified" setting still runs SAR tools in Verified mode; the LLM committee checks support of conclusions by tool outputs, not ground truth; the sensor-limits rewrite is a data-cleaning step rather than a learned refusal; the Detailed prompt actively discourages abstention.
Novelty: EO-Gym delivers no full ingredient and at most partial C3 to C6. It does not threaten EvidEO's claim that no prior system combines more than two of C1 to C6, but it is the strongest prior evidence that a small VLM can learn modality and temporal switching, so EvidEO's C4 claim must specify the cloud-triggered, automatic part.
