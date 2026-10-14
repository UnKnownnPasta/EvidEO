---
id: 095
title: "Earth AI: Unlocking Geospatial Insights with Foundation Models and Cross-Modal Reasoning"
authors: "Aaron Bell, Amit Aides, Amr Helmy, Arbaaz Muslim, and 50+ further authors (Google Research, Google X, Google Cloud, Google Geo, Google Public Sector)"
year: 2025
venue: "arXiv preprint (arXiv:2510.18318; v1 21 October 2025, v4 18 February 2026; also listed on research.google)"
link: https://arxiv.org/abs/2510.18318
code: none found (models offered through Google products and trusted-tester programs; access terms not verified)
category: upcoming
era: upcoming
tags: [big-tech, gemini, geospatial-agent, foundation-models, flood-forecasting, population-dynamics, novelty-threat]
read_depth: "full"
verified: "2026-10-05 via https://arxiv.org/html/2510.18318v2, https://research.google/pubs/earth-ai-unlocking-geospatial-insights-with-foundation-models-and-cross-modal-reasoning/ (search listing); 2026-10-14 full-text read via curl of https://arxiv.org/html/2510.18318 (v4) converted to plain text, plus arXiv API for version dates (sections read: abstract, 1 to 5 including all four limitations subsections, Tables 1 to 12, Appendix A.1 to A.3 including agent framework, baseline prompt, benchmark construction, rubric limitations and example responses; keyword grep for calibration, abstention, provenance, SAR, cloud, CPU and plain-language terms)"
takeaway: "The closest big-tech threat: a Gemini agent that chains Google's imagery, population and flood models into plain-language answers for non-experts (C6 yes), but with no calibrated confidence, no abstention, no scene receipts (its own runs give different answers), RGB-only imagery models and a hosted stack; EvidEO must win on transparent instruments, refusal and auditability"
---

# Earth AI: Unlocking Geospatial Insights with Foundation Models and Cross-Modal Reasoning

## Problem
Geospatial questions (where will a hurricane cause damage, which communities face health or flood risk) need many data types at once: imagery, human activity, weather and hazards. Each Google model covered one slice, and a plain LLM could not combine them reliably.

## Approach
Google groups three families of models under one name and puts an agent on top (Sec. 2):
- Remote Sensing Foundations: contrastive VLMs (RS-SigLIP2, RS-MaMMUT) for zero-shot classification and retrieval, an open-vocabulary detector (RS-OWL-ViT-v2, with a FLAME few-shot add-on), and a ViT backbone (RS-Global MTP), all on high-resolution RGB (0.1 to 10 m). They complement AlphaEarth Foundations, annual 10 m embeddings that fuse optical, radar and climate data.
- Population Dynamics Foundations: graph-network embeddings of regions from maps, search trends, busyness, weather and air quality; now 17 countries and monthly embeddings.
- Environment: Weather API (MetNet), Google Flood Forecasting API (inundation area, severity and probability; history from 1 August 2025) and an experimental 50-member ensemble cyclone model.
- Geospatial Reasoning Agent: built with Google's Agent Development Kit on Gemini 2.5 Pro and Flash; expert sub-agents for demographics (Data Commons), weather, on-the-fly model training (TimesFM, embeddings), Earth Engine dataset search and Google Search fallback, plus place-resolution and imagery toolsets. It loops through plan, act and reflect, and is meant for a map-based natural-language UI (Fig. 4, Appendix A.3.1).

## Data and benchmarks
- RS models: zero-shot classification (FMoW, SkyScript, RESISC45, UCM, AID), retrieval (RSICD, UCM-Captions, RSITMD, NWPU), detection (DOTA, DIOR), and 13 fine-tuning benchmarks for the backbone.
- Population embeddings: 20% held-out regions in 17 countries (India included) for four Earth Engine variables; cross-country extrapolation to France; temporal PopHIVE tests; external partner validations.
- Combined-model tasks: 20 FEMA risk indices, 21 CDC health indicators, Hurricane Ian damage (single event, 3-day lead), DRC cholera forecasting.
- Agent: 100 fill-in-the-blank Q&A questions with gold answers (5 runs each) and 10 crisis-response prompts scored by rubric autoraters (10 runs each).

## Key results
- RS-SigLIP2 zero-shot top-1: FMoW 48.13, RESISC45 80.13, UCM 84.86, AID 78.26 (Table 1; RemoteCLIP is higher on RESISC45 and AID).
- Open-vocabulary detection mAP: DOTA 31.83 and DIOR 29.39 zero-shot; 53.96 and 53.21 with 30-shot FLAME (Table 3).
- Backbone: FMoW 81.70, FLAIR 65.72 mIoU, DIOR 85.50 AP50 (Table 5).
- Population interpolation mean R squared 0.85 across countries, India 0.90 (Table 6).
- AlphaEarth plus Population embeddings: FEMA mean R squared 0.60 vs 0.54 for either alone, an 11% relative gain (Table 8); CDC 0.60 vs 0.56 and 0.42 (Table 9).
- Hurricane Ian: 2,575 predicted vs 2,496 actual damaged buildings 3 days ahead; damaged-class F1 0.59 on held-out events (Sec. 3.1.3, Table 12).
- Agent Q&A overall 0.82 vs 0.50 (Gemini 2.5 Pro with search, maps and code tools) and 0.39 (Flash); analytical questions 0.74 vs 0.33 (Table 10). Crisis prompts mean Likert 0.87 vs 0.38, excluding one prompt the baseline could not answer (Table 11).

## Limitations
- Remote sensing models target high-resolution RGB; multispectral, hyperspectral and temporal tasks are future work (Sec. 4.1). SAR enters only indirectly through AlphaEarth annual embeddings.
- Agent evaluation focuses on designed capabilities and does not test out-of-distribution queries or failed tool chains; the crisis set is small and rubric-only (Sec. 4.4).
- The authors report that the same reasoning gave different final answers when an underlying model's outputs varied (Maui fire example), and that rubrics cannot tell whether the agent analysed imagery or just summarised search results (Appendix A.3.3).
- Baseline Gemini agents were explicitly told to give a best estimate rather than abstain, and rubrics award partial credit for attempts (Appendix A.3.2); no abstention or refusal behaviour is described for the Earth AI agent itself.
- Most models and the agent sit inside Google's commercial stack; open, reproducible access is unclear.

## What it means for EvidEO
- Threat level: high on the headline claim. "Ask a plain-language question about land and get a model-backed answer" is now a Google research product aimed explicitly at non-experts. EvidEO cannot claim to be the first geospatial question-answering agent, nor the first to serve non-experts.
- How EvidEO stays different, and should say so explicitly in the pitch:
  1. Instrument-first: every number in EvidEO comes from a named, inspectable method (SAR threshold, NDVI difference, log-ratio, CLIP zero-shot) on Sentinel-1/2, not from an opaque embedding or a hosted model.
  2. Abstention: EvidEO refuses below a calibrated confidence threshold; Earth AI's confidence intervals are across repeated runs of its benchmark, not per-answer confidence, and its evaluation rewards answering over declining.
  3. Receipts: scene IDs, acquisition dates, region masks and a reproducible receipt per answer; Earth AI lists data sources (for example "Google Flood Forecasts") and reasoning steps, and admits run-to-run answer changes.
  4. Free and sovereign: public STAC, open data, runnable on CPU by an Indian district office, with no dependency on a US cloud account.
  5. India district scale and monsoon flood plus crop condition, with Bhuvan / NRSC compatible outputs.
- Adopt: their decomposition of a query into tool calls and their source-listing answer format are good reference designs; their rubric-based agent evaluation shows what judges will expect. Beat it by publishing a quantitative evaluation that includes abstention rate, selective accuracy, calibration error and re-run identity, which Earth AI does not report.

## Full-text check (2026-10-14)
Ingredients (Earth AI's own system as built and evaluated):
- C1 calibrated per-answer confidence: No. Table 10 and 11 intervals are 95% CIs over repeated benchmark runs; the flood API returns a forecast probability and the cyclone model 50 ensemble members, but these are upstream model outputs, not a calibrated confidence on the agent's answer, and no calibration error is reported.
- C2 threshold abstention with next step: No. No refusal rule for the agent; baselines are prompted to give best estimates instead of abstaining (Appendix A.3.2).
- C3 scene receipts that reproduce: No (closest is a source list). Example answers include reasoning steps and a "Data Provenance" list naming sources (Appendix A.3.3), but no scene IDs or acquisition dates, and the paper reports different outputs across runs (Appendix A.3.3, rubric limitations).
- C4 SAR chosen automatically under cloud: No. Imagery models are RGB only (Sec. 2.1.1, 4.1); radar only inside AlphaEarth annual embeddings; no cloud-triggered sensor choice.
- C5 CPU or offline: No. Gemini 2.5 hosted models, Google Cloud, Earth Engine and Search are all in the answer path.
- C6 plain-language questions for non-experts: Yes. Natural-language, map-based interface intended for non-expert users (Sec. 1, 2.1.1, 4.4, 5), evaluated on free-form questions; no user study, but the system is built and tested for this.

Corrections to the earlier entry: v1 date confirmed as 21 October 2025 (v4 read); the agent uses Gemini 2.5 Pro and Flash via ADK; added that baselines were told not to abstain and rubrics give partial credit; added the authors' own admission of run-to-run answer changes and source-versus-analysis ambiguity; added the "Data Provenance" source list in answers; replaced approximate numbers with exact table values.

Novelty impact: 1 Yes (C6), 0 part. Earth AI is the strongest threat on scope and on C6, but it does not combine more than two ingredients; it supports EvidEO's claim, provided EvidEO does not count C6 alone as a differentiator.
