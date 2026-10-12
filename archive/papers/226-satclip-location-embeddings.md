---
id: 226
title: "SatCLIP: Global, General-Purpose Location Embeddings with Satellite Imagery"
authors: "Konstantin Klemmer, Esther Rolf, Caleb Robinson, Lester Mackey, Marc Rußwurm"
year: 2025
venue: "AAAI 2025 (AAAI Conference on Artificial Intelligence, ojs.aaai.org article 32457); arXiv:2311.17179 (v1 28 November 2023, v3 12 April 2024); Microsoft Research"
link: https://arxiv.org/abs/2311.17179
code: "github.com/microsoft/satclip (named on the Microsoft Research page; the repository page was not opened, HTTP 403 from the sandbox)"
category: eo-foundation
era: recent
tags: [location-encoder, contrastive-pretraining, sentinel-2, geographic-embeddings, name-collision]
verified: "2026-10-12 via WebSearch (AAAI OJS page, Microsoft Research page, mlanthology AAAI 2025 entry) and WebFetch of arxiv.org/abs/2311.17179 (title, five authors, dates, abstract); per-task numbers not extracted"
takeaway: "Prior art for the NAME, not the method: SatCLIP is Microsoft's contrastive location encoder (AAAI 2025). Our project was called SatClip until 2026-10-12, a collision we missed for nine runs; it is now renamed EvidEO. Methodologically unrelated, but useful as a location prior"
---

# Klemmer et al. 2025, SatCLIP

## Problem
Many prediction tasks depend on where something is (temperature, species, population). Existing location encoders are trained for single tasks or on limited data, so their embeddings transfer poorly across the globe.

## Approach
A location encoder (spherical harmonics with a small network) is trained contrastively against an image encoder (CNN or ViT) on openly available satellite imagery paired with coordinates, so that each latitude and longitude gets an embedding summarising what the place looks like.

## Data and benchmarks
Openly available satellite imagery sampled globally (Sentinel-2 based dataset, per the paper; the dataset name was not re-checked for this entry). Evaluated on nine location-dependent downstream tasks, including air temperature, animal recognition and population density.

## Key results
The authors report that SatCLIP embeddings beat other pretrained location encoders across the nine tasks and generalise better to regions far from training data. Per-task numbers were not extracted for this entry.

## Limitations
Embeddings describe a place in general, not a specific date, so they cannot answer "what happened here on this day". Not designed for SAR or for change.

## What it means for EvidEO
1. **Name collision.** This is the main reason for the entry. The project's working name "SatClip" collides with an established, widely cited AAAI paper and Microsoft repository. We renamed the project EvidEO on 2026-10-12. Lesson: check names against the literature with the same care as claims.
2. **Possible use.** A location embedding could serve as a prior for which regions need their own calibration offset (the South Asia over-confidence found in the paper draft), for example by clustering held-out events by embedding similarity. Not planned yet.
