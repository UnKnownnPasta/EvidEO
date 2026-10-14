---
id: 011
title: "RSVQA: Visual Question Answering for Remote Sensing Data"
authors: "Sylvain Lobry, Diego Marcos, Jesse Murray, Devis Tuia"
year: 2020
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS) 58(12):8555-8566, DOI 10.1109/TGRS.2020.2988782"
link: https://arxiv.org/abs/2003.07333
code: https://github.com/syvlo/RSVQA
category: rs-benchmark
era: recent
tags: [vqa, sentinel-2, openstreetmap, auto-generated-qa, counting, presence, language-bias]
read_depth: "full"
verified: "2026-10-04 via https://arxiv.org/abs/2003.07333 and https://rsvqa.sylvainlobry.com/; 2026-10-14 full-text read via arXiv PDF (arxiv.org/pdf/2003.07333, v2 pre-acceptance version) with pdftotext -layout (sections read: abstract, I introduction, II datasets incl. method, data, discussion and Table I, III model, IV results incl. Tables II-III, language-bias and training-size analyses, V conclusion)"
takeaway: "Sentinel-2 VQA baseline to evaluate on first; copy OSM-template QA generation and always run a blind (random-image) baseline, which here still scored 73.8% against 79.1% with the real image"
---

# RSVQA: Visual Question Answering for Remote Sensing Data

## Problem
Extracting information from satellite imagery usually needs task-specific models and expert knowledge. The authors propose visual question answering as a generic interface, so any user can ask a natural-language question about an image.

## Approach
Questions and answers are generated automatically from OpenStreetMap: pick an element (road, water area, commercial or residential building, land-use class), optionally add a shape or size attribute and a relative position ("left of", "next to" within 1,000 m, and so on), then fill a template for one of five question types. Answers are computed from the OSM objects in the image footprint. The baseline encodes the image with an ImageNet ResNet-152 (to 1,200 features) and the question with a Skip-thoughts RNN (2,400 to 1,200), fuses them by point-wise multiplication after tanh, and classifies over a fixed answer set with an MLP (one hidden layer of 256). Trained with Adam at 1e-5 (150 epochs LR, 35 epochs HR); results are means of 3 runs.

## Data and benchmarks
- Low resolution (LR): 9 Sentinel-2 tiles over the Netherlands, RGB at 10 m, cut into 772 images of 256x256 px (6.55 km² each); 77,232 QA pairs; tile-level split 77.8 / 11.1 / 11.1%. Question types: count, presence, comparison, rural/urban. Counts are quantised into 5 bins (0, 1-10, 11-100, 101-1000, over 1000), giving 9 possible answers.
- High resolution (HR): 161 USGS orthophoto tiles from the US north-east, cut into 10,659 images of 512x512 px (about 5,898 m² each); 1,066,316 QA pairs; split 61.5% train, 11.2% validation, 20.5% test set 1 (same regions), 6.8% test set 2 (Philadelphia, unseen city and a different sensor). Types: count (exact, 0 to 89), presence, comparison, area (quantised). 98 possible answers. Test set 1 has 316,941 questions.
- Answer balance: in LR, "yes" is 34.9% and "no" 34.3% of answers; in HR, "no" is the most common answer (37.7%) and 60.9% of area answers are 0 m².
- The PDF text extraction garbles digit grouping in the size sentences; the counts above match those cited for RSVQA by VRSBench (Table 1) and RSHallu (section 7.7.1). The paper gives HR resolution as 15 cm in section II-B but 30 cm in the conclusion.

## Key results
- LR test (Table II): count 67.01%, presence 87.46%, comparison 81.50%, rural/urban 90.00%, average accuracy 81.49%, overall accuracy 79.08%.
- HR test set 1 (Table III): count 68.63%, presence 90.43%, comparison 88.19%, area 85.24%, AA 83.12%, OA 83.23%.
- HR test set 2, Philadelphia: count 61.47%, presence 86.26%, comparison 85.94%, area 76.33%, AA 77.50%, OA 78.23%.
- Language bias: with a random test image per question, OA is still 73.78% (LR), 73.78% (HR test 1) and 72.51% (HR test 2).
- Training on 1% of HR training data already gives 65% AA, and gains plateau after 10%.
- Relative-position questions are handled poorly; counting suffers when touching buildings are separate OSM objects.

## Limitations
OSM labels are incomplete or misregistered and cannot be date-matched to the imagery, so ground truth is noisy. Templates limit linguistic diversity and cover only static OSM objects. Counting is treated as classification. The drop on the unseen city shows weak geographic transfer. No calibration, confidence or abstention.

## What it means for EvidEO
- RSVQA-LR is one of the few public VQA sets on Sentinel-2, so it is a natural first evaluation for any optical VQA path.
- Adopt the OSM-to-template idea to auto-generate Indian question sets (OSM plus Bhuvan layers).
- Always run a blind-image baseline: here a random image costs only about 5 points of accuracy, so most of the score comes from the question.
- Do not answer counts from 10 m imagery as exact; route counts through detection with uncertainty or abstain.
- Report per-question-type accuracy and a held-out-region split, not a single headline number.

## Full-text check (2026-10-14)
- Changed: corrected the question types per dataset (rural/urban only in LR, area only in HR), added the LR tile count and quantisation, HR split percentages and test-set sizes, answer balance, model and training details, all per-type accuracies with table numbers, the HR test-2 blind score, and the training-size result. Noted the 15 cm versus 30 cm inconsistency and the PDF digit-grouping artefact. Earlier approximate numbers (79.1, 83.2, 78.2, 73.8) are confirmed.
- Refusal and calibration: none. The model always picks an answer from a closed set; no confidence, calibration or abstention is measured. None of the search terms (calibrat, ECE, abstain, refus, reject, confidence, uncertain, unanswerable) occur in the text.
