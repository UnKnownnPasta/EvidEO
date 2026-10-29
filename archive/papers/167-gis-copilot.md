---
id: 167
title: "GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis"
authors: "Temitope Akinboyewa, Zhenlong Li, Huan Ning, M. Naser Lessani"
year: 2025
venue: "International Journal of Digital Earth, 18(1), article 2497489 (2025); arXiv preprint November 2024 (2411.03205)"
link: https://doi.org/10.1080/17538947.2025.2497489
code: "QGIS plugin SpatialAnalysisAgent (https://plugins.qgis.org/plugins/SpatialAnalysisAgent-master); source on GitHub via a shortened link given in the paper"
category: eo-agents
era: recent
tags: [gis-agent, qgis, code-generation, autonomous-gis, non-experts, natural-language-interface, tool-documentation, gpt-4o]
read_depth: "full"
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2411.03205 (title, authors, abstract) and api.crossref.org (journal, volume, issue, article number, 2025-04-28 date); 2026-10-14 full-text read via arXiv PDF (arxiv.org/pdf/2411.03205, v4 of 22 Nov 2024, 65 pages) with pdftotext -layout (sections read: abstract, 1-7 incl. framework, workflow, case studies, Table 1 evaluation, failure analysis, discussion, limitations; appendices 1-2 tool documentation samples, skimmed appendices 3-5 test-case tables). The journal version of record was not read and may differ."
takeaway: "A GPT-driven agent inside QGIS that writes and runs PyQGIS code from plain-language requests; on 110 author-built tasks it succeeds within three attempts on 92% of basic, 83% of intermediate and 75% of advanced tasks, failing mainly on parameters, field names and missing reprojection, and it offers no calibrated confidence, abstention or provenance card, which is the gap EvidEO fills"
---

# Akinboyewa et al. 2025, GIS Copilot

## Problem
Generative AI could make spatial analysis accessible, but earlier LLM-GIS systems (LLM-Geo, GeoGPT, ChatGeoAI, QChatGPT, IntelliGeo) either run outside established GIS software or only advise users without executing tasks.

## Approach
- A QGIS plugin with four modules: data understanding (reads format, fields, CRS, extent and resolution so users need not name fields), GIS interface interaction (uses loaded layers, loads results back), code review and self-debugging (re-generates code after execution errors), and tool documentation.
- 390 native QGIS and GDAL tools are documented in TOML (description, parameters, code example); custom tools built on GeoPandas, PySAL, seaborn and similar can be registered plug-and-play.
- Workflow: break the request into steps, select tools, generate Python, execute, display layers or reports; the generated code and a workflow diagram are shown in real time and can be edited.
- Powered by OpenAI GPT models; the limitations section names GPT-4o.
- Builds on the Autonomous GIS vision from the same group (entry 091).

## Data and benchmarks
- 110 tasks written by the authors: 60 basic (one tool, usually one layer), 30 intermediate (multi-step with the steps given), 20 advanced (multi-step, the agent must plan). Mostly US vector and DEM data, plus a few Landsat raster tasks (NDVI for Akure, Nigeria; band compositing).
- A task counts as failed if it is still unsuccessful after three attempts. Success is judged by the authors; there is no independent reference output or accuracy metric beyond pass or fail.

## Key results
- Table 1: basic 52 first-attempt and 3 second-attempt successes, 5 failures (92%); intermediate 13, 4 and 8 successes, 5 failures (83%); advanced 10, 4 and 1 successes, 5 failures (75%). The section 4.4 text instead says 95%, 80% and 75%, which does not match the table counts.
- Tool selection was described as consistently correct; failures came from wrong parameter types (e.g. a vector layer passed to gdal:proximity, which needs raster), field-name mismatches when shapefiles truncate names to 10 characters, and omitted reprojection unless asked.
- Case studies show buffers, contours, clipping, zonal statistics, terrain derivatives, attribute joins, a correlation analysis and NDVI; one NDVI map needed manual symbology fixes.

## Limitations
- Generated code is the answer path, so correctness depends on the LLM each time; there is no confidence, calibration or abstention. The authors instead rely on transparency and ask users to review code.
- The authors themselves note that non-experts may not notice missing reprojection or unit errors that an expert would catch, so they may unknowingly accept wrong analyses.
- Needs QGIS and user-supplied data layers; data retrieval is future work.
- Evaluation is a curated, author-judged task set, not field use.

## What it means for EvidEO
- **Closest prior art for the 'non-expert asks in plain language' framing**, so EvidEO must state the difference: GIS Copilot helps a user drive a GIS and expects them to check code; EvidEO hands a non-GIS official a measured answer with scene IDs, a mask, calibrated confidence and an abstain path.
- Its own failure list (silent reprojection and unit errors that non-experts cannot see) is a direct argument for fixed, tested instruments instead of free code generation; this echoes GeoGPT (entry 090) and Earth-Agent (entry 094).
- **Adopt** its tool-documentation-in-prompt pattern for EvidEO's parser, limited to describing which instruments exist and what they cannot answer.
- Offer a QGIS export of EvidEO's mask and receipt so GIS staff can inspect cards in the tool they already use.

## Full-text check (2026-10-14)
- Changed: replaced the "exact rates not verified" placeholders with Table 1 counts and rates (92% / 83% / 75%), noted the text-versus-table mismatch (95% / 80% / 75%), added task counts per level (60 / 30 / 20 of 110), the three-attempt rule, the 390 documented tools, the GPT-4o backbone, failure causes, and the code and plugin location. Recorded that this read is of arXiv v4, not the journal version.
- Refusal and calibration: none. The agent always attempts the task; the only "confidence" hit refers to users' confidence in results. There is no abstention, uncertainty estimate or calibration analysis.
