---
id: 022
title: "Sen1Floods11: A Georeferenced Dataset to Train and Test Deep Learning Flood Algorithms for Sentinel-1"
authors: "Derrick Bonafilia, Beth Tellman, Tyler Anderson, Erica Issenberg"
year: 2020
venue: "CVPR Workshops 2020 (pp. 210-211)"
link: https://openaccess.thecvf.com/content_CVPRW_2020/html/w11/Bonafilia_Sen1Floods11_A_Georeferenced_Dataset_to_Train_and_Test_Deep_Learning_CVPRW_2020_paper.html
code: https://github.com/cloudtostreet/Sen1Floods11
category: sar-optical-fusion
era: recent
tags: [sentinel-1, sentinel-2, flood-mapping, segmentation, weak-labels, dataset, south-asia]
verified: "2026-10-29 full text of PDF; earlier 2026-10-04 via CVF PDF"
takeaway: "Standard Sentinel-1 flood baseline (11 events, 68 hand-labelled chips in India); EvidEO fits its water calibration on it (run 6), and the Indian chips show VV-only thresholds miss much of the labelled flood, so VH matters"
---

# Sen1Floods11: A Georeferenced Dataset to Train and Test Deep Learning Flood Algorithms for Sentinel-1

## Problem
Radar sees floods through cloud, but deep learning flood mappers lacked a public, georeferenced, globally varied training and test set, and it was unclear whether cheap automatic labels could replace costly hand labels.

## Approach
The authors build paired Sentinel-1 and Sentinel-2 chips at 10 m and train a fully convolutional network (ResNet50 backbone) on four label sources: hand labels, Sentinel-1 derived weak labels, Sentinel-2 derived weak labels and permanent water from Landsat. They compare against an Otsu threshold on VH backscatter.

## Data and benchmarks
4,831 chips of 512 x 512 pixels covering about 120,406 km2 across 11 flood events on six continents: 446 hand labeled and 4,385 weakly labeled. Correction (run 6): the hand-labelled chip names and split files in the public bucket (v1.1) show the 11 events as Bolivia, Ghana, India, Mekong, Nigeria, Pakistan, Paraguay, Somalia, Spain, Sri Lanka and USA; India has 68 hand-labelled chips (40 train, 14 valid, 14 test). An earlier version of this entry listed a different set of countries and said India was absent; that was wrong. Bolivia is held out entirely to test generalisation. Data is about 14 GB on a public Google Cloud bucket.

## Key results
Mean IoU for water on the hand-labeled test set (10 events): Sentinel-2 weak labels scored best for flood water (0.339) and all water (0.408), while Otsu VH thresholding scored best on permanent water (0.457). On the unseen Bolivia event, Sentinel-1 weak labels led on all water (0.387), with Otsu very close (0.386). Hand labels did not beat weak labels in either table.

## Limitations
Only 11 events, no urban floods in validation, minimal hyperparameter tuning, and the authors frame results as preliminary. Absolute IoU values are modest, and simple thresholding remains competitive.

## What it means for EvidEO
- Use Sen1Floods11 as a standard SAR flood baseline. Its 68 Indian hand-labelled chips are EvidEO's first Indian calibration check (run 6: training/calibration/reports/sar_water_otsu.md); still build a larger Indian test set (Assam, Bihar, Kerala).
- Keep an Otsu VH threshold as a transparent fallback and sanity check; if our model disagrees strongly, lower confidence or abstain.
- Weak labels from Sentinel-2 can scale training cheaply; adopt that for India where cloud-free optical pairs exist.
- Report IoU on a geographically held-out event, as they did with Bolivia, to avoid overstating accuracy to officials.
- Ship flood masks with scene ID and date per chip, mirroring their georeferenced design.

## Full-text check (2026-10-29)
Read the full PDF text from the CVF open-access site (main text, tables and references).
- Confirmed: 4,831 chips, 120,406 km2, 446 hand-labelled; Table 1 (10 events) Otsu-VH 0.4571 permanent, 0.2850 flood, 0.3591 all water; Sentinel-2 weak 0.3389 flood and 0.4084 all; Table 2 (Bolivia) Sentinel-1 weak 0.3871 and Otsu 0.3862 all water. The draft table (0.359 and 0.386) matches.
- The hand labels are Sentinel-2 maps (same day or within 2 days) corrected by analysts, so the reference is optical-derived, not a ground survey. The Otsu baseline is the same family as our instrument, but it smooths VH with a focal mean (a despeckle step we do not have) and runs on 1 km blocks chosen by variance.
- The text says 4,370 weak chips in the introduction and 4,385 in Section 2; 4,831 minus 446 is 4,385, so 4,370 is a typo. The paper cites Otsu as Automatica 1975; the correct source is IEEE SMC 1979.
- Event countries are given in Fig. 3 (image) and were not read; the India chip count comes from the public bucket, as the entry already says.
