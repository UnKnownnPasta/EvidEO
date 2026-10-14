---
id: 164
title: "RSure-Agent: Reliable Use of Tool Observations for Remote Sensing Agents"
authors: "Fuyuan Liu, Nayu Liu, Wenhao Yu, Peijin Wang, Yingchao Feng, Fanglong Yao, Liang Wan, Wei Feng"
year: 2026
venue: "arXiv preprint (arXiv:2610.04836, October 2026); no peer-reviewed venue yet"
link: https://arxiv.org/abs/2610.04836
code: "https://github.com/airs101/RSure-Agent (demo per arXiv comment; code not yet released; not fetched)"
category: eo-agents
era: upcoming
tags: [tool-agents, verification, tool-observations, error-propagation, reliability-prior, process-evidence, reject-option, earthbench, thinkgeo]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2610.04836 (title, authors, date, comment, abstract); 2026-10-14 full-text read via curl of https://arxiv.org/html/2610.04836 (v1) converted to text (sections read: Abstract, I Introduction, II Related Work, III Empirical Analysis with Table I, IV Method incl. protocol, prior and online verification with Tables II and III, V Experiments incl. Tables IV to X, case study, efficiency and V-H Limitations, VI Conclusion, Appendices A to E incl. verifier and final-answer prompts and reliability matrices)"
read_depth: "full"
takeaway: "The closest prior art to EvidEO's 'trust the instrument only with evidence' idea: it shows tool outputs are wrong in 22.7 to 41.3% of tool-dependent tasks and adds accept, request-evidence or reject decisions backed by process evidence and a Laplace-smoothed per-task, per-tool success prior, but it serves the agent, runs on large hosted or open LLMs, and gives no calibrated per-answer confidence or scene receipt"
---

# Liu et al. 2026, RSure-Agent (verifying tool observations)

## Problem
EO agents trust what their tools return (a detection, an area, a class). Tools can run without error and still be wrong, and the agent then builds its answer on the wrong value.

## Approach
- Measures the problem on 1,229 execution trajectories from the native agents of three RS agent benchmarks (Sec III).
- A *verifiable observation protocol* (Sec IV-B, Table II): each perceive, measure or execute call returns a status code (ok, empty, unsupport, insufficient, fail), the observation, and process evidence: source evidence (backend weights, thresholds, sensor, resolution), intermediate results (boxes, confidence scores, numerator and denominator, valid-pixel counts) and validity evidence (valid-pixel masks, class coverage, paths to intermediate files). When data quality is insufficient the tool returns "insufficient" with a reason and no estimate.
- A *task-tool reliability prior* (Sec IV-C): GPT-4o runs a base ReAct agent once over a 1,200-task calibration set (OpenEarthAgent and CHOICE), giving 10,795 tool-call records; for each of 21 task types and each coarse or fine tool configuration, reliability is the Laplace-smoothed share of calls in tasks whose final answer was correct, kept only with at least 8 samples (Table III, Appendix E).
- Online verification (Sec IV-D): deterministic rule checks first (status, required fields, non-empty masks, no repeated calls), then an LLM verifier (same model as the backbone, separate context) sees the image, question, observation, evidence and prior and outputs accept, request_evidence (stating what is needed) or reject (with a reason). At most 3 follow-up calls per observation and 10 calls per task. Only accepted observations enter the history used for the final answer.

## Data and benchmarks
- ThinkGeo (436 test tasks, entry 092), EarthBench from Earth-Agent (248, entry 094), TerraLogic (545), and CHOICE-420 (420 multiple-choice VQA tasks over 21 CHOICE task types, 20 per type).
- Backbones: 11 models from Qwen3.5-27B to GPT-5.5, including Gemini and GPT APIs (Table IV).

## Key results
- Native agents (Table I): observation dependence 88.1 to 91.7%; observation error rate 22.7% (EarthBench), 41.3% (ThinkGeo), 39.8% (TerraLogic); error propagation 82.0 to 93.2%.
- Error propagation with GPT-5 (Table IX): EarthBench 95.5 to 69.6%, ThinkGeo 93.4 to 71.2%, TerraLogic 96.8 to 75.5% (drops of 25.9, 22.2 and 21.3 points).
- Ablation with GPT-5 (Table VI): verification alone adds 1.4 to 4.7 points per metric; the prior adds a further 1.1 to 3.1; full system vs base: ThinkGeo Ans 21.1 to 23.6, EarthBench 64.9 to 68.1, TerraLogic 26.4 to 31.4.
- CHOICE-420 (Table V): all 33 backbone-by-metric comparisons improve; average gains 5.71 (overall), 5.84 (perception), 5.45 (reasoning) points.
- Cost (Table VII, EarthBench): plus 17.56% LLM calls and 19.24% tokens over the base agent, but cheaper and more accurate than CRITIC or Tools Fail adaptations. Tool-call ratio 1.7891 vs 2.4146 for Earth-Agent with GPT-5, a 25.9% reduction (Table X).
- Of 569 tasks with a failed observation, 95.8% requested more evidence and only 52 observations were rejected outright (Table VIII); accepted-after-request tasks were still answered correctly only 47.3% of the time.

## Limitations
- Very new preprint; code not yet released.
- The reliability prior is a per-tool, per-task-type success rate from one GPT-4o run with task-level weak labels, not a calibrated probability for the specific answer, and is not shown to the user.
- Rejection and evidence requests are internal agent steps; benchmarks force a multiple-choice answer even when evidence is missing (Fig 3C case selects the nearest option).
- Error propagation stays at 69.6 to 75.5% after verification (Sec V-H); verification cannot fill data gaps that no tool can reach.
- Depends on tools that emit process evidence; the verifier is itself an LLM call.

## What it means for EvidEO
- **Strongest external support** for EvidEO's design: published numbers that tool errors silently propagate in RS agents, which is exactly what EvidEO's per-tile calibrated confidence and abstention guard against.
- **Adopt** the idea that each instrument returns process evidence (threshold value, histogram bimodality, valid-pixel share) and an explicit "insufficient, with reason" status, and that EvidEO keeps a per-instrument, per-question-type reliability table from its calibration sets.
- **Beat it** on the user side: EvidEO turns the accept or reject decision into a visible calibrated confidence and an abstain message on the card, with scene IDs and a receipt, for a non-GIS official, and runs without a hosted LLM.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. The prior (Sec IV-C, eq 6) is a smoothed per-task-type, per-tool success rate fed to the verifier; no per-answer probability and no calibration error is reported.
- C2 Threshold abstention with a next step: part. Tools return "insufficient" with a reason, the verifier's request_evidence states what is needed (Sec IV-D, Appendix B-B), and the final-answer prompt asks the model to name missing evidence when the format allows (Appendix B-C). But there is no stated confidence line, the "next step" goes to the agent rather than the user, and all evaluations force an answer.
- C3 Scene receipts that reproduce: part. Process evidence records sources, thresholds and sensor, tools save intermediate files for re-checking, and the Fig 3B case cites source dates and image counts (Sec IV-B, V-F). No scene IDs per answer and no re-run reproducibility test; the verifier is a stochastic LLM.
- C4 SAR chosen automatically under cloud: No. A SAR knowledge card exists in the retrieval library (Appendix C); no sensor selection.
- C5 CPU or offline deployment: No. Smallest backbone is a 27B open model; headline numbers use GPT-5 and GPT-5.5 APIs.
- C6 Plain-language questions for non-experts: part. Tasks are natural-language questions, but drawn from expert benchmarks with multiple-choice answer contracts; no non-expert evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- "At least 22.7%" understates two of three benchmarks: ThinkGeo and TerraLogic error rates are 41.3% and 39.8% (Table I).
- The "reject" outcome is rare in practice (52 rejected observations); most failures trigger evidence requests (Table VIII).
- The tool protocol already includes an "insufficient, with reason" status, which is closer to EvidEO's abstention than the abstract suggested.

Novelty implications: three parts (C2, C3, C6), no full Yes. It does not combine more than two of C1 to C6 as defined, so the claim holds, but it is the agent paper closest to EvidEO's evidence-first design and EvidEO should cite its process-evidence protocol explicitly and avoid claiming "instrument outputs with provenance" as new.
