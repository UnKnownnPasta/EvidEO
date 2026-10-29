---
id: 172
title: "Selective Tool Use for Agentic Change Visual Question Answering in Remote Sensing"
authors: "Yakoub Bazi, Mohamad M. Al Rahhal, Mohamed A. Mekhtiche, Mansour Zuair"
year: 2026
venue: "arXiv preprint (arXiv:2609.14523, v1 13 September 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2609.14523
code: "https://github.com/yakoubbazi/ToolChangeVQA (stated as to be released; not fetched)"
category: rs-vlm
era: upcoming
tags: [change-vqa, tool-use, deterministic-tools, lora, qwen3.5-4b, cdvqa, semantic-change-detection, evidence-conditioned-answering]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2609.14523v1 (full text including Tables I to IV); WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2609.14523v1 converted to text (sections read: Abstract, I Introduction, II-A to II-C method, III-A benchmark construction with Tables I and II, III-B setup, III-C results with Table III, III-D predicted evidence with Table IV, IV Conclusion; the paper has no appendix)"
read_depth: "full"
takeaway: "Closest 2026 match to EvidEO's architecture: a LoRA-tuned 4B VLM that calls one deterministic change tool lifts measurement questions from about 50% to near 100% with ground-truth maps, but only to 63 to 66% with predicted maps, with no confidence or abstention, so instrument quality and calibrated refusal are where EvidEO must win"
---

# Bazi et al. 2026, selective tool use for change VQA

## Problem
VLMs answer change questions such as "did anything change" well, but are unreliable on questions that need transition statistics, proportions or locations, because they never actually compute them.

## Approach
- A single VLM (Qwen3.5-4B, LoRA rank 16 on selected decoder attention projections, vision encoder and alignment modules frozen) either answers directly or emits one structured call to a deterministic tool (Sec II-A, III-B).
- Three tools operate on bi-temporal semantic maps: transition (class transitions and area statistics), spatial (location of new regions), temporal summary. The tool returns a structured observation and the same VLM writes the final answer (Sec II-B).
- Semantic maps are never shown to the VLM; at most one tool call per question; no separate router.
- Which families go direct and which go to which tool is fixed at dataset construction (Table I); supervision for tool choice, arguments and observations is generated automatically from CDVQA's six-class annotations (Sec III-A).

## Data and benchmarks
Tool-augmented CDVQA: 2,968 image pairs and 47,586 questions in eight families (F1 to F2 direct, F3 to F8 tool based), split 70/15/15 by image pair; 7,164 test questions, of which 3,970 are tool dependent (Table II). Six land-cover classes: non-vegetated ground, buildings, playgrounds, water, low vegetation, trees. The paper does not name the imaging sensor. Two evidence settings: reference (ground-truth maps, which the authors say is an oracle, not a fully automatic setting) and predicted (a semantic change detection model with 73.08 mIoU, 25.42 SeK, 65.29 F_scd and 87.38% pixel accuracy, Table IV). Metric: exact-match accuracy, overall (OA) and family average (AA).

## Key results (Table III)
- Direct answering: 73.77% OA, 69.11% AA; 50.34% on proportion (F4), 47.20% on largest or smallest change (F5), 52.42% on location of new regions (F6).
- With reference maps: 88.79% OA, 89.65% AA; F3 97.77%, F4 99.83%, F6 99.76%, F8 100%; F5 only 59.51%.
- With predicted maps: 77.47% OA, 75.06% AA; F4 63.40%, F6 66.46%, F8 93.46%, F5 48.69%. OA drops 11.32 points from reference to predicted maps.
- The direct families F1 and F2 lose slightly under the tool-trained model (88.60 to 88.36 and 84.74 to 82.06), so the overall gain comes from the tool families.
- On the 3,970 tool-dependent questions the model followed the tool policy and executed the required tool correctly; evidence-conditioned answer accuracy was 91.56%, so most residual errors come after the tool returns, when the VLM compares several quantities (Sec III-C).
- Trained for three epochs on a single RTX A6000.

## Limitations
- Six-class urban land-cover benchmark (CDVQA); no SAR, no Sentinel data, no satellite scene search.
- Tool routing is fixed per question family, so the model learns a mapping rather than open-ended planning.
- No confidence, abstention or provenance; a wrong predicted map silently produces a confident wrong answer.
- The VLM still does the final comparison of numbers, which is where F5 errors arise.
- A single run per setting; no variance reported.

## What it means for EvidEO
- Adopt: strong independent support for EvidEO's design (small LoRA VLM routes, deterministic tool measures). Cite the jump from about 50% to near 100% on measurement questions when evidence is exact.
- Beat: the drop from reference to predicted maps shows that answer quality is capped by the instrument; EvidEO must report the instrument's own calibrated confidence and abstain when it is low, which this paper does not do.
- Adopt: let code, not the VLM, do comparisons and rankings of returned numbers (the F5 failure); EvidEO's explainer should only verbalise values already computed and stored in the evidence card.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. No probabilities or calibration anywhere in the paper; only exact-match accuracy (Sec III-B).
- C2 Threshold abstention with a next step: No. The model always answers, either directly or after one tool call (Sec II-A).
- C3 Scene receipts that reproduce: No. Inputs are dataset image pairs; the tool observation is passed to the VLM but no scene IDs, dates or re-run test are reported.
- C4 SAR chosen automatically under cloud: No. Single optical benchmark, no sensor choice.
- C5 CPU or offline deployment: No. A 4B VLM trained and run on an RTX A6000 GPU (Sec III-B); no CPU timing.
- C6 Plain-language questions for non-experts: part. Natural-language questions, but templated CDVQA families, not non-expert queries; no user study.

What the abstract-level entry got wrong or left unconfirmed:
- "Aerial RGB" is not stated in the paper; it only names CDVQA and its six classes. Rephrased.
- The earlier entry missed that direct families F1 and F2 lose a little accuracy under tool training, and the 91.56% evidence-conditioned accuracy on tool questions.
- Author listing: the paper prints "Mohamed M. Al Rahhal"; the arXiv record spelling "Mohamad" is kept here pending a check.

Novelty implications: zero full ingredients and one part (C6). It does not threaten the "no more than two" claim; it supports EvidEO's router-plus-instrument split and its argument that the instrument, not the language model, caps accuracy.
