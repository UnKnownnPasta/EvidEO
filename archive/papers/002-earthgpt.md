---
id: 002
title: "EarthGPT: A Universal Multi-modal Large Language Model for Multi-sensor Image Comprehension in Remote Sensing Domain"
authors: "Wei Zhang, Miaoxin Cai, Tong Zhang, Yin Zhuang, Xuerui Mao"
year: 2024
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), vol. 62, pp. 1-20, 2024; DOI 10.1109/TGRS.2024.3409624 (Crossref record title: 'EarthGPT: A Universal Multimodal Large Language Model for Multisensor Image Comprehension in Remote Sensing Domain')"
link: https://arxiv.org/abs/2401.16822
code: https://github.com/wivizhang/EarthGPT
category: rs-vlm
era: recent
tags: [vlm, multi-sensor, sar, infrared, optical, instruction-tuning, mmrs-1m, llama2]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2401.16822 and https://github.com/wivizhang/EarthGPT; 2026-10-14 full-text read via curl of https://arxiv.org/html/2401.16822 (v3, 8 March 2024) converted to plain text, plus Crossref API query for the DOI (sections read: abstract, I to VII in full, Tables I to IX, Figs. 4 to 6 captions and text; keyword grep for calibration, abstention, provenance, SAR, cloud, CPU and plain-language terms)"
takeaway: "MMRS-1M (optical, SAR, infrared; SAR is only about 1% of it) is a ready seed for LoRA data, but EarthGPT reports no quantitative SAR result, so it is evidence of SAR input support, not of SAR accuracy"
---

# EarthGPT: A Universal Multi-modal Large Language Model for Multi-sensor Image Comprehension in Remote Sensing Domain

## Problem
Multimodal LLMs work well on natural photos but remote sensing differs strongly, and earlier RS assistants (RSGPT, GeoChat) were optical only or needed per-task tuning. Analysts also need SAR and infrared, and one model that covers many interpretation tasks across sensors.

## Approach
EarthGPT (Beijing Institute of Technology) has three parts (Sec. III, V-A):
- Visual-enhanced perception: multi-layer features from a frozen DINOv2 ViT-L/14 are concatenated with multi-scale features from a frozen CLIP ConvNeXt-L, then projected to the language space.
- Cross-modal mutual comprehension: LLaMA-2's self-attention and RMSNorm layers are unfrozen and trained on natural image-text data (LAION-400M, COCO Caption).
- Unified instruction tuning: those weights are frozen and new bias and scale parameters in the linear layers (LLaMA-Adapter V2 style bias tuning) are trained on MMRS-1M, with every task phrased as an instruction.
Detection outputs are text boxes in horizontal (HBB) or oriented (OBB) form.

## Data and benchmarks
MMRS-1M: 34 existing RS datasets converted to instructions (Table I), summing to about 1.006M samples. Captioning 5 datasets, VQA 4 (FloodNet, RSVQA-LR, RSIVQA, CRSVQA), classification 7, detection 17, visual grounding and region captioning from DIOR-RSVG. SAR comes only from three ship-detection sets (AIR-SARShip-2.0, SSDD, HRSID; about 10.6k samples, roughly 1%), infrared from six detection sets (about 87k). The paper itself notes SAR and infrared data are limited relative to optical (Sec. VI-B). Evaluations: NWPU-RESISC45 (supervised), CLRS and NaSC-TG2 (zero-shot), NWPU-Captions, CRSVQA (supervised), RSVQA-HR test 2 (zero-shot, count omitted), DIOR-RSVG, and MAR20 aircraft detection (zero-shot HBB and OBB).

## Key results
- Zero-shot classification: 77.37% CLRS, 74.72% NaSC-TG2 (Table III); supervised NWPU-RESISC45 93.84% (Table II).
- NWPU-Captions: BLEU-4 65.5, CIDEr 192.6 (Table IV).
- CRSVQA OA 82.00 (Table V); RSVQA-HR zero-shot presence 62.77, comparison 79.53, OA 72.06 (Table VI; text says 72.05), just below GeoChat's 72.30.
- DIOR-RSVG: Pr@0.5 76.65, mIoU 69.34, cIoU 81.54 (Table VII).
- MAR20 zero-shot HBB AP@50 90.11 vs 88.21 for GroundingDINO (Table VIII); OBB AP@50 87.86, below DOTA-trained specialists at about 90 (Table IX). For these detection scores a RemoteCLIP score is used as the confidence for ranking boxes, because the MLLM emits none (Sec. V-F).
- SAR and infrared: qualitative examples only (Fig. 4, Sec. VI-B); no SAR metric is reported anywhere.

## Limitations
The only stated future work is better OBB detection and more modalities (Sec. VII); the earlier entry's claim that the paper acknowledges pixel-level localization difficulty is not in the text. From the results: SAR capability is shown only by examples, and SAR training data is ship detection chips, not Sentinel-1 GRD scenes, so transfer to raw Sentinel-1 is untested. Table VI's Qwen-VL-Chat and LLaVA-1.5 rows are swapped relative to GeoChat's own Table 8 (a reporting slip). No calibrated confidence or abstention. Released model weights were not clearly stated in the repo (from the earlier repo check, not re-verified).

## What it means for EvidEO
- MMRS-1M is a source of optical, infrared and a small amount of SAR instruction pairs for our LoRA fine-tune (check per-source licences first); expect to add our own Sentinel-1 flood pairs because its SAR is ships only.
- Its dual-encoder fusion (ViT plus CNN) is heavier than our CPU budget allows; adopt the lesson (multi-scale features help small objects) via tiling, not via a second encoder.
- Cite it as evidence that one assistant can accept SAR and optical, but not as evidence of SAR accuracy.
- The MAR20 trick (scoring LLM boxes with a CLIP similarity because the LLM gives no confidence) shows the community already patches missing confidence with an external score; EvidEO's calibrated score is the principled version.
- Report NaSC-TG2 or CLRS zero-shot accuracy for RemoteCLIP alongside EarthGPT's numbers if we claim classification quality.

## Full-text check (2026-10-14)
Ingredients (EarthGPT's own system as built and evaluated):
- C1 calibrated per-answer confidence: No. The paper states MLLMs do not predict confidence scores and borrows a RemoteCLIP score only to rank detection boxes for AP (Sec. V-F); it is not calibrated or shown to users.
- C2 threshold abstention with next step: No.
- C3 scene receipts that reproduce: No. Dataset chips only; no scene IDs, dates or re-run checks.
- C4 SAR chosen automatically under cloud: No. SAR images are accepted as input when supplied; there is no sensor choice and no cloud handling.
- C5 CPU or offline: No. LLaMA-2 7B with two large frozen vision encoders; no CPU or quantised inference reported.
- C6 plain-language questions for non-experts: part. Language-instruction dialogue and multi-turn use (Fig. 6, Sec. VI-A) are claimed to be more user-friendly, but prompts are templated and no non-expert evaluation exists.

Open items resolved: DOI is 10.1109/TGRS.2024.3409624 (TGRS vol. 62, 2024, pp. 1-20, via Crossref). EarthGPT is not the "unified multimodal LLM for cross-sensor EO evaluated on SAR and BigEarthNet": it has no BigEarthNet evaluation and no quantitative SAR evaluation. That description fits EarthDial (entry 003: BigEarthNet in Tables 4 and 5, SAR ship detection in Table 5).

Corrections to the abstract-level entry: removed the unsupported "pixel-level localization" limitation; added that SAR is about 1% of MMRS-1M and ships only; added all quantitative results with table refs; added venue volume, pages and DOI.

Novelty impact: none. 0 Yes, 1 part; no threat to the "no more than two" claim.
