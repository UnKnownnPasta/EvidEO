# Answering with evidence: a narrative review of trustworthy, language-driven Earth observation, with flood mapping as the test case

**Type:** narrative review (non-systematic). **Search and writing date:** 2026-11-06. **Status:** draft, not peer reviewed.

## Competing interests

The review was commissioned by the EvidEO project team (Team Stardust, RVITM), and EvidEO is one of the systems discussed. Its own results are labelled "EvidEO, own result" [O]. They are never the only support for a general claim. The author has no other financial or non-financial interests to declare.

## Abstract

**Background.** People can now ask plain-language questions about satellite imagery. Whether a district disaster officer can act on the answer to "how much land is flooded?" depends on more than the language model.

**Aim.** We reviewed what is known about making language-driven Earth observation (EO) answers trustworthy. The areas covered were language interfaces, measurement, uncertainty and human use. Flood mapping with Sentinel-1 radar is the test case. We also tried to locate where the evidence runs thin.

**Methods.** Narrative review. We started from a 227-paper annotated project archive. On 2026-11-06 we added a targeted web search for areas the archive covered weakly. Five new primary sources were checked against publisher or preprint pages, at abstract level only.

**Findings.**
- Expert-judged hallucination-free rates for remote-sensing (RS) language models run from 36% to 69%.
- Tool-using agents raise accuracy, but the benchmarks score correctness only.
- Radar flood measurement fails in predictable places (built-up areas, tree cover), and the reference maps used to score it disagree on definitions.
- Calibration, conformal risk control and abstention exist for flood segmentation. They are tested at pixel level, mostly inside the training distribution.
- Confidence displays change how much people rely on AI, but not how often the joint decision is right. We found no user study of an EO question-answering assistant.
- Provenance work in EO is mostly qualitative.

**Conclusion.** The best-supported design keeps numbers out of the language model. It attaches confidence that has been checked in the region of use, abstains with a stated next step, and records enough to replay the answer. The weakest evidence concerns cross-region calibration, answer-level evaluation and use by real decision-makers. Section 7 lists nine research questions.

**Keywords:** Earth observation, vision-language models, flood mapping, Sentinel-1, calibration, conformal prediction, abstention, provenance, human-AI reliance.

## 1. Why this topic, and what we ask

Monsoon flood questions are local and urgent. Sentinel-1 radar sees through cloud and the data are free, but turning scenes into a defensible area figure takes GIS skills that most district offices don't have. Language interfaces promise to close that gap. The worry is a fluent, confident, wrong number that somebody acts on. So the question isn't whether a model can answer. It is what design makes an answer safe to rely on, and what should happen when it isn't.

A 227-paper archive was built for a hackathon entry. Its conclusion was that every ingredient of a trustworthy EO assistant exists somewhere in 2026 work, but few systems combine more than two. That rests on one team's reading, and we wanted to see whether it holds up against a documented search and the counter-evidence.

- **RQ1.** How reliable are language models and agents on EO questions that need a number or a location?
- **RQ2.** How reliable is flood measurement from Sentinel-1, and where does it fail?
- **RQ3.** Which methods give a per-answer uncertainty, and how well do they survive a change of region?
- **RQ4.** What is known about how people use or misuse confidence displays in flood decisions?
- **RQ5.** What is known about making EO answers reproducible and auditable?

## 2. Methods

This is a narrative review and does not claim PRISMA compliance. We wrote to the six SANRA items [Baethge et al. 2019] and took the practice of describing the search and appraising included work from Green et al. [2006]. PRISMA 2020 [Page et al. 2021] was used only for flow reporting. Appendix A records how.

**Sources.**
1. *Project archive.* 227 papers in 14 categories. Each has a front-matter field recording how and when it was verified. Entries marked abstract-only were treated as leads and not used for numbers.
2. *Targeted web search, 2026-11-06.* Fourteen queries (Appendix B) covering review guidelines, RS vision-language and agent surveys, RS hallucination, conformal and uncertainty methods for SAR flood mapping, global flood monitoring validation, decision-maker studies, unanswerable-question benchmarks, verbalised confidence, Indian Sentinel-1 validation and EO provenance.
3. *Verification.* For each candidate, the publisher, preprint or portal page was fetched and the bibliographic details and any numbers were read from it.

The search relied heavily on a general web search tool restricted to US results. It is not a bibliographic database, and its recall is unknown. We did not run Scopus, Web of Science or IEEE Xplore searches with Boolean strings. That is the biggest gap in the method.

**Selection.** Papers were included if they bore on RQ1 to RQ5, concerned EO or a transferable method, and could be verified. Unverifiable items became leads (Section 6.3). Evidence tags: **[F]** numbers read from a paper's body or tables, through the archive's recorded full-text passes; **[A]** abstract or landing page only; **[S]** secondary report; **[O]** the project's own measurement.

**Counts.** 227 archive papers as background. 14 queries. 5 new primary sources, all [A]. 3 guideline papers. 2 hits duplicated archive entries. 1 hit was mislabelled: a snippet attributed an abstention dataset to arXiv 2403.20213, which is the VHM paper already in the archive, so that claim was dropped.

**Reviewer.** One person did the reading and appraisal. No second rater checked the selection or the tags. The five new sources were read at abstract level only, because of time and access constraints. Green et al. and PRISMA were confirmed from search results and abstracts, not the full text.

## 3. Framework: the answer chain

To compare papers that study very different things, we split a language-driven EO answer into five links and place each paper by the link it studies.

| Link | What happens | Typical failure |
|---|---|---|
| 1. Parse | Question becomes place, dates, quantity | Ambiguous district, wrong period |
| 2. Retrieve | Right scenes found and read | Cloud, missing pass, invented collection IDs |
| 3. Measure | A number and a mask are produced | Missed built-up or vegetated flooding, threshold error |
| 4. Qualify | Answer gets a confidence or an abstention | Over-confidence after a change of region |
| 5. Communicate and act | A person reads it and decides | Misread probability, over-reliance |

Overall reliability depends on all five links working together, so a strong result at one link can be wasted by a weak one elsewhere. The literature is lopsided. Links 1 and 3 draw most of the papers, link 4 a few, and link 5 almost none for EO.

## 4. Findings

### 4.1 The language layer (RQ1; links 1 and 2)

GPT-4V reaches IoU 0.5 for 7.6% of referents on the DIOR-RSVG referring task, where a supervised specialist reaches 76.8%. Its damage-category counts on xBD fit poorly (R² about 0.1) [A013, F]. On GEOBench-VLM the best average multiple-choice accuracy is 41.7% against a 20% chance level, and the best referring-detection precision at IoU 0.5 is 34% [A014, F]. GeoChat gets 10.6% on referring detection at the same threshold [A001, F]. The best model on VRSBench grounds 49.8% of referents [A012, F].

Hallucination is common. RSHallu reports expert-judged hallucination-free rates between 36.33% and 69.00%. RS-specific models did no better than general ones, and were weakest on attributes like modality and resolution [A033, F]. RSHBench finds hallucinations in 47 to 61% of RS question-answering outputs. A training-free attention-guided zoom (RADAR) brings one model down from 49.9% to 38.8% [A203, F]. VHM trains on deliberately deceptive questions about objects that don't exist, to teach refusal [A078]. Mitigation helps. It doesn't get rates anywhere near what an official would want before acting.

Three independent benchmark families point the same way, which is why we support a division of labour: the language model parses and explains, and instruments produce the numbers. The caveat is that these benchmarks are mostly high-resolution optical. Absolute figures may not carry over to 10 m Sentinel-1. Still, we found no benchmark in which an RS language model measures flooded area from Sentinel-1 to a tolerance a disaster office would accept.

### 4.2 Agents and tool use (RQ1; link 2)

Moving the number into code or tools helps. EO-Gym's LoRA-tuned 4B model learns to fetch older scenes and switch between optical and SAR. It reaches 0.74 Pass@3, against 0.49 for its base and 0.67 for Gemini-2.5-Pro [A176, F]. OpenEarthAgent reports end-to-end accuracy of 45.26, against 13.72 for its base and 39.22 for GPT-4o, using replay-validated tool traces [A205, F].

Live data access is brittle, though. On UnivEARTH (version 3, 5 October 2026, 408 questions; the earlier 140-question versions report 33% accuracy and 58% code failures, so the version matters) the best zero-shot accuracy is 40.0%. Generated Earth Engine code fails more than 44% of the time, and collection IDs get invented. Reflection lifts the best model to 64.5%, but wrong answers go up as well [A204, F]. A 2026 position paper argues that reprojection, resampling and compositing silently alter data so errors propagate. It says EO agents need verifiers, structured geospatial state and evaluation beyond accuracy [A193, A]. It proposes no system or benchmark.

None of EO-Gym, OpenEarthAgent or UnivEARTH scores whether an agent knows when it is wrong. A third-party 2026 survey names the same absence: calibration, abstention and validated operational use [A209, A]. Tool use looks necessary here. Whether it is sufficient is a different matter, and the evidence says no.

### 4.3 Measuring floods from radar (RQ2; link 3)

The methods are mature. Rule-based chains with Otsu-type thresholding plus slope and HAND refinement [A083], Bayesian per-pixel flood probability [A212, A187], and the Copernicus Global Flood Monitoring (GFM) product set the baseline. GFM majority-votes three algorithms and gives each flood pixel a 0 to 100 likelihood derived from their uncertainty outputs [A213]. A dual-polarised CNN beat DLR's operational rule chain by about 5 IoU points [A188].

The failure modes are well described. Intensity-based CNNs largely miss flooded built-up areas, and coherence helps [A190, A214, A215]. A 2026 preprint evaluated Prithvi-EO-2.0 on 19 unseen events. It reports cropland agreement IoU of 52%, riverine F1 of 0.69, and IoU of about 4% for tree cover and built-up areas. It attributes part of the apparent error to inconsistent definitions across two reference products, and it found 23 pipeline failure modes [A227, A]. GFM's likelihood was only roughly reliable in a single-site check [A213, F].

Indian evidence is small-scale and hard to compare. Soudagar and Thakur [2025] apply Otsu thresholding to Sentinel-1 in Google Earth Engine for Patna's 2023 monsoon flood. They report a peak water extent of 484.13 sq km on 3 September, with overall accuracy of 93.10% and F1 of 0.8416 against PlanetScope imagery [A]. The abstract doesn't say how or when the reference was chosen. A clean river-floodplain scene tells us the method can work. It says little about peak-monsoon, cloudy, vegetated or urban conditions, where optical references are scarce.

A single global accuracy figure under-describes the risk, since accuracy moves with land cover and flood type. Any uncertainty estimate probably needs to be conditioned on both. The disagreement over what counts as flooded also puts a ceiling on every score, whatever the model.

### 4.4 Qualifying answers: calibration, conformal methods, abstention (RQ3; link 4)

The basics are settled. Modern networks are over-confident, and a single temperature fitted on held-out data repairs much of it [A026]. Selective classification trades coverage for risk with a statistical guarantee [A027]. Conformal methods give label sets with finite-sample coverage [A028], and conformal risk control extends the guarantee to losses such as missed flood area [A133, A219]. Deep ensembles give a cheap spread-based uncertainty [A129]. All of this degrades under dataset shift [A132].

For flood mapping specifically, three papers matter.

*Li, Matgen and Chini [2026].* A density-aware network supplies model-knowledge uncertainty to flag out-of-distribution (OOD) inputs for abstention. Softmax entropy supplies data uncertainty for set-valued predictions. Both are exposed through conformal risk control at a user-chosen risk level. The portal abstract reports OOD-detection AUROC of 0.921, against 0.684 for Bayesian networks and 0.603 for deep ensembles. Average water false-negative rate falls from 36.9% to 28.5% when OOD inputs are abstained, and average miscoverage falls from 4.4% to 1.6% against singleton predictions [A]. This is the closest published match to calibrated abstention for SAR floods. We read the abstract only, and it doesn't say whether the tests cross regions.

*Konidakis et al. [2025].* Inductive conformal prediction is compared with k-fold CV+ for a bitemporal U-Net on Sentinel-2. The inductive variant is limited when data are scarce, and CV+ balances calibration and data use better [A]. The page gives no numbers. The venue (IGARSS 2025) is inferred from the DOI prefix.

*SHRUG-FM.* A decision tree combines input-space and embedding OOD scores with ensemble uncertainty. It lowers risk on retained flood, burn-scar and landslide tiles, but the keep/abstain output is uncalibrated and the next step offered is generic [A202, F].

Shift is the open problem. The project's own held-out analysis found that a calibration fit without South Asia was over-confident on every South Asian event: India by 20 points, Pakistan by 29, Sri Lanka by 10. It was under-confident on the USA by 31. Re-fitting an intercept on eight local chips repaired this, at a large coverage cost [O, paper/evideo.tex, one Indian event]. We treat this as a hypothesis, not a finding. We found no paper that tests conformal or calibrated SAR flood answers leave-one-region-out and reports answer-level coverage alongside.

Tian et al. [2023] found that, for general text question answering, verbalised confidences from RLHF-tuned models are usually better calibrated than token probabilities, often halving expected calibration error in relative terms [A]. Nobody seems to have tried this on EO numeric answers. Given Section 4.1, and given that the quantity of interest is an instrument measurement and not a recalled fact, we have no evidence for letting the language model be the source of confidence here.

Evaluation design is the actual gap. Pixel metrics (IoU, F1) and answer metrics (is the published area within tolerance of a reference?) are different things. An abstaining system needs the second, plus coverage, reported by region.

### 4.5 People and decisions (RQ4; link 5)

Showing an AI's confidence made people lean on it more when it was confident, but joint accuracy didn't rise, and SHAP explanations didn't help calibration [A070, F]. Cognitive forcing (commit to your own guess first) reduces blind acceptance, though people dislike it [A136]. Explanations cut over-reliance only when they make checking cheaper than trusting [A137].

For flood maps, Jean et al. [2023] interviewed 140 respondents across government, municipalities, agencies, citizens and farmers. Probabilistic forecast maps were often misread (exceedance probabilities especially), and preferences varied by group [A221; abstract read this session, details [F] in the archive entry]. That is hydrological forecasting in Quebec, not satellite extent in India. A 2024 Discover Water study on uncertainty-map design is reported in search results to change decision confidence, but the publisher page was blocked. It is a lead only (6.3).

No study of a language-driven EO assistant with real decision-makers turned up. What transfers is modest. Confidence displays shift reliance and not accuracy. Wording and map design matter. Audiences differ. That supports showing extent first, using plain wording and making verification cheap. It doesn't support the claim that abstention improves real decisions. Nobody has tested that.

### 4.6 Reproducibility and audit (RQ5)

Standards exist: STAC, COG, CEOS-ARD, openEO [A121, A122]. Omidi et al. [2025] integrate the yProv4WFs provenance library into openEO following W3C PROV-O, demonstrated on a flood-mapper workflow. It is a qualitative demonstration with no overhead, latency or accuracy figures (full HTML read). OpenEarthAgent caches and replays tool traces [A205]. We found no EO study that measures whether a published answer re-runs to identical output.

EvidEO reports 8 of 8 demo receipts (713 tiles) re-running to identical hashes, after fixing a non-deterministic decimation read and silent tile drop-outs [O, docs/quality/reproducibility.json]. The defect existing at all is informative: standard formats don't make an answer reproducible by themselves.

## 5. Synthesis

### 5.1 What the evidence supports

| Claim | Support | Strength |
|---|---|---|
| RS language models are unreliable for counts, locations, sensor facts | A013, A014, A033, A203 | Strong, mostly optical |
| Moving numbers into tools raises answer accuracy | A176, A205, A204 | Moderate; correctness only |
| Radar flood mapping has blind spots by land cover and flood type | A190, A227, A213 | Moderate to strong |
| Conformal risk control plus OOD abstention reduces SAR flood misses | Li et al. 2026 | Single source, abstract only |
| Calibration fitted elsewhere is over-confident in a new region | A132 (general); EvidEO, one Indian event | Weak for floods |
| Showing confidence changes reliance, not accuracy | A070 and companions | Moderate; non-EO tasks |
| Answers can be made replayable | Omidi (qualitative); own result | Weak; no independent measurement |

### 5.2 Disagreements, counter-evidence, and one unresolved trade-off

**Better language models might close the gap.** TerraScope-style pixel-grounded models interleave masks into their reasoning and report 68.9 average against 43.3 for the best zero-shot model, on their own benchmark [A201, F]. If a model like that reached reliable area measurement on Sentinel-1, the argument for keeping numbers out of the model weakens a lot. Nobody has shown that it can, and nobody has shown that it can't.

**Abstention.** This is the part I find hardest to settle. The appeal is easy to state. If a system declines when its confidence is low, fewer wrong figures get published, and every method in 4.4 is built around that. Li et al. report the false-negative rate for water dropping from 36.9% to 28.5% once OOD inputs are abstained [A]. EvidEO's own numbers go the same direction: wrong published answers fall from 45% to 26%, at 43% coverage [O].

Look at what 43% coverage means, though. Over half of the questions get no number. For a district officer in a flood week, "no answer, here is what to try next" may be a perfectly good outcome for some questions and a plain failure for others, and nothing in the literature says which. The two figures also aren't on the same footing. Li et al.'s reduction is an average false-negative rate for water reported in the abstract (we have not checked how it is computed), while ours is an answer-level error rate among published answers, with a tolerance we chose. Putting them side by side flatters both.

There is a second problem. The coverage cost depends on where the threshold sits, and the threshold depends on a calibration that, by our own regional result, shifts by 10 to 30 points between regions [O]. So the 43% might be 30% or 60% somewhere else, and we don't know which way it moves. A re-fit on eight local chips fixes the calibration but costs coverage, which pushes the same trade-off further out.

I don't have a clean resolution. One reading says abstention is simply the price of honesty and officials should accept it. The other says a system that withholds the majority of answers will just be abandoned for a worse tool that always answers, and then abstention has lowered reliability in practice. The second reading is speculation on my part. It is not obviously wrong. Only a study with real users (research question 7 below) can separate them, and until then the claim that abstention improves decisions stays untested.

**Pixel versus answer.** Many papers improve IoU by a few points. A trust-focused view puts answer-level error and coverage first. That is a framing choice, not an established fact, and I have made it here.

**Novelty by combination.** The archive concluded that no archived system combines calibrated per-answer confidence, threshold abstention with a next step, replayable receipts, SAR-first monsoon handling, CPU-only operation and plain-language Indian delivery. Li et al. [2026] is a closer neighbour than anything the archive held. The combination claim only holds if all the components are counted, and it should be re-checked whenever the watch-list in Section 7 moves.

### 5.3 Archive versus wider search

The wider search confirmed all five directions the archive already held. It added a direct conformal-plus-abstention SAR flood paper, a verbalised-confidence literature, a provenance-in-openEO paper, a recent Indian validation example, and evidence that decision-maker studies exist for forecast maps but not for satellite extents. It did not find a competing end-to-end assistant that publishes calibrated, region-checked, abstaining flood answers. Given the search limits in Section 2, that is weak evidence of absence.

## 6. Gaps and leads

### 6.1 Gaps

1. Leave-one-region-out evaluation of calibrated or conformal SAR flood answers, with coverage reported by region.
2. Answer-level evaluation (area within tolerance of a reference) for any language-driven EO system.
3. Any user study of a language-driven EO assistant with real decision-makers.
4. A replay-determinism test of EO answers by anyone other than the project.
5. A Sentinel-1 flood reference set for Indian events beyond the Sen1Floods11 Indian chips, with peak-monsoon labels.

### 6.2 Unresolved disagreement

Reference definitions of flood (permanent water, floodplain, wet paddy) differ across products [A227, A]. This review can't say which is right for Indian district reporting.

### 6.3 Leads not verified (not used as evidence)

- Lim et al. 2024, *Discover Water*, uncertainty representation in flood maps (publisher page blocked).
- Majuli Island flood-frequency accuracy (63.44% mean overall accuracy, kappa 0.27) and a lower-Ganges 2016 to 2024 Sentinel-1 study (EGU 2026 abstract), seen only in snippets.
- GFM annual quality-assessment reports (JRC, CEMS) and an independent 20-event GFM comparison (EGU 2026 abstract).
- Any RS abstention dataset. One search result named "RSSA", attributed to an arXiv ID that turned out to be VHM. Unresolved; do not cite.

## 7. Research agenda

1. Run leave-one-event-out and leave-one-region-out tests of Li et al.-style conformal risk control against threshold abstention, on Sen1Floods11, Kuro Siwo and any new Indian labels.
2. Label two or three further Indian events (Assam, Bihar) at peak monsoon. This would help every claim in 4.4 more than anything else.
3. Define an answer-level benchmark: question, place, dates, reference area, tolerance, publish-or-abstain, scored on error among published answers and coverage by region.
4. Run the same questions through a TerraScope-class model and through the instrument pipeline, and compare error and calibration.
5. Test verbalised confidence on EO numeric answers against instrument-derived confidence.
6. Condition uncertainty on land cover and flood type, using the detection limits in A227.
7. Run a small user study with officers and journalists comparing a number alone, number plus confidence, and number plus abstention with next step, measuring joint decision accuracy and reliance.
8. Publish a replay-determinism protocol and invite other EO assistants to run it.
9. Maintain the watch-list: SHRUG-FM and Li et al. follow-ups, TerraScope or OpenEarthAgent adding confidence, EarthDial follow-ups, Google Earth AI, NRSC Bhuvan chat.

## 8. Limitations

**Search.** The search leaned on a general web tool with unknown recall, US-only results and no Boolean database strings. Section 2 is a record of what was done and not a guarantee of completeness. The field moves monthly, and the search is dated 2026-11-06.

**Reading depth.** Five of the newer primary sources were assessed on abstracts or landing pages only, because of time and access. Green et al. and PRISMA were checked from search results and abstracts. Archive entries carry their own verification fields, and leads weren't used for numbers.

**Single reviewer.** There was no independent second reviewer, so selection and the evidence tags haven't been cross-checked.

**Competing interest.** The reviewers built one of the systems discussed. The counter-evidence is in 5.2 and the strength table is in 5.1 so readers can discount accordingly.

**Preprints.** Many 2026 sources are unreviewed arXiv preprints, and the strength ratings reflect that.

**Scope.** The work covers floods and Sentinel-1. The framework may not transfer to crops, optical land cover or very high-resolution tasks.

**Fast change.** One new paper, such as a conformal-plus-abstention assistant, could overturn Section 5.2.

## 9. Conclusions

The evidence supports a design more than a result. Numbers should come from instruments whose failure modes are known, not from the language layer. Confidence should be checked in the region where it is used. When the system abstains it should say what to do next, and enough should be recorded to replay the answer. The failure of the language layer on numbers is well established, and the case for tools is partly established. Whether calibrated abstention survives a change of region, and whether it helps real decisions, is still a hypothesis. Those are the two most useful things to test next.

## Appendix A. Self-assessment against SANRA

This is a subjective self-check by the single author. It is not an independent or definitive quality measure.

| SANRA item | Where addressed | Score (0 to 2) | To fix |
|---|---|---|---|
| 1. Importance | Section 1 | 2 | None |
| 2. Aims stated | Section 1 | 2 | None |
| 3. Search described | Section 2, Appendix B | 1 | Add Scopus, Web of Science and IEEE Xplore searches with strings |
| 4. Referencing | Tags, reference list | 1 | Read the full text of the five abstract-only sources |
| 5. Scientific reasoning | Sections 3, 4, 5.2 | 2 | Needs a second rater |
| 6. Endpoint data | Table 5.1 | 1 | Recheck archive-recorded numbers against the papers |

Total: 9 of 12. The SANRA authors report a mean of 6.0 over the 30 manuscripts they field-tested, but they also say the scale needs further validation, and a self-score proves little. Following Green et al., we used a standardised approach, a stated search, critical appraisal through evidence tags, and a theme-based structure. From PRISMA 2020 we used rationale, objectives, information sources, search dates, selection counts and limitations. Not met: protocol registration, second reviewer, risk-of-bias tool, formal synthesis.

## Appendix B. Search log (2026-11-06)

1. Narrative review structure, SANRA. Outcome: SANRA, CASRAI guide, ETH guidance.
2. PRISMA 2020. Outcome: 27-item checklist, J Clin Epidemiol 134:178-189.
3. IEEE GRSM review guidelines. Outcome: not found.
4. RS VLM and agent surveys 2025-26. Outcome: leads mostly in archive (A193, A201, A205).
5. SANRA original paper. Outcome: verified.
6. Green et al. Outcome: verified at abstract level.
7. RS hallucination benchmarks. Outcome: RSHallu, RSHBench (A033, A203).
8. Conformal and uncertainty for SAR floods. Outcome: Li et al. 2026; Konidakis et al. 2025 (new).
9. GFM validation. Outcome: A213, A227, GFM reports (leads).
10. Decision-maker studies, flood maps. Outcome: Jean et al. 2023 (A221); Lim et al. 2024 (lead).
11. Unanswerable questions, abstention. Outcome: general domain only; RS claim unresolved.
12. Verbalised confidence. Outcome: Tian et al. 2023 (new).
13. Indian Sentinel-1 flood validation. Outcome: Soudagar and Thakur 2025 (new); others leads.
14. EO provenance. Outcome: Omidi et al. 2025 (new).

## Bibliography

### Part 1. Sources new to this review

1. Baethge C, Goldbeck-Wood S, Mertens S. SANRA, a scale for the quality assessment of narrative review articles. *Res Integr Peer Rev* 2019;4:5. https://doi.org/10.1186/s41073-019-0064-8
2. Green BN, Johnson CD, Adams A. Writing narrative literature reviews for peer-reviewed journals: secrets of the trade. *J Chiropr Med* 2006;5(3):101-117. https://doi.org/10.1016/S0899-3467(07)60142-6
3. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *J Clin Epidemiol* 2021;134:178-189. https://doi.org/10.1016/j.jclinepi.2021.03.001
4. Li Y, Matgen P, Chini M. Quantifying and communicating uncertainty in SAR-based flood mapping via density-aware neural networks and conformal risk control. *IEEE Trans Geosci Remote Sens* 2026;64:4202520. https://doi.org/10.1109/TGRS.2026.3661208
5. Konidakis I, Panayidou K, Tsagkatakis G, Tsakalides P. Uncertainty-aware flood segmentation from Sentinel 2 observations with conformal prediction. IGARSS 2025, pp. 2116-2120. https://doi.org/10.1109/IGARSS55030.2025.11242848
6. Tian K, Mitchell E, Zhou A, Sharma A, Rafailov R, Yao H, Finn C, Manning CD. Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. EMNLP 2023. https://arxiv.org/abs/2305.14975
7. Omidi H, Sacco L, Hutter V, et al. Towards provenance-aware Earth observation workflows: the openEO case study. arXiv 2025. https://arxiv.org/abs/2506.08597
8. Soudagar R, Thakur AK. Quantifying spatiotemporal variability of Patna's 2023 monsoon flood using Sentinel-1 SAR data and Moran's Index. *Int Arch Photogramm Remote Sens Spatial Inf Sci* 2025;XLVIII-G:1367-1372. https://doi.org/10.5194/isprs-archives-XLVIII-G-2025-1367-2025
9. Jean V, Boucher M-A, Frini A, Roussel D. Uncertainty in three dimensions: the challenges of communicating probabilistic flood forecast maps. *Hydrol Earth Syst Sci* 2023;27:3351-3373. https://doi.org/10.5194/hess-27-3351-2023 (= A221)
10. Munir MA, et al. Agentic AI for remote sensing: technical challenges and research directions. arXiv 2026. https://arxiv.org/abs/2604.24919 (= A193)
11. Kolluru V, et al. Land cover and flood type govern the detection limits of satellite-based flood mapping across diverse global flood events. arXiv 2026. https://arxiv.org/abs/2606.07780 (= A227)

### Part 2. Archive tags used in the text

Each entry lives at `archive/papers/###-*.md`. Titles, years and links are copied from `archive/index.csv`.

| Tag | Title | Year | Link |
|---|---|---|---|
| A001 | GeoChat: Grounded Large Vision-Language Model for Remote Sensing | 2024 | https://arxiv.org/abs/2311.15826 |
| A012 | VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding | 2024 | https://arxiv.org/abs/2406.12384 |
| A013 | Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data | 2024 | https://arxiv.org/abs/2401.17600 |
| A014 | GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks | 2024 | https://arxiv.org/abs/2411.19325 |
| A026 | On Calibration of Modern Neural Networks | 2017 | https://arxiv.org/abs/1706.04599 |
| A027 | Selective Classification for Deep Neural Networks | 2017 | https://arxiv.org/abs/1705.08500 |
| A028 | Uncertainty Sets for Image Classifiers using Conformal Prediction | 2021 | https://arxiv.org/abs/2009.14193 |
| A033 | RSHallu: Dual-Mode Hallucination Evaluation for Remote-Sensing Multimodal Large Language Models with Domain-Tailored Mitigation | 2026 | https://arxiv.org/abs/2602.10799 |
| A070 | Effect of Confidence and Explanation on Accuracy and Trust Calibration in AI-Assisted Decision Making | 2020 | https://doi.org/10.1145/3351095.3372852 |
| A078 | VHM: Versatile and Honest Vision Language Model for Remote Sensing Image Analysis | 2025 | https://arxiv.org/abs/2403.20213 |
| A083 | Sentinel-1-based flood mapping: a fully automated processing chain | 2016 | https://doi.org/10.1080/01431161.2016.1192304 |
| A121 | The openEO API: Harmonising the Use of Earth Observation Cloud Services Using Virtual Data Cube Functionalities | 2021 | https://doi.org/10.3390/rs13061125 |
| A122 | CEOS-ARD Product Family Specification: Synthetic Aperture Radar (Normalised Radar Backscatter [NRB], Polarimetric Radar, Ocean Radar Backscatter, Geocoded SLC, Interferometric Radar, Composite Backscatter), Version 1.3.1 | 2026 | https://ceos.org/ard/files/PFS/SAR/v1.3.1/CEOS-ARD_PFS_SAR_v1.3.1.pdf |
| A129 | Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles | 2017 | https://arxiv.org/abs/1612.01474 |
| A132 | Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift | 2019 | https://arxiv.org/abs/1906.02530 |
| A133 | Conformal Risk Control | 2024 | https://arxiv.org/abs/2208.02814 |
| A136 | To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making | 2021 | https://arxiv.org/abs/2102.09692 |
| A137 | Explanations Can Reduce Overreliance on AI Systems During Decision-Making | 2023 | https://arxiv.org/abs/2212.06823 |
| A176 | EO-Gym: A Multimodal, Interactive Environment for Earth Observation Agents | 2026 | https://arxiv.org/abs/2605.01250 |
| A187 | Satellite-Based Flood Mapping through Bayesian Inference from a Sentinel-1 SAR Datacube | 2022 | https://doi.org/10.3390/rs14153673 |
| A188 | Sentinel-1-Based Water and Flood Mapping: Benchmarking Convolutional Neural Networks Against an Operational Rule-Based Processing Chain | 2022 | https://doi.org/10.1109/JSTARS.2022.3152127 |
| A190 | UrbanSARFloods: Sentinel-1 SLC-Based Benchmark Dataset for Urban and Open-Area Flood Mapping | 2024 | https://arxiv.org/abs/2406.04111 |
| A193 | Agentic AI for Remote Sensing: Technical Challenges and Research Directions | 2026 | https://arxiv.org/abs/2604.24919 |
| A201 | TerraScope: Pixel-Grounded Visual Reasoning for Earth Observation | 2026 | https://arxiv.org/abs/2603.19039 |
| A202 | SHRUG-FM: Reliability-Aware Foundation Models for Earth Observation | 2026 | https://arxiv.org/abs/2511.10370 |
| A203 | Seeing Clearly without Training: Mitigating Hallucinations in Multimodal LLMs for Remote Sensing | 2026 | https://arxiv.org/abs/2603.02754 |
| A204 | Towards LLM Agents for Earth Observation | 2026 | https://arxiv.org/abs/2504.12110 |
| A205 | OpenEarthAgent: A Unified Framework for Tool-Augmented Geospatial Agents | 2026 | https://arxiv.org/abs/2602.17665 |
| A209 | From Perception to Reasoning in Remote Sensing: A Survey and Outlook | 2026 | https://www.preprints.org/manuscript/202608.1840 |
| A212 | Probabilistic Flood Mapping Using Synthetic Aperture Radar Data | 2016 | https://doi.org/10.1109/TGRS.2016.2592951 |
| A213 | Estimating Ensemble Likelihoods for the Sentinel-1-Based Global Flood Monitoring Product of the Copernicus Emergency Management Service | 2023 | https://doi.org/10.1109/JSTARS.2023.3292350 |
| A214 | Use of SAR Data for Detecting Floodwater in Urban and Agricultural Areas: The Role of the Interferometric Coherence | 2016 | https://doi.org/10.1109/TGRS.2015.2482001 |
| A215 | Sentinel-1 InSAR Coherence to Detect Floodwater in Urban Areas: Houston and Hurricane Harvey as A Test Case | 2019 | https://doi.org/10.3390/rs11020107 |
| A219 | Conformal Semantic Image Segmentation: Post-hoc Quantification of Predictive Uncertainty | 2024 | https://arxiv.org/abs/2405.05145 |
| A221 | Uncertainty in three dimensions: the challenges of communicating probabilistic flood forecast maps | 2023 | https://doi.org/10.5194/hess-27-3351-2023 |
| A227 | Land cover and flood type govern the detection limits of satellite-based flood mapping across diverse global flood events | 2026 | https://arxiv.org/abs/2606.07780 |
