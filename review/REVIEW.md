# Answering with evidence: a narrative review of trustworthy, language-driven Earth observation, with flood mapping as the test case

**Type:** narrative review (non-systematic), written to the SANRA quality criteria and the narrative-review guidance of Green et al.; flow reporting borrowed from PRISMA 2020 where it fits (see Section 2 and Appendix A).
**Date of search and writing:** 2026-11-06
**Status:** draft for the team. Not peer reviewed. Several cited sources were read at abstract level only; each is marked (see the evidence tags below).
**Competing interest, stated up front:** the authors of the EvidEO project (Team Stardust, RVITM) commissioned this review and the project is one of the systems discussed. Its own results are labelled "EvidEO, own result" and are never used to support a general claim without independent evidence beside them.

---

## Abstract

**Background.** Vision-language models and tool-using agents now let people ask plain-language questions about satellite imagery. Whether those answers can be trusted by the people who act on them, for example a district disaster officer asking how much land is flooded, depends on more than the language model.

**Aim.** To review, across language interfaces, measurement, uncertainty and human use, what is known about making language-driven Earth observation (EO) answers trustworthy, using flood mapping with Sentinel-1 radar as the test case, and to identify where the evidence is thin.

**Methods.** Narrative review. We started from a 227-paper annotated project archive and added a targeted literature search on 2026-11-06 for areas the archive covered weakly (conformal uncertainty for flood maps, verbalised confidence, provenance, Indian validation studies). Five new primary sources were verified against their publisher or preprint pages and are marked by evidence level.

**Findings.** (1) Language models are the weakest link for numbers: expert-judged hallucination-free rates for remote-sensing (RS) models range from 36% to 69%, and localisation scores are low. (2) Agents that call tools raise answer accuracy but are scored on correctness only; one benchmark shows reflection raising accuracy while wrong answers also rise. (3) Radar flood measurement has well-documented blind spots (built-up areas, tree cover) and the reference maps used to score it disagree on definitions. (4) Calibration, conformal risk control and out-of-distribution abstention exist for flood segmentation, but are evaluated at pixel level, mostly inside the training distribution; cross-region and answer-level tests are rare. (5) Showing confidence changes how much people rely on AI but not how often the joint decision is right; no user study of an EO question-answering assistant was found. (6) Provenance and replay work in EO is mostly qualitative.

**Conclusion.** The best-supported design is to keep numbers out of the language model, attach calibrated and regionally checked confidence to instrument outputs, abstain with a stated next step, and record enough to replay the answer. The least supported parts are cross-region calibration, answer-level evaluation and human-use evidence. Section 7 lists nine research questions.

**Keywords:** Earth observation, vision-language models, flood mapping, Sentinel-1, calibration, conformal prediction, abstention, provenance, human-AI reliance.

---

## 1. Why this topic matters, and what this review asks

**Importance.** Monsoon flood questions are time-critical and local. The data to answer them is free (Sentinel-1 radar sees through cloud), but turning it into an answer needs GIS skills that most district offices lack. Language interfaces promise to remove that barrier. The risk is that a fluent, wrong area figure is acted on. The question is therefore not "can a model answer?" but "under what design can an answer be relied on, and what happens when it cannot?"

**Why a review, and why now.** A project archive of 227 papers (the `archive/` folder) was built for a hackathon entry and concluded that every single ingredient of a trustworthy EO assistant exists somewhere in 2026 work, but that few systems combine more than two. That conclusion rests on one team's reading. This review asks whether it survives a wider, documented search and a cold look at the counter-evidence.

**Review questions.**

- **RQ1.** How reliable are language models and agents when asked EO questions that need a number or a location?
- **RQ2.** How reliable is the measurement layer for floods from Sentinel-1, and where does it fail?
- **RQ3.** What methods give a per-answer uncertainty, and how well do they survive a change of region?
- **RQ4.** What is known about how people use and misuse confidence and uncertainty displays in flood decisions?
- **RQ5.** What is known about making EO answers reproducible and auditable?

---

## 2. Methods

This is a narrative review. It is not a systematic review and does not claim PRISMA compliance; it follows the guidance below instead, and Appendix A records exactly how.

### 2.1 Guidance followed

| Source | What we took from it |
|---|---|
| Baethge, Goldbeck-Wood and Mertens (2019), SANRA, *Res Integr Peer Rev* 4:5 | Six quality items: importance, aims, literature search, referencing, scientific reasoning, endpoint data. We wrote to each (Appendix A). |
| Green, Johnson and Adams (2006), *J Chiropr Med* 5(3):101-117 | Standardise the narrative review to be more objective; describe the search; use a critical appraisal of included work. Only the abstract was read (see limitations). |
| Page et al. (2021), PRISMA 2020, *J Clin Epidemiol* 134:178-189 | Report search sources, dates and counts; separate what was found from what was included. Used for flow reporting only. |
| General narrative-review advice (CASRAI guide; Mayer 2009, ETH Zurich) | Organise by theme, not paper by paper; state the aim in the introduction; end with future directions. Secondary sources, used lightly. |

### 2.2 Sources and search

1. **Project archive.** 227 papers, each with a front-matter `verified` field recording how and when it was checked, grouped in 14 categories. Entries marked abstract-only are leads and are not used for numbers here.
2. **Targeted web search, 2026-11-06.** Fourteen queries on: review-writing guidelines (3), RS vision-language and agent surveys, RS hallucination, conformal and uncertainty methods for SAR flood mapping, global flood monitoring validation, decision-maker studies of uncertain flood maps, unanswerable-question benchmarks, verbalised confidence in language models, Indian Sentinel-1 flood validation, and EO provenance. The search tool is a general web search limited to US results, not a bibliographic database, so recall is unknown.
3. **Verification.** For each candidate that entered the review, the publisher, preprint or portal page was fetched and the title, authors, venue, year and any numbers were read from that page.

### 2.3 Selection and appraisal

- **Included if** it bears on one of RQ1 to RQ5, is about EO or a transferable method (calibration, conformal prediction, abstention, human reliance), and was verified as above.
- **Excluded if** it could not be verified (these appear as "leads", Section 6.3) or duplicated an archive entry.
- **Evidence tags** used throughout: **[F]** numbers read from the paper's body or tables (via the archive's recorded full-text passes); **[A]** abstract or landing-page level only; **[S]** secondary report; **[O]** the project's own measurement.
- **Counts.** 227 archive papers considered as background; 14 new queries; 5 new primary sources verified and added (all [A]); 3 guideline papers; 2 search hits found to duplicate archive entries; 1 search hit found to be mislabelled (a snippet attributed an abstention dataset to arXiv 2403.20213, which is the VHM paper already in the archive, so that claim was dropped).

### 2.4 Limits of the method

One reviewer pass, no second rater, a non-bibliographic search tool, and abstract-level reading for the five new sources. Section 8 expands on this.

---

## 3. A framework: the answer chain

To compare very different papers, we treat a language-driven EO answer as a chain of five links. A paper is placed by the link it studies.

| Link | What happens | Typical failure |
|---|---|---|
| 1. Parse | The question becomes place, dates, quantity | Ambiguous district, wrong period |
| 2. Retrieve | Right scenes found and read | Cloud, missing pass, hallucinated collection IDs |
| 3. Measure | A number and a mask are produced | Misses built-up or vegetated flooding, threshold error |
| 4. Qualify | The answer gets a confidence or an abstention | Over-confidence after a change of region |
| 5. Communicate and act | A person reads it and decides | Misread probability, over-reliance |

Trust is the product of the chain, not of any one link, and the literature is lopsided: links 1 and 3 attract most papers, link 4 few, and link 5 almost none for EO.

---

## 4. Findings

### 4.1 The language layer (RQ1; links 1, 2 and the temptation to use it for 3)

**Remote-sensing language models are unreliable on exactly what a flood officer needs.** On the DIOR-RSVG referring task, GPT-4V reaches IoU 0.5 for 7.6% of referents against 76.8% for a supervised specialist, and its damage-category counts on xBD fit poorly (R² about 0.1) [A013, F]. On GEOBench-VLM the best average multiple-choice accuracy is 41.7% (chance is 20%) and the best referring-detection precision at IoU 0.5 is 34% [A014, F]. GeoChat's referring detection at 0.5 is 10.6% [A001, F]. VRSBench's best model grounds 49.8% of referents at IoU 0.5 [A012, F].

**Hallucination is the norm, not the exception.** RSHallu reports expert-judged hallucination-free rates from 36.33% to 69.00%, with RS-specific models no better than general ones and weakest on image attributes such as modality and resolution [A033, F]. RSHBench finds 47 to 61% of RS question-answering outputs contain hallucinations; a training-free attention-guided zoom (RADAR) lowers one model's rate from 49.9% to 38.8% [A203, F]. The Versatile and Honest model (VHM) trains on deliberately deceptive questions about non-existent objects to teach refusal [A078]. Mitigation helps; it does not bring rates near what an official would need before acting.

**Interpretation.** Three independent benchmark families agree. The evidence supports a division of labour: the language model parses and explains, instruments produce every number. Counter-view: these benchmarks are mostly high-resolution optical, not 10 m Sentinel-1, so absolute figures may not transfer; but no benchmark we found shows an RS language model measuring area from Sentinel-1 to a tolerance a disaster office would accept.

### 4.2 Agents and tool use (RQ1; link 2)

Agents move the number out of the language model into code or tools, and this helps. EO-Gym's LoRA-tuned 4B model learns to fetch older scenes and switch between optical and SAR, reaching 0.74 Pass@3 against 0.49 for its base and 0.67 for Gemini-2.5-Pro [A176, F]. OpenEarthAgent reports end-to-end answer accuracy of 45.26 against 13.72 for its base model and 39.22 for GPT-4o, using replay-validated tool traces [A205, F].

Two cautions. First, live data access is brittle: on UnivEARTH (version 3, 5 October 2026, 408 questions; the earlier 140-question versions report 33% and 58% code failures, so cite the version), the best zero-shot accuracy is 40.0%, generated Earth Engine code fails over 44% of the time, collection IDs are hallucinated, and reflection raises the best model to 64.5% while wrong answers also rise [A204, F]. Second, a 2026 position paper argues that EO operations (reprojection, resampling, compositing) silently change data, so errors propagate, and that EO agents need verifiers, structured geospatial state and evaluation beyond accuracy [A193, A]. It proposes no system and no benchmark itself.

**Interpretation.** Tool use is necessary but not sufficient. These benchmarks score correctness; none of EO-Gym, OpenEarthAgent or UnivEARTH scores whether an agent knows when it is wrong. A third-party 2026 survey states the same gap: calibration, abstention and validated operational use are missing from RS language models and EO agents [A209, A].

### 4.3 Measuring floods from radar (RQ2; link 3)

**Methods are mature and the operational standard is an ensemble.** Rule-based and threshold chains (automatic Otsu-type thresholding with slope and HAND refinement) [A083], Bayesian per-pixel flood probability [A212, A187], and the Copernicus Global Flood Monitoring (GFM) product, which majority-votes three algorithms and gives each flood pixel a 0 to 100 likelihood from their uncertainty outputs [A213], form the baseline. A dual-polarised CNN beat DLR's operational rule chain by about 5 IoU points [A188].

**The failure modes are well characterised.** Flooded built-up areas are largely missed by intensity-based CNNs; coherence helps [A190, A214, A215]. A 2026 evaluation of Prithvi-EO-2.0 on 19 unseen events reports cropland agreement IoU 52%, riverine F1 0.69, tree cover and built-up IoU about 4%, and says part of the apparent error comes from inconsistent definitions across two reference products, with 23 pipeline failure modes found [A227, A]. On the same theme, the likelihood in GFM is only roughly reliable in a single-site check [A213, F].

**India-specific evidence is mostly small-scale and hard to compare.** A 2025 study of Patna's 2023 monsoon flood applies Otsu thresholding to Sentinel-1 in Google Earth Engine, reports water extent peaking at 484.13 sq km on 3 September, and reports overall accuracy of 93.10% and F1 of 0.8416 against high-resolution PlanetScope imagery [Soudagar and Thakur 2025, A]. The abstract does not say how or when the reference was chosen. Such a figure shows the method can work on a clean river-floodplain scene; it says little about peak-monsoon, cloud-covered, vegetated or urban conditions, where optical references are scarce.

**Interpretation.** The measurement layer is good enough to be useful and known well enough to be labelled. The review-level lesson is that accuracy depends on land cover and flood type, so a single global accuracy figure under-describes risk; uncertainty should be conditioned on both. A reference-definition problem (what counts as flood?) also puts a ceiling on any score.

### 4.4 Qualifying answers: calibration, conformal methods and abstention (RQ3; link 4)

**Calibration basics are established.** Modern networks are over-confident and one temperature fitted on held-out data repairs it [A026]; selective classification trades coverage for risk with a statistical guarantee [A027]; conformal methods give label sets with finite-sample coverage [A028] and conformal risk control extends the guarantee to losses such as missed flood area [A133, A219]. Deep ensembles give a cheap spread-based uncertainty [A129]. Crucially, uncertainty degrades under dataset shift [A132].

**What is new for flood mapping.**

- *Conformal risk control with out-of-distribution (OOD) abstention for SAR flood mapping* (Li, Matgen and Chini, IEEE TGRS 64, 4202520, 2026, DOI 10.1109/TGRS.2026.3661208) [A]. Model-knowledge uncertainty from a density-aware network flags OOD inputs for abstention; data uncertainty from softmax entropy drives set-valued predictions; both are exposed through conformal risk control at a user-chosen risk level. The portal abstract reports OOD-detection AUROC of 0.921 (against 0.684 for Bayesian networks and 0.603 for deep ensembles), a fall in average water false-negative rate from 36.9% to 28.5% when OOD inputs are abstained, and a fall in average miscoverage from 4.4% to 1.6% against singleton predictions. This is the closest published match to "calibrated abstention for SAR floods". The abstract does not say whether the tests cross regions.
- *Conformal prediction for Sentinel-2 flood segmentation* (Konidakis, Panayidou, Tsagkatakis and Tsakalides, IGARSS 2025, DOI 10.1109/IGARSS55030.2025.11242848; venue inferred from the DOI prefix) [A]. Compares inductive conformal prediction with k-fold CV+ for a bitemporal U-Net; reports that the inductive variant is limited when data are scarce and that CV+ balances calibration and training-data use better. No numbers on the page.
- *SHRUG-FM*: a decision tree fusing input-space and embedding OOD with ensemble uncertainty lowers risk on kept flood, burn-scar and landslide tiles, but outputs an uncalibrated keep/abstain with a generic next step [A202, F].

**Shift is the open problem.** A calibration fitted elsewhere drifts [A132]. The project's own held-out analysis found a fit never seeing South Asia was over-confident on every South Asian event (India +20, Pakistan +29, Sri Lanka +10 points; under-confident on the USA by 31) and that re-fitting an intercept on eight local chips repairs this at a large coverage cost [O, `paper/evideo.tex`, one Indian event; treat as a hypothesis-generating result]. Li et al. address OOD at the sample level; we found no paper that tests conformal or calibrated SAR flood answers leave-one-region-out and reports answer-level coverage together.

**Can the language model state its own confidence?** For general text question answering, verbalised confidences from RLHF-tuned models are usually better calibrated than their token probabilities, often cutting expected calibration error by about half in relative terms (Tian et al., EMNLP 2023, arXiv 2305.14975, "EMNLP 2023 camera ready" per the arXiv comment) [A]. We found no test of this on EO numeric answers. Given 4.1, and that the quantity of interest is an instrument measurement rather than a recalled fact, there is no evidence for using the language model as the source of confidence here.

**Interpretation.** Tools exist; the evidence gap is evaluation design. Pixel metrics (IoU, F1) and answer metrics (is the published area within tolerance?) differ, and an abstaining system needs the second, plus coverage, reported by region.

### 4.5 People and decisions (RQ4; link 5)

- Showing an AI's confidence made people rely on it more when it was confident but did not raise joint accuracy, and SHAP explanations did not help calibration [A070, F]. Cognitive forcing (commit to your own guess first) reduces blind acceptance but is disliked [A136]. Explanations reduce over-reliance only if they make checking cheaper than trusting [A137].
- For flood maps, an interview study of 140 respondents (government, municipalities, agencies, citizens, farmers) found probabilistic flood forecast maps often misread, such as exceedance probabilities, and that preferences differ by group [Jean et al., HESS 27, 3351, 2023, DOI 10.5194/hess-27-3351-2023; A221, abstract read this session, details F in the archive entry]. This is hydrological forecasting in Quebec, not satellite extent in India.
- A 2024 online study (Discover Water) is reported by search results to show that uncertainty-map design changes decision confidence; the publisher page could not be read, so it is a lead only (6.3).

**Interpretation.** No study of a language-driven EO assistant with real decision-makers was found. The transferable findings are modest: confidence displays change reliance, not accuracy; wording and map design matter; audiences differ. They support showing extent first, plain wording and cheap verification. They do not support any claim that abstention improves decisions in practice. That is an untested claim.

### 4.6 Reproducibility and audit (RQ5)

Standards exist (STAC, COG, CEOS-ARD, openEO) [A121, A122]. Recent work integrates the yProv4WFs provenance library into openEO following W3C PROV-O (Omidi et al., arXiv 2506.08597, 2025), demonstrated on a flood-mapper workflow; the paper is a qualitative demonstration with no overhead, latency or accuracy figures [A, full HTML read]. OpenEarthAgent caches and replays tool traces [A205]. We found no EO study that measures whether a published answer re-runs to an identical output. The EvidEO project reports 8 of 8 demo receipts (713 tiles) re-running to identical hashes after fixing a non-deterministic decimation read and silent tile drop-outs [O, `docs/quality/reproducibility.json`]. That the defect existed is itself a finding: reproducibility cannot be assumed from using standard formats.

---

## 5. Synthesis

### 5.1 What the evidence supports

| Claim | Support | Strength |
|---|---|---|
| RS language models are unreliable for counts, locations and sensor facts | Three benchmark families (A013, A014, A033, A203) | Strong, mostly optical |
| Moving numbers into tools raises answer accuracy | A176, A205, A204 | Moderate; correctness only |
| Radar flood mapping has known blind spots by land cover and flood type | A190, A227, A213 | Moderate to strong |
| Conformal risk control plus OOD abstention reduces SAR flood misses | Li et al. 2026 | Single source, abstract-level |
| Calibration fitted elsewhere is over-confident in a new region | A132 (general), EvidEO own result (one Indian event) | Weak for floods |
| Showing confidence changes reliance, not accuracy | A070 and companions | Moderate, non-EO tasks |
| Answers can be made replayable | Qualitative (Omidi), own result | Weak, no independent measurement |

### 5.2 Points of disagreement and counter-evidence

- **Will better language models close the gap?** Pixel-grounded models such as TerraScope interleave masks into reasoning and report large gains on their own benchmark (68.9 average against 43.3 for the best zero-shot) [A201, F]. If such models reach reliable area measurement on Sentinel-1, the case for keeping numbers out of the model weakens. The honest position is that this has not been shown, not that it cannot be.
- **Is abstention worth its cost?** Abstention reduces wrong answers at the price of coverage. The project's own result (wrong published answers from 45% to 26% at 43% coverage) [O] means more than half of questions go unanswered at that line. Whether officials prefer silence to a flagged low-confidence number is untested (5 above).
- **Pixel versus answer.** Many papers improve IoU by a few points. A trust-focused view says the answer-level error and coverage matter more. This is a framing choice, not a settled fact.
- **Novelty by combination.** The archive concludes that no archived system combines calibrated per-answer confidence, threshold abstention with a next step, replayable receipts, SAR-first monsoon handling, CPU-only operation and plain-language Indian delivery. Li et al. 2026 (calibration plus OOD abstention, SAR floods) is a stronger neighbour than anything the archive held; the combination claim still stands only if the other components are included, and it should be re-checked whenever the watch-list (Section 7) moves.

### 5.3 Where the archive and the wider search agree and differ

The wider search confirmed all five directions the archive held and added: a direct conformal-plus-abstention SAR flood paper, a verbalised-confidence literature, a provenance-in-openEO paper, a recent Indian validation example, and evidence that decision-maker studies exist for forecast maps but not for satellite extents. It did not find a competing end-to-end assistant that publishes calibrated, region-checked, abstaining flood answers.

---

## 6. Gaps and leads

### 6.1 Gaps (evidence we looked for and did not find)

1. Leave-one-region-out evaluation of calibrated or conformal SAR flood answers with coverage reported by region.
2. Answer-level evaluation (area within tolerance of a reference) for any language-driven EO system.
3. Any user study of a language-driven EO assistant with real decision-makers.
4. A measured replay-determinism test of EO answers by anyone other than the project.
5. A Sentinel-1 flood reference set for Indian events beyond the Sen1Floods11 Indian chips, with peak-monsoon labels.

### 6.2 Disagreements in the literature we could not resolve

Reference definitions of flood (permanent water, floodplain, wet paddy) differ across products [A227, A]; this review cannot say which is right for Indian district reporting.

### 6.3 Leads not verified (not used as evidence)

- Lim et al. 2024, *Discover Water*, uncertainty representation in flood maps and geographic decisions (publisher page blocked).
- Majuli Island flood-frequency accuracy (63.44% mean overall accuracy, kappa 0.27) and a lower-Ganges 2016 to 2024 Sentinel-1 study (EGU 2026 abstract), both seen only in search snippets.
- GFM annual quality-assessment reports (JRC and CEMS); an independent 20-event GFM comparison (EGU 2026 abstract).
- Any remote-sensing abstention dataset: a search result named one ("RSSA", attributed to an arXiv ID that turned out to be VHM). Unresolved; do not cite.

---

## 7. Research agenda

1. Run a leave-one-event-out and leave-one-region-out test of Li et al.-style conformal risk control against threshold abstention on Sen1Floods11 plus Kuro Siwo plus any new Indian labels.
2. Label 2 to 3 further Indian events (Assam, Bihar) at peak monsoon; the largest single gain for every claim in Section 4.4.
3. Define an answer-level benchmark: question, place, dates, reference area, tolerance, publish or abstain, scored on error among published answers and coverage by region.
4. Run the same questions through a pixel-grounded RS model (TerraScope-class) and through the instrument pipeline; compare error and calibration.
5. Test verbalised confidence on EO numeric answers against instrument-derived confidence.
6. Condition uncertainty on land cover and flood type, using the detection limits in A227.
7. Run a small user study (officers and journalists) comparing a number alone, number plus confidence, and number plus abstention with next step, measuring joint decision accuracy and reliance.
8. Publish a replay-determinism test protocol and ask other EO assistants to pass it.
9. Maintain the watch-list: SHRUG-FM follow-ups, Li et al. follow-ups, TerraScope or OpenEarthAgent adding confidence, EarthDial follow-ups, Google Earth AI, NRSC Bhuvan chat.

---

## 8. Limitations of this review

- **Search:** a general web search with unknown recall; no database search string with Boolean logic; US-only results; dated 2026-11-06 in a field moving monthly. Section 2.2 is a record, not a guarantee of completeness.
- **Reading depth:** five new sources were read at abstract or landing-page level; Green et al. and PRISMA were confirmed from search results and abstract only, not the body. Archive entries carry their own verification fields; entries marked as leads were not used for numbers.
- **Single reviewer, no second rater.** Self-appraisal against SANRA (Appendix A) is therefore indicative only.
- **Conflict of interest:** the reviewers built one of the systems discussed. Counter-evidence is in 5.2 and the evidence strength table is in 5.1 so readers can discount accordingly.
- **Preprint reliance:** many 2026 sources are arXiv preprints without peer review; strength in 5.1 reflects that.
- **Scope:** floods and Sentinel-1; the framework may not transfer to crops, optical land cover or very high resolution tasks.
- **Rapid change:** a single new paper (for example a conformal-plus-abstention assistant) could change Section 5.2.

## 9. Conclusions

The evidence converges on a design more than on a result. Keep numbers out of the language layer; produce them with instruments whose failure modes are known; attach confidence that has been checked in the region where it is used; abstain with a next step; record enough to replay the answer. What is proven is the first, partially the second, and the failure of the language layer. What is still a hypothesis is that calibrated abstention survives cross-region shift and helps real decisions. Those two are the most valuable things to test next.

---

## Appendix A. How the review follows the guidance

| SANRA item | Where addressed | Self-score (0 to 2; indicative, single rater) | Weakness to fix before submission |
|---|---|---|---|
| 1. Importance explained | Section 1 | 2 | None |
| 2. Aims / questions stated | Section 1 (RQ1 to RQ5) | 2 | None |
| 3. Literature search described | Section 2, Appendix B | 1 | Non-bibliographic tool; add database searches (Scopus, Web of Science, IEEE Xplore) with strings |
| 4. Referencing | Evidence tags, reference list | 1 | Five new sources abstract-only; read full text |
| 5. Scientific reasoning | Sections 3, 4, 5.2 | 2 | Second rater needed |
| 6. Appropriate endpoint data | Tables 5.1; numbers with tags | 1 | Mostly archive-recorded numbers; recheck against papers before publication |

Total 9 of 12, self-assessed, to be replaced by an independent score. The SANRA paper reports a mean of 6.0 over 30 manuscripts it field-tested, so 9 would be above that average, but the scale's validity needs more testing (its authors say so) and a self-score proves little.

Green et al. practice followed: standardised approach, stated search, critical appraisal via the evidence tags, theme-based structure. PRISMA 2020 items used: rationale, objectives, information sources, search dates, selection counts, limitations. Items not met: protocol registration, second reviewer, risk-of-bias tool, formal synthesis; these belong to systematic reviews.

## Appendix B. Search log (2026-11-06)

| # | Topic | Outcome |
|---|---|---|
| 1 | Narrative review structure, SANRA | SANRA, CASRAI guide, ETH guidance |
| 2 | PRISMA 2020 | 27-item checklist, J Clin Epidemiol 134:178-189 |
| 3 | IEEE GRSM review guidelines | Not found; IEEE Sensors Magazine survey guidance seen |
| 4 | RS VLM and agent surveys 2025 to 2026 | Leads mostly in archive (A193, A201, A205) |
| 5 | SANRA original paper | Baethge et al. 2019 verified |
| 6 | Green et al. | Verified at abstract level |
| 7 | RS hallucination benchmarks | RSHallu, RSHBench (A033, A203) |
| 8 | Conformal and uncertainty for SAR floods | Li et al. 2026; Konidakis et al. 2025 (new) |
| 9 | GFM validation | A213, A227, GFM reports (leads) |
| 10 | Decision-maker studies, uncertain flood maps | Jean et al. 2023 (A221); Lim et al. 2024 (lead) |
| 11 | Unanswerable questions, abstention | General-domain only; RS claim unresolved |
| 12 | Verbalised confidence | Tian et al. 2023 (new) |
| 13 | Indian Sentinel-1 flood validation | Soudagar and Thakur 2025 (new); others leads |
| 14 | EO provenance | Omidi et al. 2025 (new) |

## References

Archive entries are cited as [A###] and live in `archive/papers/###-*.md`; links are in `archive/index.csv`. Sources new to this review:

1. Baethge C, Goldbeck-Wood S, Mertens S. SANRA, a scale for the quality assessment of narrative review articles. *Res Integr Peer Rev* 2019;4:5. doi:10.1186/s41073-019-0064-8
2. Green BN, Johnson CD, Adams A. Writing narrative literature reviews for peer-reviewed journals: secrets of the trade. *J Chiropr Med* 2006;5(3):101-117. doi:10.1016/S0899-3467(07)60142-6 (reprint of J Sports Chiropr Rehabil 2001;15:5-19)
3. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *J Clin Epidemiol* 2021;134:178-189. doi:10.1016/j.jclinepi.2021.03.001 (also BMJ 2021;372:n71)
4. Li Y, Matgen P, Chini M. Quantifying and communicating uncertainty in SAR-based flood mapping via density-aware neural networks and conformal risk control. *IEEE Trans Geosci Remote Sens* 2026;64:4202520. doi:10.1109/TGRS.2026.3661208
5. Konidakis I, Panayidou K, Tsagkatakis G, Tsakalides P. Uncertainty-aware flood segmentation from Sentinel 2 observations with conformal prediction. IGARSS 2025, pp. 2116-2120. doi:10.1109/IGARSS55030.2025.11242848
6. Tian K, Mitchell E, Zhou A, Sharma A, Rafailov R, Yao H, Finn C, Manning CD. Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. EMNLP 2023. arXiv:2305.14975
7. Omidi H, Sacco L, Hutter V, et al. Towards provenance-aware Earth observation workflows: the openEO case study. arXiv:2506.08597, 2025.
8. Soudagar R, Thakur AK. Quantifying spatiotemporal variability of Patna's 2023 monsoon flood using Sentinel-1 SAR data and Moran's Index. *Int Arch Photogramm Remote Sens Spatial Inf Sci* 2025;XLVIII-G:1367-1372. doi:10.5194/isprs-archives-XLVIII-G-2025-1367-2025
9. Jean V, Boucher M-A, Frini A, Roussel D. Uncertainty in three dimensions: the challenges of communicating probabilistic flood forecast maps. *Hydrol Earth Syst Sci* 2023;27:3351-3373. doi:10.5194/hess-27-3351-2023 (= A221)
10. Munir MA, et al. Agentic AI for remote sensing: technical challenges and research directions. arXiv:2604.24919, 2026 (= A193; position paper)
11. Kolluru V, et al. Land cover and flood type govern the detection limits of satellite-based flood mapping across diverse global flood events. arXiv:2606.07780, 2026 (= A227; preprint)
