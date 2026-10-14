---
id: 041
title: "Kuro Siwo: 33 billion m² under the water. A global multi-temporal satellite dataset for rapid flood mapping"
authors: "Nikolaos Ioannis Bountos, Maria Sdraka, Angelos Zavras, Andreas Karavias, Ilektra Karasante, Themistocles Herekakis, Angeliki Thanasou, Dimitrios Michail, Ioannis Papoutsis"
year: 2024
venue: "NeurIPS 2024 Datasets and Benchmarks Track (Advances in Neural Information Processing Systems, vol. 37)"
link: https://arxiv.org/abs/2311.12056
code: https://github.com/Orion-AI-Lab/KuroSiwo
category: change-detection
era: recent
tags: [sentinel-1, sar, flood, multi-temporal, pre-post-event, dataset, grd, slc, copernicus-ems, calibration-set]
read_depth: "full"
verified: "2026-10-04 via https://github.com/Orion-AI-Lab/KuroSiwo; 2026-10-14 full-text read via raw arXiv HTML (arxiv.org/html/2311.12056, v3 of 1 Nov 2024) converted to text, plus the GitHub README licence line (sections read: abstract, 1-6 incl. Tables 1-2 and limitations, supplementary 1-10 incl. annotation process, training setup, SLC Table 3, licence and maintenance)"
takeaway: "Expert-relabelled Sentinel-1 pre/pre/post flood set (43 events 2015 to 2022, 67,490 labelled 224x224 time series, three classes separating flood from permanent water, event-held-out test split); the best calibration set for EvidEO's SAR change instrument, though about half its events are European and the paper gives no per-event list"
---

# Kuro Siwo: 33 billion m² under the water. A global multi-temporal satellite dataset for rapid flood mapping

## Problem
Deep learning for SAR flood mapping lacks large, carefully annotated, multi-temporal Sentinel-1 datasets. Many existing sets use only a post-event image, automatic or semi-automatic labels, or Copernicus EMS (CEMS) rapid-mapping polygons drawn under time pressure by different teams, and several shuffle samples from the same event across splits.

## Approach
- For each of 43 flood events, a triplet of Sentinel-1 acquisitions: two pre-event images at varying lags and one post-event image as close to the event as possible (post-event gap mean 3.6 days, s.d. 6.07, median 1 day). All three come from the same pass direction (ascending or descending). VV and VH, 10 m.
- Two products: GRD processed in SNAP (orbit, thermal and border noise removal, calibration, speckle filtering, terrain correction with SRTM 1 arcsec) and minimally processed SLC with phase and amplitude.
- Labels: five SAR experts photo-interpreted the GRD images at 1:1000 into No Water, Permanent Waters and Floods, starting from CEMS shapefiles when available and from scratch otherwise; each annotator quality-checked another's part under a senior supervisor. In a French example, CEMS and Kuro Siwo agree with IoU of only 51% (permanent water) and 48% (flood); models trained on raw CEMS labels stayed below 70% on all metrics.
- BlackBench: U-Net, DeepLabv3, UPerNet (ResNet, Swin, ConvNeXt), change-detection models (FC-EF-Diff, FC-EF-Conc, SNUNet-CD, Changeformer), ConvLSTM, and an MAE-pretrained ViT (FloodViT) on the unlabelled set. Inputs vary in number of pre-event images and in DEM or slope channels.

## Data and benchmarks
- Labelled: 67,490 time series, 202,470 SAR samples as 224x224 tiles, with DEM and metadata (climate zone, AOI, dates). Coverage over 338 billion m², of which 33 billion m² is flood or permanent water.
- Unlabelled: 533,847 time series, 1,601,511 SAR samples (Table 1 lists 466,357 unlabelled samples, which does not match the text).
- 43 events across six continents and three climate zones; 10 events held out entirely for testing.
- About 1.33 TB compressed (GRD about 706 GB, SLC about 493 GB).
- Licence conflict: the paper says the dataset and BlackBench are MIT licensed (section 3 and supplementary section 9), while the GitHub README says CC BY. Check before redistributing.
- South Asia: the paper has no per-event table. Sample figures include Sri Lanka and Nepal patches; Pakistan appears only as motivation, and India is not named. The paper says most events are European but Asian events contribute more samples, because Asian floods are larger.

## Key results
- Best GRD model (Table 2): UNet-ResNet50 with all three images, F1 flood 80.12%, F1 permanent water 78.24%, mIoU 76.20%, F1 for merged water 83.85%.
- Change-detection architectures do worse than segmentation models fed the stacked series: SNUNet-CD F1 flood 74.26%, Changeformer 76.96%, FC-EF-Diff only 10.93% F1 on permanent water.
- Using all pre-event images helps most models; adding DEM or slope gives negligible gains.
- FloodViT with a frozen encoder is comparable to most supervised models and beats all change-detection methods.
- SLC (Supplementary Table 3): best water F1 79.94% (UNet-ResNet18), flood F1 71.20%.
- Per-event analysis: permanent-water scores drop sharply for Honduras and Australia, where flood and river boundaries overlap.

## Limitations
- From the paper: about half of events are in Europe; a single post-event image may miss peak extent given revisit; speckle, forests and complex terrain, wind roughening, flooded vegetation (C-band does not penetrate dense canopy) and urban double bounce all remain hard.
- No threshold or classical baseline is reported, so it does not tell us how a split-based threshold compares.
- The authors chose not to supply a static permanent-water layer, arguing it can add noise.

## What it means for EvidEO
- Make Kuro Siwo the primary calibration set for the Sentinel-1 water change instrument, using its flood class as positives and permanent water as a separate class.
- Copy its input design: at least two pre-event scenes from the same pass direction, which the paper's results favour over a single pre image.
- Its three-class labels match what EvidEO must report: "newly flooded" must exclude permanent water.
- Group any cross-validation by event, as the paper's event-held-out split does; random chip splits leak.
- Because the paper does not list events, derive the event list from the released metadata before claiming South Asian coverage; abstain or lower confidence in flooded-vegetation and dense-urban areas.

## Full-text check (2026-10-14)
- Changed: added sample counts (67,490 labelled series, 202,470 samples; unlabelled 533,847 series), annotation protocol, triplet timing, same-pass constraint, preprocessing, the 10-event held-out test, CEMS disagreement figures, change-detection and SLC results, and dataset size. Corrected the licence (paper says MIT, README says CC BY). Corrected "Asia is underrepresented": Asia has fewer events but more samples than Europe, and the paper names only Sri Lanka and Nepal patches, not India. Confirmed best-model numbers (80.12 / 78.24 / 76.20, Table 2).
- Refusal and calibration: not applicable to a segmentation dataset, and none is measured. The only "calibration" hit is SAR radiometric calibration in preprocessing. No uncertainty or confidence outputs are evaluated.
