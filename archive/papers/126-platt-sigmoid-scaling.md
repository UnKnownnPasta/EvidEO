---
id: 126
title: "Probabilities for SV Machines"
authors: "John C. Platt"
year: 2000
venue: "Chapter in Advances in Large-Margin Classifiers (eds. Smola, Bartlett, Schoelkopf, Schuurmans), MIT Press, 2000; widely cited as a 1999 technical report titled Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods"
link: https://doi.org/10.7551/mitpress/1113.003.0008
code: "none found (method is a two-parameter sigmoid fit; implemented in scikit-learn CalibratedClassifierCV method=sigmoid)"
category: trust-calibration
era: historical
tags: [platt-scaling, sigmoid-calibration, post-hoc-calibration, svm, score-to-probability]
verified: "2026-10-29 pages 1-5 of the 1999 preprint read as images; earlier 2026-10-07 via Crossref"
takeaway: "Platt scaling is the simplest way to turn a raw EvidEO score (for example a backscatter margin below the Otsu threshold) into a probability, and is the baseline any fancier calibrator must beat"
---

# Platt scaling, sigmoid calibration of classifier scores

## Problem
Support vector machines output an uncalibrated margin, not a probability. Downstream decisions (combining evidence, rejecting uncertain cases) need a posterior class probability.

## Approach
- Fit a two-parameter sigmoid, P(y=1 | f) = 1 / (1 + exp(A f + B)), mapping the SVM output f to a probability.
- Fit A and B by maximum likelihood on held-out data (or cross-validation folds), not on the training set, to avoid biased scores.
- Use slightly smoothed target labels instead of hard 0 and 1 to reduce overfitting when calibration data are few.
- Compare the resulting probabilities with kernel methods that directly optimize a regularized likelihood.

## Data and benchmarks
Benchmarked on several standard classification datasets of the period; the exact list was not confirmed here because the full text was not fetched.

## Key results
- A sigmoid fitted after training gives probabilities of quality comparable to regularized likelihood kernel methods, while keeping the SVM's sparsity and accuracy.
- Because the map is monotone, ranking and accuracy are unchanged; only the probability values move.

## Limitations
- The sigmoid shape is a strong assumption; if the score-to-probability curve is not sigmoidal, isotonic regression (entry 127) or binning (entry 128) can fit better.
- Binary by design; multiclass needs one-vs-rest or pairwise coupling.
- Assumes calibration data come from the same distribution as deployment data; under shift the fit degrades (entry 132).

## What it means for EvidEO
- EvidEO's instruments emit scores, not probabilities: the distance of a pixel's VV backscatter below a flood threshold, or the size of an NDVI drop. A per-tile Platt fit on labelled tiles (for example Sen1Floods11) turns that score into the probability that feeds the 0.60 abstention rule.
- Two parameters can be fitted from a small number of labelled Indian flood tiles, which matters when district-level labels are scarce.
- Fit separately per instrument and sensor mode (S1 VV, S1 VH, S2 NDVI), and record the fitted A and B with the scene ID so a confidence on any answer card is reproducible.

## Full-text check (2026-10-29)
Read the 1999 preprint of the same chapter ("Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods", March 1999, CiteSeerX copy; pages 1 to 5 viewed as images because the PDF text layer is garbled). The book chapter (Crossref record above) is the published form.
- Confirmed: the model is P(y=1|f) = 1/(1+exp(Af+B)), fitted by maximum likelihood (cross-entropy). Fitting on the same data used to train the SVM gives biased scores, so a hold-out set or cross-validation is needed. Our practice of fitting on a held-out split matches this.
- Platt's setting is a margin score from an SVM; EvidEO applies the same two-parameter sigmoid to its own quality score. Dataset names and the later experiments (pages 6 to 11) were not read.
