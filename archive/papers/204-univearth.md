---
id: 204
title: "Towards LLM Agents for Earth Observation"
authors: "Chia Hsiang Kao, Wenting Zhao, Cheryl Lam, Aarush Umap, Shreelekha Revankar, Samuel Speas, Snehal Bhagat, Rajeev Datta, Cheng Perng Phoo, Utkarsh Mall, Carl Vondrick, Kavita Bala, Bharath Hariharan"
year: 2026
venue: "ACL 2026 Findings (per arXiv comment and an ACL Anthology preview page listing 2026.findings-acl.124); earlier ICML 2025 TerraBytes workshop; arXiv:2504.12110 (v1 April 2025, v3 5 October 2026)"
link: https://arxiv.org/abs/2504.12110
code: "Dataset and project page https://iandrover.github.io/2025_univearth/ (per the paper; page not opened)"
category: rs-benchmark
era: recent
tags: [univearth, google-earth-engine, code-agents, live-data-retrieval, nasa-earth-observatory, hallucinated-collection-ids, reflexion, yes-no-qa, failure-taxonomy]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2504.12110 (title, authors, v3 date, ACL 2026 Findings comment, abstract) and curl of https://arxiv.org/html/2504.12110v3 (benchmark construction, Table 1 sources, Table 3 results, collection-ID hallucinations, reflexion results, Limitations); WebFetch of arxiv.org was rate limited (HTTP 429); ACL Anthology page seen only as a search result, not opened; 2026-10-14 full-text read via curl of https://arxiv.org/html/2504.12110v3 converted to text (sections read: Abstract, 1 Introduction, 2 Related Work, 3 Benchmark Construction with Tables 1 and 2, 4 Benchmarking incl. Tables 3 and 4 and Sec 4.1 to 4.4, 5 Conclusion, Limitations, Appendix A dataset, B GEE background, C error analysis with Tables 5 and 6, D reviewer instructions)"
read_depth: "full"
takeaway: "UnivEARTH (408 yes/no questions from NASA Earth Observatory) makes LLM agents fetch live data by writing Google Earth Engine code: best zero-shot accuracy 40.0%, code fails over 44% of the time, collection IDs are hallucinated, and reflexion lifts the best model to 64.5% while wrong answers rise; the strongest evidence that free-form code agents over live archives are unreliable, which favours EvidEO's fixed instruments"
---

# Kao et al. 2026, UnivEARTH

## Problem
Most EO agent benchmarks use curated images and predefined tools. Real EO questions require choosing the right sensor, product, place and date from a large live catalogue, under revisit and cloud constraints, which earlier benchmarks do not test (Sec 1).

## Approach
- 408 yes/no questions mined from NASA Earth Observatory articles (cutoff 30 September 2025), each checked to be answerable with data available in Google Earth Engine (GEE). The first 140 questions were reviewed by four reviewers (each saw half) and revised until full agreement on the answer; the extended 268 were each reviewed by two reviewers until consensus (Sec 3.2).
- Agents plan, write a GEE Python script, run it against the live catalogue, and Gemini-2.5-Flash derives the final answer from the script output, question and code (Sec 4).
- Failure taxonomy, also assigned by Gemini-2.5-Flash: empty collection (C1), no valid pixels after masking such as cloud masking (C2), calculation failure (C3), and code or syntax error (D).
- Variants: Python vs JavaScript API, a two-round dialogue that first picks a modality (Landsat, MODIS, VIIRS, other) and then injects correct collection IDs and band names, reflexion (up to two debugging rounds on execution errors), and in Appendix C a three-round re-planning run with Oscar.

## Data and benchmarks
- Topics: hydrosphere (34%, including surface water extent and precipitation), temperature (14%), land cover (13%), atmosphere (13%), fire, human activity, geology (Sec 3.3).
- Main sources (Table 1, 443 source mentions): Landsat 4 to 9 (162), MODIS (140), VIIRS (60), Sentinel-5P (16), GEOS (17), GRACE (11), GPM, CHIRPS, SMAP and others; Sentinel-2 appears twice and Sentinel-1 is not listed.
- Questions name a place and a date or period, sometimes with explicit coordinates (Table 2, Appendix D).
- Models: Gemini-2.5-Pro and Flash, Claude-4.5-Sonnet and Haiku, GPT-5, DeepSeek-Reasoner and Chat, Kimi-k2.

## Key results
- Best zero-shot accuracy 40.0% (Claude-4.5-Sonnet), then Gemini-2.5-Pro 36.9% and GPT-5 33.1%; Flash, Haiku and Kimi below 20% (Table 3).
- Syntax and method errors 21.4% for the best model and above 30% for all others; empty collections around 15% for most models but 4.4% for GPT-5 (Table 3).
- Typical hallucinated GEE collection IDs are wrong version, tier or provider strings (Table 4).
- Supplying correct collection IDs cut syntax errors (VIIRS for Claude 23.5% to 0%) and raised VIIRS accuracy from 38.2% to 61.5%, but the wrong-answer rate rose from 8% to 23.1% (Sec 4.3).
- Python vs JavaScript: Claude 40.0% to 43.8% in JavaScript; Gemini-2.5-Pro and GPT-5 slightly worse (Sec 4.2).
- Reflexion: Claude-4.5-Sonnet 40.0% to 64.5%, GPT-5 33.1% to 59.3%; wrong-answer rate rose at the same time (15.7% to 26.0% for Claude), so running code is not correct code (Sec 4.4).
- Appendix C (Gemini-2.5-Pro, zero shot): wrong dataset IDs 14.2%, temporal or spatial mismatch 15.7%, wrong band names 9.6%, pure syntax errors only 10.0% (Table 5). Oscar re-planning lifts correct answers from 36.8% to 55.9% while wrong answers rise from 9.6% to 21.3% (Table 6).
- The authors themselves call these scores only marginally above chance for a yes/no task.

## Limitations
- No unanswerable or inconclusive questions (the authors list this as a limitation), so abstention is not measured, although reviewers had an "I don't know or not conclusive" option (Appendix D).
- Yes/no only; reviewers were computer science students checking against article text, not domain experts.
- Both the final answer and the error category are produced by an LLM (Gemini-2.5-Flash), not by a fixed parser.
- No calibration, confidence or provenance output is evaluated, though the code itself is an implicit receipt.
- Dependent on GEE; the text calls GPT-5's 33.1% to 59.3% change a 79 percentage point increase, when it is about 26 points (79% relative), so read numbers from the tables. The Limitations section also calls the benchmark "OpenEARTH", a leftover name.

## What it means for EvidEO
- Avoid: letting an LLM write retrieval or analysis code at query time. UnivEARTH shows that even frontier models pick wrong collections, empty date windows and broken cloud masks; EvidEO's fixed STAC queries and fixed instruments avoid all four failure classes.
- Adopt: the failure taxonomy (empty collection, no valid pixels, calculation failure) maps directly onto EvidEO's abstention reasons; an empty Sentinel-2 window or all-cloud scene should trigger the SAR fallback or an explicit abstain with the reason in the receipt.
- Adopt: add unanswerable questions to EvidEO's evaluation set, the gap the authors name.
- Novelty: weakens the claim slightly on one axis. It shows live satellite data retrieval by a language agent from natural-language questions is already published and peer reviewed (ACL Findings 2026), so live retrieval alone is not new. It has no calibrated confidence, abstention, SAR fallback or non-expert delivery, and its low accuracy is an argument for EvidEO's constrained design rather than against its novelty.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. Only correctness and error-category rates (Table 3); no probabilities.
- C2 Threshold abstention with a next step: No. Failures are classified after the fact (C1, C2, C3, D) but the agent never declines; inconclusive answers are excluded by design (Limitations).
- C3 Scene receipts that reproduce: No. The generated GEE script is kept and could be re-run, but answers do not list scene IDs or dates and no re-run reproducibility is tested; the answer step is an LLM.
- C4 SAR chosen automatically under cloud: No. The agent does choose the sensor and collection itself (the point of the benchmark), but no SAR data are in scope (Table 1) and cloud is only a failure category (C2), not a trigger for switching sensors.
- C5 CPU or offline deployment: No. Hosted frontier LLMs plus server-side GEE computation (Appendix B).
- C6 Plain-language questions for non-experts: part. Questions are natural language, but phrased for scientists with exact dates and sometimes coordinates; no non-expert evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- The review process was not uniform: four reviewers on the first 140 questions, two per question on the remaining 268 (Sec 3.2).
- GPT-5's empty-collection rate (4.4%) is much lower than the "around 15% for most" pattern (Table 3).
- Appendix C adds a second correction method (Oscar re-planning, 36.8% to 55.9%) with the same rise in wrong answers.

Novelty implications: zero full ingredients and one part (C6); automatic sensor selection exists but without SAR. It does not threaten the "no more than two" claim.
