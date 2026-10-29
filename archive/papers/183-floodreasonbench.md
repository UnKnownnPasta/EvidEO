---
id: 183
title: "FloodReasonBench: Benchmarking VLM Reasoning Segmentation for Embodied Flood Response at the Edge"
authors: "Rajat Bhattacharjya, Yoomee Jung, Minwoo Kim, Sing-Yao Wu, Eli Bozorgzadeh, Nalini Venkatasubramanian, Nikil Dutt"
year: 2026
venue: "arXiv preprint (arXiv:2608.15410, v1 15 August 2026); under review per the arXiv comment"
link: https://arxiv.org/abs/2608.15410
code: "Not yet released; code and dataset promised upon acceptance"
category: upcoming
era: upcoming
tags: [flood, reasoning-segmentation, lisa, mobilesam, lora, edge, jetson, split-computing, uav, benchmark]
read_depth: "full"
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract, comment) and https://arxiv.org/html/2608.15410 (introduction, dataset curation, split-inference design); WebFetch permission request timed out; 2026-10-14 full-text read via curl of https://arxiv.org/html/2608.15410 converted to text (sections read: I to VI, Tables I to III, Figures 1 to 6 captions; the paper has no appendix); the source of the flood images is not named anywhere in the paper"
takeaway: "Short UC Irvine flood benchmark where a responder's text request returns a pixel mask (people, buildings, vehicles); flood fine-tuning lifts LISA-7B from 0.72 to 0.84 gIoU and only the MobileSAM encoder prefix is profiled on a Jetson, with the language model running remotely; a useful quality-floor operating-point pattern for EvidEO, but close-range imagery, 100 test samples and no satellite or offline full pipeline"
---

# Bhattacharjya et al. 2026, FloodReasonBench

## Problem
Flood responders want to ask a drone or robot in words (for example, find partly submerged vehicles) and get the matching pixels back. Generic reasoning-segmentation benchmarks do not reflect flood scenes, the heavy SAM encoder is costly on embedded hardware, and sending everything to a server needs bandwidth and connectivity.

## Approach
- FloodResponseSeg (Section II-A): collect real-world flood images (source not named), filter with CLIP, inspect manually, localise targets with Grounding DINO, make masks with SAM2, reject poor masks by eye, then hand-write one or more responder-style queries per target.
- Model (Sections III-A, IV-A): LISA-7B with the SAM ViT-H encoder replaced by MobileSAM (TinyViT, frozen); the language and segmentation parts are fine-tuned on flood data (learning rate 1e-4, effective batch 4).
- Split computing (Section III-B, III-C): the TinyViT backbone can be cut after any of its 12 blocks; the edge device runs the prefix, a per-cut autoencoder (trained on ADE20K, compression ratio 0.1 by default) compresses the feature, and a remote server finishes the backbone, the CLIP branch, the LLM and the mask decoder. Split-aware flood adaptation then fine-tunes the downstream parts with the compression in the loop.
- Systems study (Section IV-C): edge-side latency, power, energy per frame and transmitted bytes on an NVIDIA Jetson AGX Xavier, FP16, 1024 by 1024 input, across power modes (MAXN, 10 W, 15 W, several 30 W modes). Given a user-set minimum gIoU, the benchmark lists the feasible cuts and their costs.

## Data and benchmarks
Three target classes (people, buildings, vehicles). 532 annotated training samples (189 people, 209 buildings, 134 vehicles), expanded to 2,128 with three photometric variants each; 100 un-augmented evaluation samples (48, 24, 28) (Table I). Metrics gIoU (primary) and cIoU plus latency, energy and transmitted size. The 200-sample ReasonSeg validation set is used for the pre-adaptation partition study.

## Key results
- Table II: off-the-shelf LISA-SAM on the flood set scores 0.7223 gIoU and 0.7385 cIoU; after flood fine-tuning 0.8423 and 0.9013. LISA-MobileSAM after fine-tuning: 0.8202 and 0.8572. The earlier SAM split design (AVERY) scores 0.8081 to 0.8240 gIoU across compression ratios.
- Partition sensitivity (Section V-B, Figure 4): before adaptation on ReasonSeg, gIoU across the 12 cuts spans 0.5322 to 0.7146; after split-aware flood adaptation it spans only 0.7599 to 0.8025.
- Operating point (Section V-C): with a 0.79 gIoU floor, Block 1 qualifies at 0.7941 gIoU, 50.1 ms, 0.461 J per frame and 0.125 MiB sent (30 W mode); against the best cut (Block 9) it gives up 0.84 gIoU points but cuts latency by 50.5%, energy by 54.8% and bytes sent by 50%. A 0.80 floor leaves only Block 9. At 10 W, Block 1 takes 142.8 ms and 0.947 J.
- Compressed feature size is non-monotonic in depth: 0.750 MiB at MB1, 0.125 MiB at Blocks 1 to 6, 0.250 MiB at Blocks 7 to 9 (Table III).

## Limitations
- Close-range or UAV-style flood imagery; not satellite, not SAR, and not flood extent mapping. Image source not stated.
- Very small test set (100 samples) and three classes; masks come from Grounding DINO and SAM2 with manual rejection.
- Only the encoder prefix runs on the Jetson; the 7B language model and decoder run remotely, so the full answer path is not edge-only or offline.
- No confidence, calibration or abstention; data and code not yet public. Authors' future work: more entities, newer models and platforms, closed-loop execution under varying networks.

## What it means for EvidEO
- Adopt: the quality-constrained operating-point idea (pick the cheapest configuration that still meets a stated accuracy floor) fits EvidEO's offline laptop target; apply it to choosing quantisation level and instrument resolution.
- Adopt: evidence that a small in-domain set (hundreds of samples) moves a VLM a lot, supporting EvidEO's small LoRA parser.
- Watch: if released, its responder-style queries are a source of realistic flood phrasing for EvidEO's intent tests; it does not compete with EvidEO's satellite-scale flood extent answers.

## Full-text check (2026-10-14)
Ingredient verdicts for the paper's own pipeline:
- C1 calibrated per-answer confidence: No. Only gIoU and cIoU over the test set (Table II).
- C2 threshold abstention with next step: No. The gIoU floor selects hardware configurations, not answers; the model never declines.
- C3 scene receipts that reproduce: No. No scene metadata, provenance or re-run test.
- C4 SAR chosen automatically under cloud: No. Single optical camera images only.
- C5 CPU or offline: part. Edge-side encoder prefix measured on a Jetson AGX Xavier GPU (Section IV-C, Figure 5); the LLM and decoder run on a remote server, so the full path needs a network link and a GPU server. No CPU-only run (the "CPU" hits refer to Jetson CPU-core power modes).
- C6 plain-language questions for non-experts: part. Hand-written responder requests in everyday language (Section II-A), but no user study and the audience is operators of the platform.
Corrections to the earlier entry: the edge measurement covers only the vision-encoder prefix, not the full model (the entry implied an edge deployment of the whole pipeline); the base model is LISA-7B; the MobileSAM backbone is frozen during fine-tuning; the image source is confirmed as unstated in the full text, not just in the parts read before.
Novelty: at most partial C5 and C6, so it does not threaten EvidEO's "no more than two" claim; it also shows that even edge-focused flood VLM work keeps the language model off-device, which supports EvidEO's emphasis on a fully local answer path.
