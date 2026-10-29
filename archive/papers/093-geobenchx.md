---
id: 093
title: "GeoBenchX: Benchmarking LLMs in Agent Solving Multistep Geospatial Tasks"
authors: "Varvara Krechetova, Denis Kochedykov"
year: 2025
venue: "1st ACM SIGSPATIAL International Workshop on Generative and Agentic AI for Multi-Modality Space-Time Intelligence (GeoGenAgent 2025), DOI 10.1145/3764915.3770721"
link: https://arxiv.org/abs/2503.18129
code: https://github.com/Solirinai/GeoBenchX
category: eo-agents
era: recent
tags: [benchmark, tool-calling, unsolvable-tasks, rejection, llm-as-judge, gis, abstention]
read_depth: "full"
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2503.18129 and https://arxiv.org/html/2503.18129 (v2, October 2025, workshop header on the paper); 2026-10-14 full-text read via curl of https://arxiv.org/html/2503.18129 (v2, 22 October 2025) converted to text (sections read: 1 to 8, Tables 1 to 8, Appendix A prompts, Appendix B tool list)"
takeaway: "Only geo-agent benchmark here that scores refusal on deliberately unsolvable tasks (79 of 202); models trade answering for refusing (o4-mini rejects 90% correctly but solves 51%, Claude Sonnet 4 solves 55% but rejects 17%), which supports EvidEO's explicit, model-independent abstention and gives a test design to copy"
---

# GeoBenchX: Benchmarking LLMs in Agent Solving Multistep Geospatial Tasks

## Problem
GIS practitioners (the authors are at the World Bank and JP Morgan Chase) want to know which LLM to put behind a tool-calling geospatial assistant, and whether it will admit when a task cannot be done with the tools and data it has instead of producing a plausible but wrong answer.

## Approach
- A deliberately simple LangGraph ReAct agent, temperature 0, up to 25 tool iterations, no human in the loop, so that the benchmark measures the LLM rather than an agent architecture (Section 3.1).
- 23 geospatial functions (loading tabular, vector and raster data, joins, filters, buffers, raster overlap, choropleths, heatmaps, contours) plus a reject_task tool that just returns "unsolvable" (Section 3.2, Appendix B).
- The rules prompt tells the agent to reject geospatial tasks the data or tools cannot solve, to treat partial geographic coverage as unavailable data, to pick the latest year with at least 70% coverage, and not to ask the user questions (Appendix A). The system prompt asks the agent to name the datasets it used.
- Dataset snapshots are stored locally to avoid API drift, and each conversation with maps is saved as HTML (Section 3.2).
- Tasks: seeds from practitioners and publications, expanded with Claude 3.5 Sonnet and manually filtered; reference solutions drafted by GPT-4o or Claude 3.5 Sonnet and rewritten by hand, sometimes with several valid solutions (Sections 4.2, 4.3).
- Evaluation compares the agent's tool-call sequence with reference solutions using a panel of LLM judges (GPT-4.1, Claude Sonnet 3.5, Gemini 2.5 Pro Preview), scoring match, partial match or no match; judges chosen from nine candidates on 50 manually scored tasks, matching human scores 96%, 94% and 88% (Section 5).

## Data and benchmarks
- 202 tasks: 123 solvable and 79 unsolvable, across four groups: merge-visualise (36), process-merge-visualise (56), spatial operations (53), heatmaps and contour lines (54) (Section 4.1, Table 1).
- Data: 18 statistical CSV panels, 21 vector datasets and 11 rasters (snow cover, flood extents, population) (Section 3.3).
- Eight commercial models reported: Claude Sonnet 3.5 and 4, Claude Haiku 3.5, Gemini 2.0 Flash, Gemini 2.5 Pro Preview, GPT-4o, GPT-4.1, o4-mini; o3-mini was run but excluded after giving empty solutions on 103 tasks (Section 6.1).
- Benchmark set, evaluator and task generation pipeline are open source.

## Key results
- Solvable tasks (Table 2): best match rates are 0.55 (Claude Sonnet 4) and 0.51 (o4-mini); most models are below 0.5, and 0.16 to 0.22 of solutions are partial matches for several models.
- Unsolvable tasks (Table 1): correct rejection ranges from 0.17 (Claude Sonnet 4) and 0.22 (Claude Haiku 3.5) to 0.62 (GPT-4o) and 0.90 (o4-mini).
- Clear trade-off: Claude Sonnet 4 solves more than three times as often as it correctly rejects; GPT-4o and o4-mini reject better than they solve; Claude Sonnet 3.5, Gemini 2.0 Flash and GPT-4.1 are balanced (Section 6.2).
- o4-mini best overall and Claude Sonnet 3.5 second (Table 7); o4-mini rejected 49% of all tasks and 62% in the spatial-operations group.
- On unsolvable tasks candidate solutions have 50% (o4-mini) to 760% (Claude Sonnet 4) more steps than references, showing models trying many calls before giving up (Table 1).
- Tokens (Table 8): Claude Sonnet 4 used 26.9 million input tokens versus 7.5 to 12.7 million for most others; o4-mini produced the most output tokens (956.6k).
- Error types (Section 6.5): misreading geometric relationships, outdated world knowledge (for example BRICS expansion), over-reliance on internal knowledge, inefficient data handling, and solving with partial data or modifying the task instead of rejecting.

## Limitations
- Stated by the authors (Section 8): no per-model prompt tuning, no human feedback, only the solution algorithm is judged (not the final numbers or the wording of a rejection), moderate set size, no measurement of response variance beyond binomial bounds.
- Vector, tabular and simple raster GIS; no satellite imagery analysis.
- All models are hosted commercial APIs.

## What it means for EvidEO
- Copy the design: include deliberately unanswerable questions (outside India, no Sentinel-1 pass in the window, crop question in a non-crop district) and report rejection accuracy next to answer accuracy.
- The trade-off result supports moving abstention out of the LLM: EvidEO abstains on calibrated instrument confidence, so the decision does not depend on a model's disposition to please.
- Its error type "solving with partial data instead of rejecting" is exactly the failure EvidEO's coverage check should catch.
- Note the gap EvidEO addresses: GeoBenchX checks whether the plan was right but not whether the number was right, nor whether a rejection explains itself. EvidEO's receipts let us verify both.

## Full-text check (2026-10-14)
GeoBenchX is a benchmark; it measures hosted LLMs inside a minimal agent and implements no system of its own beyond that harness. Verdicts say what it implements or measures:
- C1 calibrated per-answer confidence: No. Not implemented or measured.
- C2 threshold abstention with next step: part (measured). Rejection of unsolvable tasks via a reject_task tool is scored (Table 1), but rejection is a model judgement, not a confidence threshold, and the rejection message is a fixed "unsolvable" with no next step; the wording of rejections is explicitly not evaluated (Section 8).
- C3 scene receipts that reproduce: part. The agent is told to name the datasets used, data are frozen local snapshots, temperature is 0 and transcripts are saved (Section 3, Appendix A); but no imagery scenes, and repeat-run variance is not measured.
- C4 SAR chosen automatically under cloud: No. No imagery sensors involved.
- C5 CPU or offline: No. Tools run locally but every answer needs a hosted commercial LLM.
- C6 plain-language questions for non-experts: part (measured). Tasks are casual, sometimes ambiguous natural-language requests from GIS practice (Sections 4, 7), aimed at practitioners rather than non-experts.
Corrections to the earlier entry: the agent framework (LangGraph ReAct, temperature 0, 25-step limit), the exact rejection rates (o4-mini 0.90, GPT-4o 0.62, Claude Sonnet 4 0.17), the solvable count (123), the data inventory, the o3-mini exclusion, and the DOI were missing; the authors' affiliations (World Bank, JP Morgan) were not stated.
Novelty: partial C2, C3 and C6 at the benchmark level only, with no calibrated confidence and no imagery, so it does not threaten EvidEO's "no more than two" claim. It is the closest prior work on scored refusal and should be cited as such.
