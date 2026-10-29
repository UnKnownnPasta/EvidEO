---
id: 195
title: "RS-Agent: Automating Remote Sensing Tasks through Intelligent Agent"
authors: "Wenjia Xu, Zijian Yu, Boyang Mu, Jiuniu Wang, Zhiwei Wei, Mugen Peng"
year: 2026
venue: "SCIENCE CHINA Information Sciences, 69(8), 180302 (2026), DOI 10.1007/s11432-026-5026-5; arXiv:2406.07089 (v1 June 2024, v4 July 2026)"
link: https://arxiv.org/abs/2406.07089
code: "Paper says code will be at https://github.com/IntelliSensing/RS-Agent (release status not checked)"
category: rs-vlm
era: recent
tags: [agents, task-planning, rag, dualrag, sar-tools, despeckling, qwen2.5-32b, langchain, vqa, counting]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, journal_ref, DOI, abstract), curl to https://api.crossref.org (journal title and DOI) and curl to https://arxiv.org/html/2406.07089v4 (default backbone, retrieval setup, SAR tool list); WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2406.07089v4 converted to text (sections read: Abstract, 1 Introduction, 2 Related Works, 3 method incl. 3.1 to 3.5, 4 Experiments incl. Tables 1 to 8, 5 Conclusion and limitations, Supplementary A prompts (headings only), B end-to-end success Table S1, C full planning Table S2, D tool list Table S3, E multi-tool example, F user interface)"
read_depth: "full"
takeaway: "A published 2026 RS agent that routes questions to 27 expert tools (18 evaluated tasks, including SAR despeckling, detection and change detection) with over 95% first-tool planning accuracy; it confirms LLM-as-router beats end-to-end MLLMs, but works on a user-uploaded image and returns tool outputs without scene provenance, calibrated confidence or abstention"
---

# Xu et al. 2026, RS-Agent

## Problem
RS multimodal LLMs follow instructions and describe images but struggle with tasks that need multi-source data, fine spatial reasoning and expert procedures.

## Approach
- Central Controller: an LLM (default Qwen2.5-32B-Instruct, built on LangChain) that reads intent and plans (Sec 3.2, 4.1).
- Toolkit of 27 tools in a three-level hierarchy (modality, analysis level, geometry and semantics), listed in Table S3: optical tools (super-resolution, denoising, cloud removal, dehazing, VQA via GeoChat, detection, aircraft type, scene and land-cover classification, building damage, building and road extraction, counting, knowledge reasoning) and SAR tools (despeckling, SAR detection, SAR aircraft type, rotated detection, land-cover classification, semantic segmentation, sea-land segmentation, multi-temporal SAR change detection, target recognition). 18 tasks are used for evaluation (Sec 3.3, 4.1).
- Solution Space with Task-Aware Retrieval: the LLM first maps the query to a predefined task type, then retrieves expert-written solution documents (34 in total: 27 single-tool templates and 7 multi-tool RSVQA pipelines) with m3e-base embeddings and FAISS (Sec 3.4).
- Knowledge Space with DualRAG: weighted keyword plus global semantic retrieval over a Wikipedia-derived RS corpus stored as a knowledge graph, with an aircraft subset (RSaircraft, 65 categories) as case study; top N = 30 documents (Sec 3.5, 4.1).
- LLM-agnostic: tested with ChatGPT, LLaMA, Qwen and DeepSeek backbones.
- The user uploads an image and types a request in a chat interface (Supplementary F).

## Data and benchmarks
Nine datasets covering 18 tasks. Planning accuracy is whether the first invoked tool is correct, on about 20 query-solution pairs per task, mixing clear and ambiguous instructions (Sec 4.2.1); a second set has 360 queries over 18 tasks (Sec 4.2.2). Task benchmarks: DOTAv1 counting (458 images, 1,099 questions), RSVQA-LR (772 images), RSSDIVCS, AID and UCMerced. DualRAG judged pairwise by GPT-4o-mini against LightRAG.

## Key results
- Planning accuracy vs Remote Sensing ChatGPT on its seven tasks (Table 1): 84.89% vs 72.66% (gpt-3.5-turbo-1106), 87.77% vs 82.01% (gpt-3.5-turbo), 95.68% vs 88.49% (gpt-4o-mini). The gain is not uniform; with gpt-4o-mini the baseline scores higher on scene classification and image captioning and ties on land-use segmentation.
- Over all 18 tasks (Table S2): gpt-4o-mini 99.17%, Qwen2.5-72B 98.61%, Qwen2.5-32B 97.78%, LLaMA-3.1-8B 75.28%; speeds measured on RTX 4090 GPUs.
- Ablation (Table 6): without the Solution Space, multi-tool planning accuracy is 9.42%; with task inference plus solution retrieval it is 90.62% (single-tool 69.06% to 93.53%).
- Counting on DOTA (Table 3): 33.30% exact vs 17.65% GeoChat; RSVQA-LR average 90.88% vs 90.70% GeoChat (Table 4, a thin margin); scene classification 96.88% on AID and 98.63% on UCMerced (Table 5), using a ViT fine-tuned on RSSDIVCS.
- End-to-end RSVQA-LR success (Table S1): 90.88% full system vs 84.24% to 84.57% for partial variants.

## Limitations
- Uses a 32B controller on GPUs; not sized for CPU or offline use. The authors list dependence on large proprietary LLMs as a limitation (Sec 5).
- Authors' own list: task inference sometimes over-abstracts queries, tool arguments can be malformed, upstream errors propagate in multi-tool chains, metrics do not check intermediate steps, and the knowledge and solution bases are small and hand curated (Sec 5).
- Tools return outputs without uncertainty; there is no rule for refusing when a tool is unreliable.
- Works on one user-supplied image; no catalogue search, dates or flood mapping. Planning test sets are small (about 20 queries per task).

## What it means for EvidEO
- Adopt: task-type identification before retrieval is a simple, strong pattern for EvidEO's intent parser (flood extent, flood change, crop change), and supports keeping the question set closed. The ablation (9% to 91% multi-tool planning) is a citable number for that choice.
- Avoid: RAG over free text documents is not needed for EvidEO's narrow scope and adds hallucination risk.
- Beat: RS-Agent routes and executes but does not tie answers to scene IDs and dates, report calibrated confidence or abstain; EvidEO's claim remains open against this published system.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. No confidence output or calibration metric anywhere (Sec 4).
- C2 Threshold abstention with a next step: No. The pipeline always produces an answer (Algorithm 1).
- C3 Scene receipts that reproduce: No. Inputs are uploaded images; no scene IDs, dates or re-run test.
- C4 SAR chosen automatically under cloud: No. The agent picks SAR tools when the user supplies a SAR image (Table 7 cases), and an optical cloud-removal tool exists (Table S3), but it never chooses a sensor or switches to radar because optical is blocked.
- C5 CPU or offline deployment: No. Open-weight Qwen2.5 controllers can run locally, but all reported runs use GPUs (RTX 4090) or hosted GPT models (Table 2 notes); no CPU path.
- C6 Plain-language questions for non-experts: part. The interface accepts plain requests without remote sensing or programming expertise (Supplementary F) and vague queries are handled (Sec 4.6), but there is no non-expert user evaluation.

What the abstract-level entry got wrong or left unconfirmed:
- The toolkit has 27 tools, not 18; 18 is the number of evaluated tasks (Sec 3.3, Table S3).
- "Task-planning accuracy" means the first invoked tool is correct (Sec 4.2.1), a narrow measure.
- SAR coverage is broader than despeckling and detection: it includes multi-temporal SAR change detection and sea-land segmentation (Table S3).

Novelty implications: one part (C6). It does not threaten the "no more than two" claim. It is the clearest published case of an agent with SAR tools, so EvidEO should not claim "SAR tools in an agent" as new, only automatic sensor choice under cloud.
