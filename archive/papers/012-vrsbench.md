---
id: 012
title: "VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding"
authors: "Xiang Li, Jian Ding, Mohamed Elhoseiny"
year: 2024
venue: "NeurIPS 2024 Datasets and Benchmarks Track"
link: https://arxiv.org/abs/2406.12384
code: https://github.com/lx709/VRSBench
category: rs-benchmark
era: recent
tags: [captioning, visual-grounding, vqa, human-verified, dota, dior, lora-finetune, gpt-4v-generated]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2406.12384 and https://github.com/lx709/VRSBench; 2026-10-14 full-text read via raw arXiv HTML (arxiv.org/html/2406.12384, v2 of 11 Nov 2024) converted to text (sections read: abstract, 1-7 incl. Tables 1-5, appendices A-G incl. Tables 6-7, GPT-4V prompts and human verification guidelines)"
takeaway: "Reference LoRA recipe and human-verified QA design, but VHR optical only and the best model grounds only 49.8% of referents at IoU 0.5 overall (57.4% for unique objects, 24.3% with oriented boxes), so masks need a dedicated segmenter"
---

# VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding

## Problem
Earlier remote sensing vision-language datasets tend to have short captions, one task each, automatically generated QA, little human checking, and grounding sets where many referents are the only object of their class (38.36% in DIOR-RSVG, per the paper).

## Approach
A semi-automatic pipeline: extract object attributes (class, box, position, size, uniqueness) from DOTA-v2 and DIOR detection labels; prompt GPT-4V with the image plus this object list to write a detailed caption, 1 to 5 unambiguous referring sentences and 3 to 10 QA pairs; regenerate up to five times if outputs contain phrases like "unknown"; then have human annotators verify and correct every image. Verification took about 120 s per image, 1,004 hours and about 6,200 USD in total, plus a second review of 2,000 images. Annotators were told to remove uncertain or ambiguous content and questions that contain their own answer.

## Data and benchmarks
- 29,614 images of 512x512 px (20,310 DOTA-v2 patches from train and val, 9,304 DIOR patches), 29,614 captions, 52,472 referring sentences, 123,221 QA pairs; 26 merged object classes.
- Split (Table 2): train 20,264 images, 36,313 refs, 85,813 QA; test 9,350 images, 16,159 refs, 37,408 QA.
- Captions average 52 words and 4 sentences (Fig. 3; the text says 54 words).
- VQA test set by type (Table 5): category 5,435; presence 7,789; quantity 6,374; color 3,550; shape 1,422; size 1,011; position 5,829; direction 477; scene 4,620; reasoning 902. Answers are a single word or short phrase.
- Yes/no balance is not reported anywhere in the paper.
- Licence: CC-BY-4.0 for the dataset (Appendix D); the README additionally restricts DOTA images to academic, non-commercial use.

## Key results
- Setup: all baselines (LLaVA-1.5, MiniGPT-v2, Mini-Gemini, GeoChat) use CLIP ViT-L/14 and Vicuna-7B, LoRA rank 64, 5 epochs, learning rate 2e-4 with cosine decay and 3% warm-up, batch 32 on 4 A100s; GPT-4V is evaluated zero-shot without object information.
- Captioning (Table 3): LLaVA-1.5 best, BLEU-1 48.1, BLEU-4 14.7, CIDEr 33.9; GPT-4V gets the highest LLM-judged score (0.83), which the authors note is judged by GPT-4 itself.
- Grounding, accuracy at IoU 0.5 (Table 4): GeoChat 49.8% overall (57.4% unique, 44.5% non-unique; 19.9% at IoU 0.7), LLaVA-1.5 41.6%, MiniGPT-v2 35.8%, Mini-Gemini 30.1%, GeoChat without fine-tuning 12.9%, GPT-4V 5.1%. With oriented boxes GeoChat drops to 24.3% (Table 7).
- VQA, GPT-4 judged (Table 5): Mini-Gemini 77.8%, LLaVA-1.5 76.4%, GeoChat 76.0%, GPT-4V 65.6%, GeoChat without fine-tuning 40.8%, MiniGPT-v2 38.2%. Quantity is the weakest type for every model (best 58.8%); presence is easiest (up to 92.1%).

## Limitations
Optical RGB only, very high resolution, no SAR or multispectral, no temporal or change questions (all listed as future work). Geographic diversity is limited to DOTA-v2 and DIOR. Annotations start from GPT-4V output, and VQA and caption scores rely on GPT-4 judging. Image licensing limits commercial reuse.

## What it means for EvidEO
- Use the LoRA recipe (rank 64, 5 epochs, lr 2e-4) as a reference starting point for any VLM fine-tune.
- Adopt the human-verification step for any Indian QA set we generate; a small verified set beats a large noisy one.
- Do not assume VRSBench scores transfer to 10 m Sentinel imagery; keep a separate Sentinel-based test split.
- Grounding below 50% overall (IoU 0.5) shows VLM boxes alone are unreliable; pair VLM answers with segmentation for the region mask we return.
- Note the design choice: VRSBench deletes questions without a definite answer, so it cannot test whether a model knows when not to answer. EvidEO's evaluation should keep such questions.

## Full-text check (2026-10-14)
- Changed: corrected the grounding headline. The 57.4% figure is for unique objects only; overall GeoChat accuracy at IoU 0.5 is 49.8% (Table 4), and the takeaway now says so. Added the pipeline and verification cost, source patch counts, train/test split, per-type VQA counts, training hyperparameters, GPT-4V results, oriented-box result and the dataset licence from the paper. Yes/no balance was checked and is not reported.
- Refusal and calibration: none. The construction rules remove uncertain or unanswerable questions, so every test item has a definite answer and no abstention is possible or scored. The seven "uncertain" hits are all annotation instructions, not evaluation.
