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
tags: [captioning, visual-grounding, vqa, human-verified, dota, dior, lora-finetune]
verified: "2026-10-29 full text of arXiv PDF; earlier 2026-10-04 via arXiv and GitHub"
takeaway: "Reference LoRA recipe and human-verified QA design, but VHR optical only and grounding about 57% at IoU 0.5, so masks need a dedicated segmenter"
---

# VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding

## Problem
Earlier remote sensing vision-language datasets tend to have short captions, a single task each, and limited human checking. That makes it hard to train and compare general remote sensing VLMs on several tasks at once.

## Approach
The authors build one dataset that supports captioning, visual grounding and VQA on the same images. Annotations are produced with model assistance and then verified by humans, giving detailed captions, object references with boxes, and diverse question/answer pairs.

## Data and benchmarks
- 29,614 images, 29,614 human-verified detailed captions, 52,472 object references, 123,221 QA pairs (from the abstract).
- Images come from the DOTA-v2 and DIOR object detection datasets (very high resolution optical aerial and satellite imagery).
- VQA categories include presence, quantity, color, shape and reasoning.
- Text annotations are CC-BY-4.0; DOTA images are restricted to academic, non-commercial use (per the README).

## Key results
From the paper (Tables 3 to 5; earlier from the README): the open baselines (LLaVA-1.5, MiniGPT-v2, Mini-Gemini, GeoChat) were fine-tuned (LoRA rank 64, 5 epochs per the README); GPT-4V and GeoChat without fine-tuning were not. LLaVA-1.5 led captioning with BLEU-4 of 14.7; GeoChat led grounding with 57.4% accuracy at IoU 0.5 on unique objects; Mini-Gemini led VQA at 77.8%. Other per-metric numbers were not checked.

## Limitations
Optical only, very high resolution, and no SAR or multispectral bands, so it does not match Sentinel-1/2 scale. No temporal or change questions. Image licensing limits commercial reuse. Grounding scores remain modest, showing localization is still hard.

## What it means for EvidEO
- Use the LoRA recipe in the README (rank 64, short schedule) as a reference starting point for our planned VLM fine-tune.
- Adopt the human-verification step for any Indian QA set we generate; a small verified set beats a large noisy one for evaluation.
- Do not assume VRSBench scores transfer to 10 m Sentinel-2 imagery; keep a separate Sentinel-based test split.
- Grounding at about 57% (IoU 0.5) shows region masks from a VLM alone are unreliable; pair VLM answers with segmentation or detection for the region mask we return.
- Check licenses before mixing DOTA-derived data into anything beyond the academic prototype.

## Full-text check (2026-10-29)
Read the full arXiv PDF text.
- Confirmed: 29,614 images, 52,472 referring sentences, 123,221 QA pairs; LLaVA-1.5 BLEU-4 14.7; GeoChat grounding 57.4 (unique) and 49.8 (all) at IoU 0.5; Mini-Gemini VQA 77.8 overall.
- Quantity questions stay hard after fine-tuning (best 58.8, GPT-4V 45.6); presence is about 92. GPT-4V grounding is 5.1 overall without object hints.
- Annotations were drafted by GPT-4V, then checked by humans (1,004 hours, 6,200 USD); the paper admits GPT-4V hallucinates. The VQA scorer and the CHAIR caption metric use GPT-4 as judge.
