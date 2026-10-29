---
id: 013
title: "Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data"
authors: "Chenhui Zhang, Sherrie Wang"
year: 2024
venue: "CVPR 2024 Workshops (EarthVision), pp. 7839-7849; also presented at ICLR 2024 ML4RS workshop"
link: https://arxiv.org/abs/2401.17600
code: https://github.com/Earth-Intelligence-Lab/vleo-bench
category: rs-benchmark
era: recent
tags: [gpt-4v, vleo-bench, counting, localization, change-detection, xbd, disaster, evaluation, refusal-rate]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2401.17600, https://vleo.danielz.ch/ and https://openaccess.thecvf.com/content/CVPR2024W/EarthVision/html/Zhang_Good_at_Captioning_Bad_at_Counting_Benchmarking_GPT-4V_on_Earth_CVPRW_2024_paper.html; 2026-10-14 full-text read via raw arXiv HTML (arxiv.org/html/2401.17600, v1 of 31 Jan 2024) converted to text (sections read: abstract, 1 introduction incl. limitations, 2 scene understanding, 3 localization and counting, 4 change detection, 5 conclusion, appendix A data sheet, B, C incl. Tables 1-12 and 28-30)"
takeaway: "Let the VLM caption and explain but route counts, boxes and damage to dedicated instruments: GPT-4V localises only 7.6% of DIOR-RSVG referents at IoU 0.5 (mean IoU 0.16) against 76.8% for the specialist MGVLF, and its damage-category counts on xBD have R2 of about 0.1"
---

# Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data

## Problem
General-purpose instruction-following VLMs such as GPT-4V were being proposed for Earth observation work without a quantitative picture of what they can and cannot do on real EO tasks. The authors frame this around a non-ML analyst (their example is a UN analyst assessing building damage) who would like to ask in natural language instead of training a model.

## Approach
VLEO-Bench is assembled from existing datasets plus one new one, grouped into three capability areas: scene understanding, localization and counting, and change detection. Five models are prompted zero-shot: GPT-4V, InstructBLIP-FLAN-T5-xxl, InstructBLIP-Vicuna-13b, LLaVA-v1.5 and Qwen-VL-Chat. Answers are parsed and scored against labels; for counting the authors report MAE, MAPE and R2, for localization Pr@IoU thresholds, mean IoU and centroid distance. Every task also reports a refusal rate (refusing or giving an unparsable answer), and refusals are counted as wrong. Several system prompts explicitly tell the model to answer without refusal, because generic prompts produced refusal rates too high to score.

## Data and benchmarks
- Landmark recognition (new): 602 US landmarks from Google Landmarks matched to OSM polygons, imaged with NAIP; five-option multiple choice (Table 12).
- Captioning: RSICD, 8,730 training plus 1,009 validation images queried.
- Land use / land cover: fMoW-WILDS (2,000 sampled test images), PatternNet (1,000 sampled), BigEarthNet Sentinel-2 RGB (1,000 sampled, multi-label).
- Referring expression localization: DIOR-RSVG (the source dataset has 23,463 images of 800x800 px; the number of test items queried is not stated).
- Counting: NEON-Tree (194 validation RGB images), COWC cars (1,000 images from 4 locations), aerial animals from Kenya (112 test images), xBD buildings (933 test images).
- Change detection: xBD pre/post pairs, counting buildings per damage class.
- Benchmark released on Hugging Face under CC BY-SA 4.0 (appendix A.3).

## Key results
- Landmarks: GPT-4V overall accuracy 0.671, InstructBLIP-T5 0.400, Qwen 0.292 (Table 1). Qwen refused 31.4% of landmark questions, GPT-4V 5.4% (Table 2).
- Captioning: all models have RefCLIPScore 0.75 to 0.79 (GPT-4V 0.754) and near-zero BLEU-4 versus 0.178 for a 2017 LSTM specialist (Table 3); the authors argue the human RSICD captions are poor references.
- Classification: GPT-4V accuracy 0.19 on fMoW-WILDS against 0.74 (ID) and 0.49 (OOD) for fine-tuned CLIP (Table 4); accuracy 0.73 and F1 0.71 on PatternNet (Table 5); F1 0.38 on BigEarthNet (Table 6).
- Referring localization on DIOR-RSVG (Table 7): GPT-4V Pr@0.5 0.076, mean IoU 0.158, mean centroid error 147 px, refusal 0.02. Qwen Pr@0.5 0.053 with 0.69 refusal; both InstructBLIP models refused or failed format 100%; LLaVA scored 0 (it output normalised coordinates). The supervised MGVLF reaches Pr@0.5 0.768 and mean IoU 0.680; these MGVLF numbers are quoted from Zhan et al. 2023, not re-run on the same items.
- Counting R2 for GPT-4V: NEON trees 0.249 (Table 8), COWC cars 0.612 (Table 9), animals 0.076 (Table 10), xBD buildings before disaster 0.676 (Table 11). The COWC specialist has MAE 0.248 against GPT-4V's 2.853.
- Change detection on xBD (Table 11): GPT-4V R2 is 0.108 (no damage), 0.062 (minor), 0.055 (major), 0.106 (destroyed); it systematically undercounts damaged buildings. The three non-GPT-4V/Qwen models failed to give parsable JSON over 90% of the time.

## Limitations
- Stated by the authors: possible training-data contamination, limited error analysis, static benchmark.
- Optical RGB only; the paper notes current VLMs cannot ingest multispectral, SAR or multi-temporal stacks, and none segment.
- Closed-model behaviour may drift with API versions; arXiv version is v1.
- Internal inconsistencies in the arXiv text: the Qwen-VL-Chat row in Table 5 (PatternNet: precision 0.57, recall 0.39, F1 0.40, refusal 0.044) is identical to the Qwen row in Table 6 (BigEarthNet), which looks like a copy error, so treat Qwen numbers on those two tasks as unreliable. The text gives Qwen localization as Pr@0.5 0.040, mean IoU 0.007, centroid 336 px, while Table 7 gives 0.053, 0.009 and 262 px. The introduction gives GPT-4V NEON-Tree R2 as 0.20 and the results text gives COWC R2 as 0.528, while Tables 8 and 9 give 0.249 and 0.612. Cite table values.

## What it means for EvidEO
- The title is our design rule: let the VLM caption and describe, but never let it produce counts or boxes directly; use a detector or segmenter and attach confidence.
- Damage assessment from before/after pairs is exactly where general VLMs fail, so our change detection should be a dedicated model with the VLM only explaining its output.
- Reuse the three-way capability split (understanding, localization/counting, change) for our own evaluation report.
- Note the contrast in method: VLEO-Bench pushes models not to refuse and scores refusal as failure; EvidEO treats a justified abstention as a correct outcome and scores it with risk-coverage, which is a clear point of difference to state.
- Abstain by default on counting questions when detector confidence is low.

## Full-text check (2026-10-14)
- Changed: added the model list, per-task data sizes, licence, and table-referenced numbers for every task (previously only the project-page headlines). Added the DIOR-RSVG Pr@0.5 of 0.076 and MGVLF 0.768, and noted that MGVLF is quoted from its own paper. Resolved the earlier "per-dataset numbers for open models were not verified" flag. Documented the Table 5/6 Qwen duplicate row and three text-versus-table mismatches.
- Refusal and calibration: the benchmark does measure refusal rate on every task, but only as an instruction-following failure counted as wrong, and prompts actively discourage refusal. It has no calibration metric, no confidence elicitation and no credit for abstaining. The single "calibrate" hit is a remark that a good R2 would let counts be calibrated post hoc.
