---
id: 193
title: "Agentic AI for Remote Sensing: Technical Challenges and Research Directions"
authors: "Muhammad Akhtar Munir, Muhammad Umer Sheikh, Akashah Shabbir, Muhammad Haris Khan, Fahad Khan, Xiao Xiang Zhu, Begüm Demir, Salman Khan"
year: 2026
venue: "arXiv preprint, position paper (arXiv:2604.24919, v1 27 April 2026, v3 1 June 2026); no peer-reviewed venue listed"
link: https://arxiv.org/abs/2604.24919
code: "Not applicable (position paper)"
category: rs-vlm
era: upcoming
tags: [agents, position-paper, geospatial-state, provenance, verifier, uncertainty, failure-modes, flood-area, tool-use, evaluation]
read_depth: "full"
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, comment 'Position Paper') and curl to https://arxiv.org/html/2604.24919v3 (state definition, verifier checks, flood-area example, calibration discussion); WebFetch permission request timed out; the paper has no experiments, so no numbers are reported; 2026-10-14 full-text read via curl of https://arxiv.org/html/2604.24919v3 converted to text (sections read: 1 to 7 including the formal EO agent environment, 5.1 to 5.6, 6.1 to 6.4 and all figure captions; no appendix; the HTML author block renders only the first author, the full author list is from the arXiv API)"
takeaway: "A 2026 MBZUAI-led position paper arguing that EO agents must carry CRS, resolution, extent, time window, modality, an uncertainty descriptor and provenance in their state, check every step with geometric, temporal, physical, provenance and statistical verifiers, and keep execution records; it describes EvidEO's design goals but builds and tests nothing, so it is citable support rather than prior art"
---

# Munir et al. 2026, Agentic AI for remote sensing (position paper)

## Problem
Generic tool-using agents assume tools are independent, actions reversible, correctness visible near the step that caused an error, and internal evaluation sufficient. EO workflows are stateful: reprojection, resampling, compositing and aggregation change the data, so a wrong step can pass silently and give a plausible but invalid final answer (Sections 1.2, 2.2).

## Approach
- Lists the implicit assumptions of generic agent designs (planner-executor-verifier, SFT on trajectories, RL with internal rewards, self-evolving agents) and shows where each breaks for EO (Section 2, Figure 3).
- Describes what makes EO distinct: scale and resolution choice, context-defined objects (floods, burned areas), physics-driven modalities (SAR versus optical), irregular time series interrupted by cloud, and physical validity (Section 3).
- Catalogues failure modes (Section 4, Figure 5) and states when agents should not be used: fixed operations such as radiometric calibration, reprojection, index computation and tiling should be reliable operators, with agency only at the orchestration level (Section 4.5).
- Formal EO agent environment (Section 5): state holds data, CRS, GSD, extent, time window, modality, a reliability or uncertainty descriptor, provenance and tool history; actions are parameterised tool calls; hard feasibility predicates block inadmissible calls; orchestration is posed as constrained optimisation with geospatial-quality, physical-validity, cost and irreversibility terms.
- Learned tools (Section 5.4): proposes attaching a learned reliability score in [0, 1] to each learned-tool output, conditioned on the state and on the train-to-deployment shift, feeding the uncertainty descriptor; suggests regional recalibration or threshold re-estimation under shift.
- Verifier taxonomy (Section 5.6): geometric, temporal, radiometric or physical, provenance (source data, tool versions, parameter logs) and statistical checks (uncertainty calibration, low-confidence warnings, shift alarms).
- Research directions (Section 6): benchmark design rules, SFT plus RL, self-improvement accepted only above a verifier threshold with a per-step execution record of tool, parameters, data sources and before and after states, and trajectory metrics (pipeline integrity, trajectory validity score, discounted inconsistency burden, cost-aware efficiency).

## Data and benchmarks
None; it is a conceptual paper. It recommends trajectory-level evaluation with spatial and temporal leakage control rather than final-answer accuracy.

## Key results
- Figure 2 contrasts a generic agent trace and an EO-native trace for flood-area estimation from pre and post imagery: the generic one reaches a plausible but invalid area through window, transformation-order, CRS and unit errors. Figure 6 shows a second worked trace (ground area lost to destroyed buildings via change detection and GSD conversion).
- Argues that correct orchestration cannot fix a learned model that is miscalibrated or outside its training distribution (Section 5.4).
- Names cross-modal corroboration, such as SAR confirming optical measurements under cloud, as a probabilistic check (Section 6.3).

## Limitations
- No implementation, benchmark or measured gains; every formula is a design pattern the authors say is not a prescribed implementation.
- The reliability score is specified only as a learned function; no fitting data, calibration method or calibration metric is given, and there is no rule for when an agent should refuse or what it should tell the user.
- Several figures were drawn with ChatGPT help, per the captions.

## What it means for EvidEO
- Adopt: use its state schema as a checklist for EvidEO's answer record (CRS, pixel spacing, extent, time window, sensor, provenance, uncertainty) and its verifier list as unit tests on every pipeline step.
- Adopt: its point that fixed steps should not be left to an LLM backs EvidEO's choice to keep the VLM to intent parsing and explanation.
- Adopt: its execution record (tool, parameters, data sources, before and after state) is close to EvidEO's receipt; cite it when describing receipts.
- Novelty check: this is the closest statement of EvidEO's philosophy found so far, including a flood-area example, but it is a position paper with no system, calibration method or abstention rule; EvidEO can cite it as motivation and claim the working, calibrated, abstaining implementation.

## Full-text check (2026-10-14)
This is a position paper; it implements and measures nothing. Verdicts say what it requires or proposes:
- C1 calibrated per-answer confidence: required in part. Proposes a learned per-tool-output reliability score and lists "uncertainty calibration" as a statistical verifier (Sections 5.4, 5.6), but per intermediate product, not per user-facing answer, and with no calibration error defined.
- C2 threshold abstention with next step: No. Mentions low-confidence warnings and verifier thresholds for accepting training trajectories (Section 6.3), but no answer-level abstention and no next-step advice.
- C3 scene receipts that reproduce: required in part. Provenance in state, provenance verifiers and a per-step execution record including data sources (Sections 5.6, 6.3); repeated-run identity is not discussed.
- C4 SAR chosen automatically under cloud: required in part. Says the planner should select sensing modalities and mentions SAR corroborating optical under cloud (Sections 3.3, 5.6, 6.3), without a mechanism.
- C5 CPU or offline: No. Cost and latency appear only as budget terms; nothing on CPU or offline deployment.
- C6 plain-language questions for non-experts: No. Agents are framed as decision-support instruments for analysts (Section 7).
Corrections to the earlier entry: it does propose a form for the uncertainty descriptor (a learned, shift-aware reliability score), so "does not specify how the uncertainty descriptor should be computed" was too strong; the fair statement is that it gives no fitting or calibration procedure. It also contains an explicit per-step execution record and a SAR-under-cloud corroboration remark not noted before.
Novelty: as a requirements document it touches C1, C3 and C4 partially, but builds none of them, so it does not count as a prior system combining more than two ingredients. EvidEO should cite it as the design-level statement it implements, and avoid claiming that the idea of state-carried provenance and uncertainty is new.
