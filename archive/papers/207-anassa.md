---
id: 207
title: "ANASSA: An Agentic AI Orchestration Framework for Spatial Intelligence"
authors: "Constantinos Papantoniou, Brian Hilton"
year: 2026
venue: "arXiv preprint arXiv:2609.14824 (v1 13 September 2026); no venue stated; first author affiliated with Anassa.ai (a company of the same name), second author listed only as a research scientist in the USA"
link: https://arxiv.org/abs/2609.14824
code: "None; architecture specification only"
category: eo-agents
era: upcoming
tags: [agentic-gis, architecture-spec, provenance, uncertainty-states, human-in-the-loop, governance, authoritative-data, insufficient-evidence, no-evaluation]
read_depth: "full"
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2609.14824 (title, authors, date, abstract) and curl of https://arxiv.org/html/2609.14824v1 (affiliations, contributions, validation output states, conclusion, statement that empirical evaluation is deferred); 2026-10-14 full-text read via curl of https://arxiv.org/html/2609.14824v1 converted to text (sections read: 1 to 5 including 2.1 to 2.5, 3.1 to 3.3, Table 1 and figure captions; no appendix)"
takeaway: "A design-only specification for agentic GIS (eleven components, a six-step cognitive loop, typed contracts) that requires provenance records, uncertainty propagation and explicit outcome states such as validated-with-uncertainty and insufficient-evidence; no implementation or results, but it names EvidEO's trust features as requirements, so EvidEO's claim must rest on a working, measured system"
---

# Papantoniou and Hilton 2026, ANASSA

## Problem
Agentic GIS systems connect LLM reasoning to geospatial tools, but reasoning, execution, validation, governance and provenance are built as separate pieces. The authors argue this leaves no consistent way to make agent outputs traceable and accountable, and that current systems remain weak on quantitative spatial reasoning, execution robustness with real data, and evaluation (Section 1).

## Approach
- Extends the authors' earlier GeoBlockchain coordination model to AI agents (Section 1).
- Eleven components in four layers (Table 1): participants, sectors, deployment paths (enterprise, cloud, edge, SaaS, desktop, field, mobile), an orchestrator with a multi-model language gateway, the cognitive loop, multimodal spatial data, governance, an authoritative data foundation, output delivery, and downward and upward process flows.
- Six-step Geospatial AI Cognitive Loop (Section 2.2): sensing, reasoning, planning, decision with hallucination validation, execution, learning; human checkpoints at planning and validation, mandatory only for high-consequence workflows.
- Spatial validation contract at the decision step (Section 2.4): CRS compatibility, topology, positional accuracy, scale and resolution compatibility, temporal validity and staleness, uncertainty propagation, jurisdiction and source authority, and conflicting authoritative sources.
- Validation returns one of five states: validated, validated with uncertainty, conflicting authoritative evidence, insufficient evidence, or rejected, each carrying its evidence and checks.
- Typed inter-component contracts and typed failure states (for example tool unavailable, CRS mismatch, insufficient evidence), and a provenance record with data identifiers and versions, models and tools, parameters, intermediate outputs, validations and human interventions, so a decision path can be compared across repeated runs (Section 2.5).
- Eight design requirements DR1 to DR8 (Section 3.2). The authors explicitly do not claim novelty for orchestration, human approval, feedback loops or authoritative-data checks individually, only for their integration.

## Data and benchmarks
- None. Section 3.3 states there is no implemented reference system, benchmark comparison or performance result. It lists candidate metrics for future work: execution success, validation precision and recall, provenance completeness, escalation rate and run-to-run output agreement.

## Key results
- No quantitative results. Contributions are the architecture, the loop, contracts, requirements and four research questions.

## Limitations
- No implementation, no data, no measurements; all claims are design intentions.
- Company-affiliated position paper, not peer reviewed as of the verification date.
- Uncertainty handling is a requirement only; no calibration method, confidence measure or threshold is specified.
- Not specific to satellite imagery; EO is one data source among many, and the language gateway assumes large hosted models (GPT, Claude, Gemini are named as examples).

## What it means for EvidEO
- Adopt: the outcome states are a good vocabulary for EvidEO's answer card. Mapping EvidEO's outputs to answered, answered-with-low-confidence (below display threshold but above abstain), insufficient evidence (no usable scene), and conflicting evidence (optical and SAR disagree) would make abstentions more informative to a district official.
- Adopt: data staleness as an explicit check; EvidEO should state the age of the newest usable scene in every answer and abstain when it exceeds the question's window.
- Adopt: run-to-run output agreement as a reported metric for receipts.
- Novelty: weakens the claim only on paper. It shows that provenance, uncertainty and insufficient-evidence outcomes are already proposed as design goals for geospatial agents, so EvidEO should not present the idea of combining them as new. Because ANASSA has no implementation or evaluation, EvidEO's novelty shifts to being a working, measured system with calibrated confidence on real Sentinel scenes; EvidEO should cite it as a design-level precursor.

## Full-text check (2026-10-14)
ANASSA is an architecture specification; it implements and measures nothing. Verdicts say what it requires:
- C1 calibrated per-answer confidence: No. Requires uncertainty propagation and a validated-with-uncertainty state (Section 2.4, DR4) but no probability, fitting or calibration error.
- C2 threshold abstention with next step: required in part. Insufficient-evidence and rejected states plus typed failure states that drive replanning or escalation (Sections 2.4, 2.5), but no confidence threshold, and the next step is human escalation rather than advice to the user.
- C3 scene receipts that reproduce: required in part. Provenance record with data identifiers and versions and a proposed run-to-run agreement metric (Sections 2.5, 3.3); not built or tested.
- C4 SAR chosen automatically under cloud: No. No sensor-selection logic; remote sensing is one agent type among many.
- C5 CPU or offline: No. Edge and desktop appear as deployment paths, but the design assumes a multi-model language gateway and gives no offline or CPU path.
- C6 plain-language questions for non-experts: required in part. Natural-language intent from participants including communities (Table 1, Section 2), with no study.
Corrections to the earlier entry: none of substance; added the typed failure states, the provenance-record contents, the run-to-run agreement metric, the GeoBlockchain lineage, and the fact that human approval is risk-dependent rather than always required.
Novelty: as a paper design it touches C2, C3 and C6 partially but delivers none, so it is not a prior system combining more than two ingredients. Its existence means EvidEO must claim implementation and measurement, not the idea of combining trust features.
