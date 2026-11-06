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

**Abstention.** This is the part I find hardest to settle. The appeal is easy to state. If a system declines when its confidence is low, fewer wrong figures get published, and every method in 4.4 is built around that. Li et al. report the false-negative rate for water dropping from 36.9% to 28.5% once OOD inputs are abstained [A]. EvidEO's own numbers go the same direction: wrong published answers fall from 45% to 26%, at 43% coverage [O]. That coverage figure is the catch. More than half the questions get no number at that confidence line, and the same property that makes the system safe is what makes it frustrating to use.

The literature doesn't tell us which side a real user would pick. A district official in the middle of a flood may want a low-confidence figure flagged as low-confidence and not a refusal. A journalist about to publish may want the opposite. Section 4.5 found no study that measured it. Until someone does, "abstention is worth its coverage cost" is an argument and not a result. Two things should make it easier to accept: a stated next step on every abstention, such as when the next useful satellite pass is, and coverage reported by region and not as one global number. Neither of these has been tested either.

**Pixel versus answer.** Many papers improve IoU by a few points. A trust-focused reading says the error and coverage of the published answer matter more than the pixels behind it. That is a choice of framing, and a reasonable person could prefer the other. We chose answer-level because the end user never sees a pixel.

**Novelty by combination.** The archive concluded that no archived system combines calibrated per-answer confidence, threshold abstention with a next step, replayable receipts, SAR-first monsoon handling, CPU-only operation and plain-language delivery for Indian districts. Li et al. [2026] (calibration plus OOD abstention for SAR floods) is a closer neighbour than anything the archive held when that conclusion was drawn. The combination claim still stands only if all the components are counted together, and it should be re-checked whenever the watch-list in Section 7 moves.

### 5.3 Where the wider search agreed with the archive, and where it differed

The wider search confirmed every direction the archive already held. It added five things: a direct conformal-plus-abstention paper for SAR floods, a verbalised-confidence literature, a provenance-in-openEO paper, one recent Indian validation example, and the observation that decision-maker studies exist for flood forecast maps but not for satellite extents. It did not find a competing end-to-end assistant that publishes calibrated, region-checked, abstaining flood answers. Given the search limits in Section 2, that is weak evidence of absence and not proof.

## 6. Gaps and leads

### 6.1 Evidence we looked for and did not find

1. Leave-one-region-out evaluation of calibrated or conformal SAR flood answers, with coverage reported by region.
2. Answer-level evaluation (published area within tolerance of a reference) for any language-driven EO system.
3. Any user study of a language-driven EO assistant with real decision-makers.
4. A measured replay-determinism test of EO answers by anyone other than the project.
5. A Sentinel-1 flood reference set for Indian events beyond the Sen1Floods11 Indian chips, with peak-monsoon labels.

### 6.2 A disagreement we could not resolve

Reference definitions of "flood" (permanent water, floodplain, wet paddy) differ across products [A227, A]. This review can't say which is right for Indian district reporting.

### 6.3 Leads not verified (not used as evidence)

- Lim et al. 2024, *Discover Water*, on uncertainty representation in flood maps and geographic decisions. The publisher page was blocked.
- A Majuli Island flood-frequency study (63.44% mean overall accuracy, kappa 0.27) and a lower-Ganges 2016 to 2024 Sentinel-1 study (an EGU 2026 abstract). Both were seen only in search snippets.
- The GFM annual quality-assessment reports (JRC and CEMS) and an independent 20-event GFM comparison (an EGU 2026 abstract).
- A remote-sensing abstention dataset named in one search result ("RSSA"), attributed to an arXiv ID that turned out to be VHM. Unresolved, so not cited.
- IC-EO, AgentAbstain and RSure-Agent, surfaced by the last round of searches and not read.

## 7. Research agenda

1. Run a leave-one-event-out and leave-one-region-out test of Li et al.-style conformal risk control against threshold abstention on Sen1Floods11, Kuro Siwo and any new Indian labels.
2. Label two or three more Indian events (Assam, Bihar) at peak monsoon. This is the largest single gain for every claim in Section 4.4.
3. Define an answer-level benchmark: question, place, dates, reference area, tolerance, publish-or-abstain, scored on error among published answers and on coverage by region.
4. Run the same questions through a pixel-grounded RS model (TerraScope-class) and through the instrument pipeline, and compare error and calibration.
5. Test verbalised confidence on EO numeric answers against instrument-derived confidence.
6. Condition uncertainty on land cover and flood type, using the detection limits reported in A227.
7. Run a small user study with officers and journalists that compares a number alone, a number with confidence, and a number with abstention and next step, measuring joint decision accuracy and reliance.
8. Publish a replay-determinism test protocol and ask other EO assistants to pass it.
9. Maintain the watch-list: SHRUG-FM and Li et al. follow-ups, TerraScope or OpenEarthAgent adding confidence, EarthDial follow-ups, RSure-Agent, Google Earth AI, and the NRSC Bhuvan chat.

## 8. Limitations

- **Search.** A general web search with unknown recall, no Boolean database strings, US-only results, run on a single day in a field that moves monthly. Section 2 and Appendix B are a record of what was done, not a guarantee of completeness.
- **Reading depth.** Five new sources were read at abstract or landing-page level. Green et al. and PRISMA were confirmed from search results and abstracts. Archive entries carry their own verification fields, and entries marked as leads were not used for numbers.
- **One reviewer.** No second rater checked selection or tags, so the SANRA self-score in Appendix A is indicative only.
- **Conflict of interest.** The review was commissioned by the team that built one of the systems discussed. Counter-evidence is in 5.2 and the strength column in 5.1 is there so readers can discount accordingly.
- **Preprints.** Many 2026 sources are arXiv preprints without peer review, and the strength ratings in 5.1 reflect that.
- **Scope.** Floods and Sentinel-1 only. The framework may not transfer to crops, optical land cover or very-high-resolution tasks.
- **Speed of change.** One new paper, for example a conformal-plus-abstention assistant, could change Section 5.2.

## 9. Conclusions

The evidence converges on a design more than on a result. Keep numbers out of the language layer. Produce them with instruments whose failure modes are known. Attach confidence that has been checked in the region where it is used. Abstain with a next step. Record enough to replay the answer. The first of these, and the unreliability of the language layer, are well supported. The rest are partly supported. What remains a hypothesis is that calibrated abstention survives a change of region and helps real decisions. Those two are the most valuable things to test next.

## Appendix A. How the review follows the guidance

| SANRA item | Where addressed | Self-score (0 to 2; indicative, one rater) | Weakness to fix before submission |
|---|---|---|---|
| 1. Importance explained | Section 1 | 2 | None |
| 2. Aims and questions stated | Section 1 (RQ1 to RQ5) | 2 | None |
| 3. Literature search described | Section 2, Appendix B | 1 | Non-bibliographic tool; add Scopus, Web of Science and IEEE Xplore searches with strings |
| 4. Referencing | Evidence tags, reference list | 1 | Five new sources abstract-only; read full text |
| 5. Scientific reasoning | Sections 3, 4, 5.2 | 2 | Needs a second rater |
| 6. Appropriate endpoint data | Table in 5.1; tagged numbers | 1 | Many numbers come from archive records; recheck against the papers before publication |

Total 9 of 12, self-assessed, to be replaced by an independent score. The SANRA paper reports a mean of 6.0 over the 30 manuscripts it field-tested, so 9 would sit above that, but its authors say the scale needs more validity testing, and a self-score proves little.

Practice taken from Green et al.: a standardised approach, a stated search, critical appraisal through the evidence tags, and a theme-based structure. PRISMA 2020 items used: rationale, objectives, information sources, search dates, selection counts and limitations. Not met: protocol registration, a second reviewer, a risk-of-bias tool and formal synthesis. Those belong to systematic reviews.

## Appendix B. Search log (2026-11-06)

| # | Topic | Outcome |
|---|---|---|
| 1 | Narrative review structure, SANRA | SANRA, CASRAI guide, ETH guidance |
| 2 | PRISMA 2020 | 27-item checklist; J Clin Epidemiol 134:178-189 |
| 3 | IEEE GRSM review guidelines | Not found; IEEE Sensors Magazine survey guidance seen |
| 4 | RS vision-language and agent surveys, 2025 to 2026 | Leads mostly already in archive (A193, A201, A205) |
| 5 | SANRA original paper | Baethge et al. 2019 verified |
| 6 | Green et al. | Verified at abstract level |
| 7 | RS hallucination benchmarks | RSHallu, RSHBench (A033, A203) |
| 8 | Conformal and uncertainty for SAR floods | Li et al. 2026 and Konidakis et al. 2025 (new) |
| 9 | GFM validation | A213, A227; GFM reports (leads) |
| 10 | Decision-maker studies, uncertain flood maps | Jean et al. 2023 (A221); Lim et al. 2024 (lead) |
| 11 | Unanswerable questions, abstention | General-domain only; RS claim unresolved |
| 12 | Verbalised confidence | Tian et al. 2023 (new) |
| 13 | Indian Sentinel-1 flood validation | Soudagar and Thakur 2025 (new); others leads |
| 14 | EO provenance | Omidi et al. 2025 (new) |

## References

Archive entries are cited as [A###] and live in `archive/papers/###-*.md`. Their links are in `archive/index.csv`. Sources new to this review:

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
