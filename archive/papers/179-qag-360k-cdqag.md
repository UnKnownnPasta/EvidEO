---
id: 179
title: "Show Me What and Where has Changed? Question Answering and Grounding for Remote Sensing Change Detection"
authors: "Ke Li, Fuyu Dong, Di Wang, Shaofeng Li, Quan Wang, Xinbo Gao, Tat-Seng Chua"
year: 2024
venue: "arXiv preprint (arXiv:2410.23828, v2 13 November 2024); no peer-reviewed venue stated on arXiv or in the official README"
link: https://arxiv.org/abs/2410.23828
code: "https://github.com/like413/VisTA (README fetched; QAG-360K released November 2024, VisTA code June 2025; test set by request, research use only)"
category: rs-benchmark
era: recent
tags: [change-vqa, grounding, cdqag, qag-360k, change-masks, visual-evidence, empty-mask, cdvqa, benchmark]
read_depth: "full"
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, abstract), https://arxiv.org/html/2410.23828 (dataset, method, Tables 2 and 3 text) and the GitHub README at raw.githubusercontent.com/like413/VisTA; WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2410.23828 (v2) converted to plain text, with Table 2 and 3 values cross-checked against the PDF via pdftotext (sections read: abstract, 1 to 6, Tables 1 to 4; the appendices A to C cited in the text are not included in the arXiv version; keyword grep for calibration, abstention, provenance, SAR, cloud, CPU and plain-language terms)"
takeaway: "First change-QA benchmark that pairs every textual answer with a pixel mask of where the change is (360K triplets, 8 question types) and requires an empty mask when nothing changed; closest public benchmark to EvidEO's answer-plus-mask output, though optical only, without confidence, and its headline mask IoU in the text (82.6) contradicts its own Table 2 (44.94)"
---

# Li et al. 2024, change detection question answering and grounding (QAG-360K, VisTA)

## Problem
Change VQA (entry 178) gives text answers with no visual proof, so users cannot check where the model looked. The authors argue answers should come with the change mask that supports them.

## Approach
- New task CDQAG: input two dated images and a question; output a textual answer and a pixel-level mask of the referenced change (Sec. 3.1).
- QAG-360K is generated automatically from Hi-UCD, SECOND and LEVIR-CD semantic or binary change labels with a rule-based triplet engine; an LLM drafted about 20 question templates per type and the authors kept 5 (Sec. 3.2).
- Eight question types: change or not, change to what, change from what, increase or not, decrease or not, largest change, smallest change, change ratio.
- When the queried class did not change or is absent, the target is an empty mask, so models are pushed not to guess a region.
- Baseline VisTA (Sec. 4): CLIP-pretrained text encoder and twin CLIP-pretrained ResNet-101 image encoders, language-guided feature aggregation, a vision-language decoder, a question-answer selector, and a decoder that turns text features into convolution kernels so mask and answer stay consistent. The textual answer is a softmax classification over answer classes; masks are binarised at threshold 0.35. Trained 50 epochs on 4 RTX 4090 GPUs (Sec. 5.1).

## Data and benchmarks
6,810 image pairs (0.1 to 3.0 m, 24 regions in Estonia, China and the USA), 10 land-cover classes, over 360K question-answer-mask triples (about 53 per pair, questions 4 to 15 words). Some biased questions were removed before a 70/10/20 split by image. Metrics: average and overall accuracy (AA, OA) for text; mIoU and oIoU for masks. Also evaluated on CDVQA (2,968 pairs, 6 classes). Baselines are referring-segmentation and VQA models given the same text and mask heads.

## Key results
- †VisTA (two weight-shared backbones) on QAG-360K: AA 73.03, OA 77.35; mIoU 44.94, oIoU 52.13. Single-backbone VisTA: AA 71.16, OA 75.76, mIoU 39.87, oIoU 47.98. Best baseline ETRIS: OA 71.78, oIoU 42.56; SOBA OA 71.98 (Table 2).
- The text (Sec. 5.2) instead claims mIoU 82.6% and oIoU 84.8%, and a †VisTA oIoU of 78.39%; none of these appear in Table 2, which the PDF confirms. The table values should be cited.
- Hardest types: smallest change OA 41.57 and oIoU 24.78 (†VisTA, Table 2).
- CDVQA: test 1 OA 73.1, test 2 OA 68.5 in Table 3 (the text says 69.5), both above SOBA (69.2, 64.8).
- Ablation: dropping the visual-answer branch lowers OA from 75.76 to 70.86 (Table 4).
- Failure cases include over-smooth masks for discrete buildings and faded features mistaken for land-cover change (Fig. 6).

## Limitations
- Very-high-resolution optical only; no SAR, no Sentinel-1/2, no flood class.
- The authors say precise visual answers remain hard (Sec. 6); mask IoU around 45 to 52 confirms it.
- Answers and masks come from one learned model, so a wrong mask still looks authoritative; the softmax answer score is never calibrated or exposed, and there is no abstention beyond the empty-mask convention.
- Labels are rule-generated from existing change datasets, inheriting their label noise and urban bias. Test set is not openly downloadable. Text-versus-table inconsistencies (mIoU, CDVQA test 2) lower confidence in the write-up.

## What it means for EvidEO
- Adopt: the output contract (answer plus supporting mask, empty mask when nothing changed) matches EvidEO's evidence card; use the eight question types and the empty-mask rule as acceptance tests.
- Adopt: report both text accuracy and mask IoU in EvidEO's eval so that a right answer from the wrong pixels is caught. Cite the Table 2 IoU values (about 45 to 52), not the text's 82 to 85.
- Beat: EvidEO's masks come from a calibrated instrument (SAR thresholding or a segmenter) with scene IDs and dates, and it abstains when confidence is low; VisTA always answers.
- Novelty note: this is the strongest prior work for answer-plus-mask change QA, so EvidEO should claim novelty on calibration, abstention, Sentinel provenance and plain-language delivery for officials, not on grounded change answers alone.

## Full-text check (2026-10-14)
Ingredients (VisTA as built and evaluated):
- C1 calibrated per-answer confidence: No. The answer head is a softmax classifier (Sec. 4.3), but no probability is reported to users and no calibration error is measured.
- C2 threshold abstention with next step: No. The empty-mask rule (Sec. 3.2, attribute 4) teaches "no change" answers, which is a correct negative answer, not a decline with a suggested fix.
- C3 scene receipts that reproduce: No. Image pairs from existing datasets; no scene IDs, acquisition dates or re-run check.
- C4 SAR chosen automatically under cloud: No. Optical only.
- C5 CPU or offline: part. VisTA is a small ResNet-101 plus CLIP text encoder model with no LLM, so a local offline answer path is plausible, but only GPU training is reported and no CPU inference is measured (Sec. 5.1). Counted as part at most; strictly it is unevaluated.
- C6 plain-language questions for non-experts: part. Questions are natural-language templates (Sec. 3.2), but the vocabulary is closed (8 types, 10 classes) and answers are class labels; no non-expert study.

Corrections to the earlier entry: mIoU and oIoU are 44.94 and 52.13 (†VisTA, Table 2), not 82.6 and 84.8 (those come from the paper's inconsistent text); CDVQA test 2 OA is 68.5 in Table 3; added single-backbone numbers, the softmax answer head, mask threshold and training hardware; noted the arXiv version lacks the appendices.

Novelty impact: none. 0 Yes, 2 part at most (C5 unevaluated, C6 templated).
