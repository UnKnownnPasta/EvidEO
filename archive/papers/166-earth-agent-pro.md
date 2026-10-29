---
id: 166
title: "Earth-Agent-Pro: Towards Real-World Full-Chain Earth Observation with Agents"
authors: "Zhutao Lv, Chenhao Dang, Yi Feng, Yanpei Gong, Xiaolei Wang, Junyan Ye, Conghui He, Weijia Li"
year: 2026
venue: "arXiv preprint (arXiv:2609.12533, September 2026); no peer-reviewed venue yet"
link: https://arxiv.org/abs/2609.12533
code: "Not released (arXiv comment says code and datasets will be released soon)"
category: eo-agents
era: upcoming
tags: [tool-agents, plan-and-execute, expert-skills, structured-memory, data-acquisition, grpo, verifiable-rewards, qwen, earth-bench-pro]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2609.12533 (title, authors, date, comment, abstract); numbers from the abstract only; 2026-10-14 full-text read via curl of https://arxiv.org/html/2609.12533 (v1) converted to text (sections read: Abstract, I Introduction, II Related Work, III Earth-Bench-Pro incl. Table I and data curation, IV framework incl. skills, structured memory, execution and repair, V role-specialized training, VI Experiments incl. Tables II to X, VII Discussion incl. case studies, limitations and error analysis, VIII Conclusion; the paper has no appendix)"
read_depth: "full"
takeaway: "The strongest full-chain EO agent so far (acquires and prepares its own data, keeps provenance-tagged accepted evidence and answers only from it) moves toward EvidEO's design with six expert-authored skills, yet reaches only 66% LLM-judged accuracy with GPT-5 and 50% with a fine-tuned 9B model, parameter accuracy stays near 33%, and there is no user-facing confidence or abstention"
---

# Lv et al. 2026, Earth-Agent-Pro (full-chain EO agent)

## Problem
Earlier EO agents, including Earth-Agent (entry 094), start from data that is already supplied, and Earth-Bench gave expert-prepared local inputs with multiple-choice answers. Real questions require the agent to find observations, prepare them, compute, and conclude from what it actually measured (Sec I).

## Approach
- Plan-and-Execute framework (Sec IV). A Skill Router picks one of six expert-authored skills (spectral analysis, product computation, RGB perception), a Tool Router narrows the 112-tool catalogue, and the Planner composes a tool sequence through a four-role sequential debate checked by a catalogue validator.
- Workflow-centred structured memory (Sec IV-C): each accepted call is stored with tool, arguments, observation and provenance (for files: variables, time, region, bands, batches). Rejected attempts never enter this memory.
- Execution and repair (Sec IV-D): a hybrid gate (deterministic checks, then an LLM checker) accepts, retries or replaces each call; after repeated failure only the failed suffix of the workflow is replanned. An Answer Controller checks computations, coverage, units and non-finite values and answers only from accepted evidence; if evidence is incomplete it reopens a node.
- Role-specialised training (Sec V): LoRA adapters on a frozen backbone; Planner SFT on reference tool sequences, Executor GRPO with a rule-based reward comparing argument dictionaries (G = 4 samples). Training data: 2,480 trajectories instantiated from the 248 seed workflows by an LLM-written, human-reviewed program that swaps places, extents and dates, plus OpenEarthAgent training examples.

## Data and benchmarks
- Earth-Bench-Pro: 248 expert task cores posed as 744 questions in three regimes (instruction following, autonomous planning, open-world execution). The 248 open-world questions use 1,765 reference tool calls (7.1 per task, 84 distinct tools); 188 Product and Spectrum tasks require online acquisition and preprocessing from 323 expert-authored acquisition specifications (source, product, bands, extent, period, resolution, scaling); 60 RGB tasks keep user-provided images (Sec III-C).
- Eight domains, six continents, periods 1980 to 2025; the case studies use ASTER and MODIS acquisitions (Sec VII-A); task cores are inherited from Earth-Bench (entry 094). Eight annotators (two CS, three RS, three Earth science).
- Metrics: LLM-as-judge accuracy, ROUGE-L, embedding match, efficiency, TAO, TIO, TEM and parameter accuracy (Sec VI-A). Comparisons on TerraScope categories and against Codex and Manus use a 15% relative-error rule.
- All open-weight training and evaluation ran on eight NVIDIA H200 GPUs; closed models via APIs.

## Key results
- Backbones on Earth-Bench-OW (Table II): GPT-5 66.13% judge accuracy, Gemini-3.5-flash 63.31%, Claude-4.6-sonnet 56.85%; parameter accuracy only 27.28% (GPT-5) to 32.77% (fine-tuned 9B).
- Framework comparison with GPT-5 (Table VI): 66.13 vs ReAct 45.18, AFlow 40.16, OpenEarthAgent 41.53; TIO 71.97 vs 47.53. Embedding match is the one metric where it loses (13.31 vs up to 36.70).
- Fine-tuning Qwen3.5-9B: 38.31% to 50.00% judge accuracy, parameter accuracy +7.72 points; 4B: 32.26% to 43.15% (Table II, VIII). Tuned Planner beats GPT-5 on planning-only TAO, TIO, TEM (92.51 / 83.35 / 76.14, Table IX); with the reference plan fixed, GPT-5 still answers better (68.95 vs 52.82, Table X).
- Skills matter: for the fine-tuned 9B model, removing skills drops judge accuracy from 50.00% to 37.10% (Table VII); skills remove all logged tool-hallucination events in the 9B runs (Fig 8).
- TerraScope categories (Table III): 50.58% average vs 42.60% for TerraScope; distance measurement only 1.55%.
- OpenEarthAgent benchmark with GPT-5 (Table IV): answer accuracy 56.54 vs 45.38 best baseline.
- vs general agents (Table V): GPT-5 version 75.00% vs Codex 46.67% and Manus 43.33%, but Codex wins on Products (75% vs 55%).

## Limitations
- Accuracy is judged by an LLM, not by exact numeric checks; one in three answers is still wrong with the best backbone, and exact workflow match tops out at 71% and parameter accuracy at 33% (Sec VII-B).
- Training trajectories are instantiated from the same 248 seed workflows that define the test task cores (with places and dates swapped); the paper does not discuss this overlap.
- No calibrated confidence, abstention or user-visible provenance; the evidence memory serves the agent's own repair loop.
- Code and data not yet released; GPU-heavy, not CPU friendly. Skill guidance lengthens trajectories slightly (Sec VII-B).
- No SAR data or radar tools are mentioned.

## What it means for EvidEO
- **Convergent evidence**: the best-performing EO agent now constrains planning with expert-written skills, a move toward EvidEO's fixed instrument recipes; cite it as support, not competition.
- **Adopt** the "accepted evidence plus provenance" record: EvidEO's receipt already lists scenes and parameters; adding which step depends on which, and rejecting failed attempts from the record, makes partial re-runs and audits easier.
- **Adopt** the Answer Controller idea (answer only from accepted evidence, check units and coverage) as a pre-release gate before EvidEO's explainer runs.
- **Beat it** on reliability for a narrow scope: a fixed router plus calibrated instruments should exceed 66% on flood and crop questions and abstain on the rest; report exact-match accuracy, not LLM-as-judge.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. No probability per answer; the paper's phrase about producing a "calibrated numerical value" (Sec VII-B) means an exact measurement, not a confidence.
- C2 Threshold abstention with a next step: No. Incomplete evidence produces an internal diagnosis that reopens a workflow node (Sec IV-D), but the user is never told the system declines, and every task is answered.
- C3 Scene receipts that reproduce: part. Accepted evidence records carry provenance with time, region, bands and batches, and the benchmark reference trajectories were re-executed by experts (Sec III-C, IV-C), but answers do not cite scene IDs and no identical re-run of the agent is shown; LLM checkers and debate are stochastic.
- C4 SAR chosen automatically under cloud: No. The agent acquires data at runtime, but expert acquisition specifications fix source, product and bands (Sec III-C); no SAR and no cloud-driven sensor switch.
- C5 CPU or offline deployment: No. H200 GPUs for open models, hosted APIs for closed ones (Sec VI-A).
- C6 Plain-language questions for non-experts: part. Questions are self-contained natural-language requests with region and period (Sec III-C), and the introduction names non-EO users as motivation, but there is no non-expert evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- Earth-Bench (entry 094) is described here as multiple-choice over expert-prepared local inputs, which the Earth-Agent entry did not say.
- The toolset is 112 tools (84 used in references) and there are only six skills.
- Possible train-test overlap: training trajectories derive from the 248 test seed workflows.
- Parameter accuracy is the weak point (about 27 to 33%), not mentioned in the abstract-based entry.

Novelty implications: two parts (C3, C6), no full Yes. It does not threaten the "no more than two" claim, but its provenance-tagged accepted-evidence memory and answer-only-from-evidence controller mean EvidEO should claim receipts as user-facing and re-run tested, not as provenance tracking alone.
