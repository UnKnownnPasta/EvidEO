# What is new in EvidEO, and what would have to be true

This document is an honest comparison against the closest existing systems. Version 10 (M8, 2026-10-10) is the final pass against the whole archive of 225 papers plus the competitor evidence in [docs/reference/problem-evidence.md](docs/reference/problem-evidence.md). **Start with section 5**, which states each claim in its final wording, ties it to the closest prior art and points to the prototype evidence in [docs/VERIFICATION.md](docs/VERIFICATION.md). Sections 1 to 4 are kept as the run-by-run record that led there.

Citation keys: `[A001]` is an archive entry and `[E49]` is an evidence-brief claim.

## 1. Comparison

The dimensions are the ones that matter to a district official, extension officer or fact-checker without GIS skills.

| System | Plain-language questions | Fetches live Sentinel data for my area and dates | SAR used automatically under cloud | Scene ID and date on every answer | Region mask | Calibrated confidence | Abstains when unsure | Re-runnable receipt | Runs on CPU or offline | Free or open, usable in India |
|---|---|---|---|---|---|---|---|---|---|---|
| GeoChat [A001] | Yes | No (user supplies image) | No (RGB only) | No | Boxes as text, weak | No | No | No | No (7B) | Open weights |
| EarthGPT [A002] | Yes | No | Can read SAR, no automatic choice | No | No | No | No | No | No | Open data and code; weights not confirmed |
| EarthDial [A003] | Yes | No | Reads S1 VH, no automatic choice | No | Boxes | No | No | No | Possible but slow (4B) | Open weights |
| TEOChat [A007] | Yes, temporal | No | No | No | No | No | No | No | No | Open |
| LHRS-Bot [A005], RSGPT [A006], SkyEyeGPT [A004], RS-LLaVA [A025] | Yes | No | No | No | Partial (some grounding) | No | No | No | No | Mostly open |
| SARChat models [A021] | Yes, SAR only | No | SAR only | No | Partial | No | No | No | Small checkpoints exist | Open |
| Remote Sensing ChatGPT [A023] | Yes | No | No | No | Via tools | No | No | No | No (cloud LLM) | Code open; needs a paid LLM |
| GeoLLM-Engine agents [A024] | Yes | Environment only | No | No | Via tools | No | No | No | No | Research environment; no public code found |
| VHM [A078] | Yes | No | No | No | Boxes | No | **Partly: trained to refuse questions about absent objects (four question types); no threshold or score** | No | No (7B) | Open |
| EarthMind [A079], FUSAR-GPT [A082] | Yes | No | Reads SAR, no automatic choice; EarthMind's authors find the fused model nearly ignores SAR | No | Partial | No | No | No | No | Mostly open |
| Falcon [A080] | Task prompts | No | No | No | Masks | No | No | No | Plausible (0.7B) | Open |
| Change-Agent [A089] | Yes, change only | No | No | No | Change masks | No | No | No | No | Open code |
| Earth-Agent [A094] (ICLR 2026) | Yes | Via GEE products | No SAR | No | Via tools | No | No | No | No (cloud LLM) | Benchmark and code |
| Google Earth AI and Gemini geospatial reasoning [A095, E49] | Yes | Yes (Google data and models) | Not evaluated on SAR time series [A095] | No per-answer scene IDs found [A095] | Yes, on map | Confidence intervals on some model outputs, not on agent answers [A095] | No refusal behaviour described [A095] | No public evidence | No | US-gated paid tiers; not India |
| NASA and Microsoft Earth Copilot [E50] | Yes | NASA data | Unknown | Dataset-level | Unknown | Unknown | Unknown | Unknown | No | Researcher preview |
| Esri ArcGIS AI assistants [E51] | Yes, for ArcGIS tasks | Via ArcGIS | No | Via layers | Yes | No | No | Partial (ArcGIS history) | No | Paid licence |
| NRSC Bhuvan chatbot proposal [E29, E56] | Yes, multilingual | Proposed | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Government infrastructure | Research proposal, not deployed |
| NRSC and NDEM flood maps [E3, E5, E6] | No (fixed products) | Yes, centrally | Yes (SAR preferred) | Yes | Yes | No (labelled "preliminary") | n/a | No | Government | Official agencies; not on demand |
| RSure-Agent [A164] (2026 preprint) | Agent tasks | No | No | No | Via tools | **Per-tool reliability learned from past tasks, used inside the agent; not shown to users** | **Internal: rejects or asks for more evidence before using a tool output** | No | No (LLM agent) | Preprint |
| Selective tool use for change VQA [A172] (2026 preprint) | Yes, change questions | No | No | No | Via fixed change tools | No | No | No | Small (4B LoRA) | Preprint |
| ScaleEarth [A171] (2026 preprint) | Yes | No | No | No | No | Uncertainty on its resolution guess only | Falls back to a default resolution, never abstains on the answer | No | No | Preprint |
| GeoDisaster agents [A174] (2026 benchmark, IIT Bombay) | Yes, disaster questions incl. Sentinel-1 floods | Workflows over prepared data | Yes, in a SAR flood subset | Not per answer | Via workflows | No (authors list uncertainty as future work) | No | Runnable workflows | No | Benchmark |
| Earth-Agent-Pro [A166] (2026 preprint) | Yes | Via tools | Partial | No | Via tools | No | No | Evidence log for self-repair only | No | Preprint |
| QAG-360K / VisTA [A179] (2024 preprint) | Yes, change questions | No (bitemporal optical pairs supplied) | No | No | **Yes: a change mask with every answer, empty when nothing changed** | No | No | No | No | Test set on request |
| EO-Gym agent [A176] (2026 preprint) | Yes | Yes, inside its environment (local lookups of older scenes and of paired optical and SAR views) | Tool call to an optical-to-SAR view, chosen by the question, not by cloud (benchmark only) | No | Via tools | No | No | No | Small (4B LoRA) | Preprint |
| TerraScope [A201] (CVPR 2026) | Yes | No | Learned token-level choice between optical and SAR from the question text (cloud example in the paper); concatenation scored slightly higher; prepared chips, no live scene search | No | **Yes, pixel masks behind area answers** | No | No | No | No (GPU) | Open per paper |
| SHRUG-FM [A202] (CVPR EarthVision 2026) | No (segmentation model) | No | No (Sentinel-2 optical) | No | Flood masks | **Reliability scores, stated as not calibrated** | **Rejects unreliable flood maps; no next step** | No | Not stated | Research code |
| UnivEARTH agents [A204] (ACL 2026 Findings) | Yes | **Yes, via Earth Engine code the agent writes** | Not automatic | No | Via code | No | No | No | No (cloud LLM) | Needs Earth Engine |
| OpenEarthAgent [A205] (ECCV 2026) | Yes | No | No | No | Via tools | No | No | **Deterministic replay of tool traces** | No | Open |
| **EvidEO (built, run 9)** | Yes, a fixed set of question types and 735 named districts; Indian date formats and common Hindi and Hinglish words | **Yes, live** (three public STAC catalogues, tested end to end) | **Yes** (monsoon rule, tested on live data; water uses VV and VH since run 7) | **Yes** | **Yes** (per-tile PNG overlays clipped to the district) | **Fitted for water extent (Sen1Floods11) and water change (Kuro Siwo, one map per answer regime); crop change still a labelled placeholder** | **Yes, with a next step** | **Yes** | **Yes** (a whole district in about 40 to 60 s on CPU) | **Yes, open source, free data** |

"Unknown" means we found no public evidence either way. These cells will be revisited as the archive grows.

## 2. What is new, stated honestly

**Not new on its own.** Each of these exists in prior work:

- natural-language interfaces to remote sensing [A001 to A007];
- multi-sensor understanding including SAR [A002, A003, A021];
- tool-calling EO agents [A023, A024];
- SAR flood mapping [A022];
- cloud masking and SAR fallback (NRSC already prefers SAR for floods [E32]).

**New, as far as the archive shows so far:**

1. **Instruments answer, the language model only routes and explains.** Every number in a EvidEO answer comes from a named, versioned, transparent instrument run on an identified scene. Generative model weights never produce it. RS assistants in the archive generate answers directly [A001 to A007, A025]. Agents call tools but pass free text back through the LLM, with no confidence carried through [A023, A024].
2. **The evidence card as the unit of answer.** One answer carries:
   - what the system understood;
   - scene IDs and dates;
   - the sensor, with automatic optical-or-SAR choice;
   - the mask;
   - calibrated confidence;
   - an observed-versus-inferred flag;
   - a receipt that re-runs to the same output hash.

   None of the archived systems return this bundle. The receipt and observed-versus-inferred parts answer the provenance and audit-trail call in [E39].
3. **Abstention as a designed outcome, with a constructive next step.** "Insufficient evidence, next Sentinel-1 pass on date X" replaces a guess. Run 4 narrows this: VHM [A078] trains an RS VLM to refuse questions about objects that are not in the image, and GeoBenchX [A093] scores agents on refusing unsolvable tasks. Neither ties refusal to a confidence threshold over a measurement, reports coverage, or tells the user what would fix it. The claim is therefore "threshold-based abstention over a measured quantity, with a next step", not "the first RS system that refuses".
4. **Ease of deployment.** The whole truth layer runs on CPU on free data with no training, and can run fully offline. That makes it deployable on district or state infrastructure today. Fine-tuning improves only the language layer.

The claim is novelty of **combination and packaging for a specific user**, which is what the user asked for ("innovative in how it solves the problem"). It is not a new model architecture.

## 3. What would have to be true for the claim to hold

| # | Condition | How we check it | Status |
|---|---|---|---|
| 1 | No published RS assistant already returns per-answer scene provenance plus calibrated confidence plus abstention | Keep searching the archive, especially trust-calibration, eo-agents and upcoming work (runs 2 onward) | **Holds for 175 papers (run 7).** The nearest 2026 work learns tool reliability inside an agent without showing it to users (RSure-Agent [A164]), abstains only on an internal resolution guess (ScaleEarth [A171]), or names uncertainty as future work (GeoDisaster [A174]). Earlier note, still narrower than run 1: instrument-grounded agents exist (Earth-Agent [A094], Change-Agent [A089], Google Earth AI [A095]) and learned refusal exists (VHM [A078]). None combines the four (instruments, per-answer scene provenance, confidence, threshold abstention), and none uses SAR for cloud |
| 2 | Instrument answers are accurate enough on Indian scenes to be useful at a reasonable coverage | M3 and M6: risk-coverage curves on a labelled Indian set | **Improved but not met (run 7).** Water v1.1 (VV or VH) publishes 43% of held-out chips with 26% wrong and 52% of Indian chips (fit without India) with 55% wrong; flood-change answers with real new water are right only 27% of the time on Kuro Siwo and now abstain. Run 6 status: **Fails for water today.** On 64 Indian Sen1Floods11 chips the VV-only water instrument has median IoU 0.03, and after calibration it publishes 12% of them with 62% wrong. The trust machinery works (it abstains), but usefulness needs instrument v1.1 with VH. Crop change not yet tested on labels |
| 3 | Calibration fitted on public data transfers to India, or Indian labels can be gathered | M5 calibration fitting; report expected calibration error per zone | **Partly (runs 6 and 7).** Run 7: India with a fit made without India, ECE 0.30 to 0.23 (v1.1); Kuro Siwo change maps cross-validated by event, ECE 0.041 with regime maps. Run 6: Fit on 312 chips worldwide: held-out ECE 0.30 to 0.09; unseen Bolivia 0.34 to 0.22; India with a fit made without India 0.50 to 0.36. Calibration transfers to unseen chips of known events but degrades on new regions, as dataset-shift work predicts [A132], so per-region refits are needed |
| 4 | Non-GIS users understand evidence cards and abstentions faster than maps or chat answers | M4 UX design; a small usability test with students or officers if possible | Not yet tested |
| 5 | Public STAC endpoints plus COG reads are fast enough for "minutes, not hours" on CPU | M2 and M6: measured latency per district-sized AOI | **First measurement holds:** Barpeta, 117 tiles, 2,335 sq km, 30.6 s from question to card on sandbox CPU (run 4). Repeat under load in M6 |
| 6 | Google Earth AI, Earth Copilot or the NRSC chatbot do not already ship this bundle in India | Re-check product pages each run | Holds as of 2026-10-04 [E49, E50, E56] |

### Run 2 evidence that strengthens or tests the claim

- **Calibration and abstention are mature in general ML but absent from RS assistants.** Temperature scaling [A026], selective classification with a guaranteed risk [A027], conformal sets [A028] and VQA abstention [A030] are well established. Conformal prediction has reached per-pixel RS classification [A032]. None of the archived RS assistants use any of them. EvidEO's contribution is applying them per instrument and showing them to a non-expert, not inventing them.
- **The hallucination gap is now measured for RS VLMs.** RSHallu reports hallucination-free rates of roughly 36% to 69% for RS multimodal models [A033]. This strengthens the case for keeping generated text out of the number path.
- **Learned change models are no clear upgrade over a transparent instrument.** On Kuro Siwo, dedicated change-detection networks did not beat segmentation models given the full pre/post stack [A041], and learned optical change models swing widely across datasets [A038]. This supports transparent, calibrated instruments.
- **Official Indian practice already uses thresholding.** The NRSC flood atlas detects SAR water by variable thresholding [A046], and Indian case studies use Otsu on Sentinel-1 [A042]. EvidEO's instruments are therefore familiar to official users; the new part is per-question, on-demand delivery with confidence and a receipt.
- **New risk to the claim:** strict risk targets can collapse coverage [A030]. The claim must be stated with its measured coverage, not just its risk.

### Run 3 evidence that strengthens or tests the claim

- **Human-factors research backs the evidence card over the chat answer.** Explanations raise acceptance of AI answers whether right or wrong [A067]; confidence display helps reliance match reliability but does not by itself raise accuracy [A070]; trust should be calibrated, not maximised [A065]; responders are limited by trust and workflow fit more than by algorithms [A069]. Fluent RS assistants optimise the very thing these studies warn about. The card-first design is a direct application, not a novelty of method.
- **The parser can be small.** Natural-language interfaces to data work by turning a question into an inspectable structured spec with ambiguity flags [A068]. EvidEO's "I understood your question as" panel is the same pattern, which means a 256M to 2.2B open VLM [A063] with LoRA [A059, A060] is enough for the language layer.
- **EO foundation models are a threat and an ally.** Prithvi-EO-2.0, CROMA, SSL4EO-S12, DOFA and Clay [A052, A054 to A057] are open and Sentinel-native, but none ships a calibrated, abstaining, receipt-backed answer for a non-expert. They are best registered as instruments behind the same card. SkySense [A053] shows the accuracy ceiling of multi-modal fusion, but with non-commercial weights at billion-parameter scale.
- **Object counting stays out of scope.** Detection benchmarks are built on 0.3 m to 1 m imagery (DOTA, xView, DIOR [A071 to A073]); even there small objects are hard. Sentinel-1 ship detection (xView3-SAR [A075]) is the one object task native to our data and a candidate future instrument.
- **Data-layer ease is real but must be engineered.** Of three public catalogues, only some serve openly readable Sentinel-1 pixels (Earth Search S1 GRD is requester-pays; CDSE downloads need an account). EvidEO's M2 data layer records which catalogue answered and why a scene was chosen, so this complexity never reaches the user.

### Run 4 evidence that strengthens or tests the claim

- **Instrument-grounded EO agents now exist, and they are the closest prior art.** Earth-Agent (ICLR 2026) [A094] calls 104 tools including NDVI and NDWI; Change-Agent [A089] uses a change model as its eyes and an LLM as its brain; Google Earth AI [A095] chains Google's imagery, population and flood models under a Gemini agent. EvidEO's "instruments answer" is therefore not new as an idea. What stays new is what these agents lack: calibrated confidence on the answer, abstention below a threshold, scene IDs and dates on every answer, a re-runnable receipt, and SAR when clouds block optical.
- **Free-form tool agents get the parameters wrong.** Earth-Agent's GPT-5 matches expert tool parameters only about 26% of the time [A094]; on ThinkGeo, GPT-4o gets tool arguments right about a third of the time and the final answer right under 10% end to end [A092]; GeoGPT reports hallucinated tool and file arguments [A090]. A fixed router to versioned instruments with set parameters removes this whole failure class. This is the strongest published support so far for EvidEO's ease claim.
- **VLMs still cannot be trusted to read SAR.** EarthMind's authors find the fused optical plus SAR model is nearly blind to the SAR input [A079]; FUSAR-GPT counts SAR targets correctly about 53% of the time [A082]; Geo-R1's SAR grounding is about 25% [A081]. Pixel-grounded RS VLMs reach about 52 mIoU on masks [A076]. EvidEO's SAR answers stay instrument-only.
- **The SAR flood method EvidEO uses is the operational one.** The DLR / Copernicus GFM chain is split-based tile selection plus a minimum-error threshold, with a fallback near -18 dB [A083 to A086]. EvidEO implements the same family per tile, reports every threshold, and found on live Barpeta data that Otsu misplaces the threshold where Kittler-Illingworth does not.
- **The data supply keeps improving.** Sentinel-1C and 1D restore a two-satellite constellation with about 6-day revisit [A100]; NISAR adds free L-band and S-band SAR with provisional calibrated products since July 2026 [A098]. More passes mean fewer abstentions for lack of a recent scene.
- **A learned land-cover model was wrong, and the card abstained.** On live Sentinel-2 over Darbhanga (mostly cropland), RemoteCLIP [A008] labelled patches as grassland, forest and bare land with mean top probability 0.35, so the card abstained instead of publishing it. This is the design working, and a measured case for keeping learned models behind a confidence gate.

### Run 5 evidence that strengthens or tests the claim

- **Benchmarks keep confirming the core design choice.** On DisasterM3, general and RS VLMs are near chance at counting damaged buildings and get worse when the post-disaster image is SAR [A118]. On XLRS-Bench, the best MLLMs average about 40% on four-option questions over huge scenes and almost never draw a correct box [A117]. EarthVQA finds counting and comprehensive analysis far weaker than yes/no judging even with masks as input [A115]. Measuring with instruments and letting language only phrase the result remains the safer design.
- **Foundation models do not beat simple supervised baselines on flood water.** On PANGAEA's Sen1Floods11 task a plain UNet outperforms every geospatial foundation model, and RemoteCLIP reaches about 55 water IoU [A120]; GEO-Bench also found RS pre-training often fails to beat ImageNet weights [A119]. This supports keeping SAR thresholding as the water instrument and keeping RemoteCLIP experimental (risk 10 in SOLUTION.md is not yet materialising).
- **The data-layer ease is not unique and should not be claimed as such.** openEO (now an OGC Community Standard) [A121] and odc-stac [A125] already turn STAC searches into district-clipped cubes. EvidEO's novelty is above that layer: the question-to-card contract, calibrated abstention and receipts for a non-expert. We should reuse these tools where they fit and record an openEO-style process graph in the receipt.
- **The method lineage is decades old, which is a strength.** Minimum-error thresholding [A109], Otsu [A108], NDWI [A110], NDVI [A111], Lee speckle filtering [A113], change vectors [A114] and the reject option [A112] are well understood and explainable to an auditor. The new part is packaging them behind a plain question with a calibrated, abstaining, receipt-backed answer.
- **Official Indian products still publish headline numbers without uncertainty.** A peer-reviewed Assam 2022 Sentinel-1 study reports a flooded area of about 33,900 sq km with no stated uncertainty [A105]; the NRSC atlases are multi-year syntheses, not answers to today's question [A046, A106]. This gap is exactly what the evidence card fills.
- **Live check, run 5.** The web UI ran end to end on live data: Barpeta flood extent (published, 0.66, just above the 0.60 line), Barpeta flood change June to July 2024 (abstained at 0.56, shown with its map), Darbhanga crop change March to April 2024 (published, 0.89, with the caveat that harvest also lowers greenness), and an ambiguous "Aurangabad" (two one-tap choices, nothing measured). A live search on 6 October 2026 also returned Sentinel-1D scenes over Barpeta, so the restored constellation [A100] is already in the catalogue.

### Run 6 evidence that strengthens or tests the claim

- **Calibration is what makes the abstention claim real, and it changed the product.** Fitting the water confidence on Sen1Floods11 hand labels showed that the uncalibrated score would have published most answers with a majority of them wrong; after fitting, the live Barpeta flood card abstains (0.46) instead of publishing (0.66). None of the RS assistants or agents in the archive reports a reliability diagram or a risk-coverage curve for its answers [A001 to A007, A094, A095]. Fitting on the production code with a published report and a per-region ledger is part of the claim now, following classic calibration practice [A126, A127, A128] and shift testing [A132].
- **The cost: today EvidEO is honest but rarely useful for Indian floods.** The novelty claim is about a trustworthy answer at a useful coverage; the run 6 numbers meet the first half and miss the second (SOLUTION risk 15). This is the most important open problem in the project.
- **Learned change detectors do not threaten the instrument choice at 10 m.** The best FC-Siam F1 on Sentinel-2 OSCD is about 58 [A142]; ChangeFormer's 90 F1 is on very high resolution LEVIR-CD [A143]; zero-shot AnyChange has 4% to 31% pixel precision [A144]. Classical difference-image thresholding with an EM posterior [A140] stays the better fit for an auditable, calibrated card.
- **Human factors work supports the card design and adds two concrete rules.** Explanations reduce overreliance only when they make checking cheaper [A137]; countable uncertainty displays beat densities on phones [A135]. Satellite emergency mapping today is delivered as expert map products [A138], which confirms the gap between existing services and a non-expert asking a question.
- **The language layer is measurable and the baseline is weak.** The rule parser's full-match rate is 0.16 on held-out districts (0.08 in Hindi). A small LoRA model constrained to a five-key JSON [A149, A150] is a plausible fix, but the claim does not depend on it: the parser only affects the "I understood" step, which the user can correct.

### Run 7 evidence that strengthens or tests the claim

- **The 2026 frontier is moving toward EvidEO's architecture, not past it.** Models that route to fixed tools (More with Less [A170], selective tool use [A172], GeoDisaster [A174], Earth-Agent-Pro [A166]) are now common. That validates "the model routes, the instrument measures" and means the claim cannot rest on tool use. What still separates EvidEO is what the user receives: per-answer scene IDs and dates, a calibrated probability, threshold abstention with a next step, and a receipt.
- **The closest new work is about reliability inside the agent.** RSure-Agent [A164] shows tool outputs are wrong in at least 22.7% of tool-dependent tasks even when the tool runs, and learns per-tool reliability to accept, ask or reject. It does not show a calibrated probability per answer to the user, and it reports no scene receipts. EvidEO's Kuro Siwo result is the same lesson measured on a physical instrument, and it is why reliability is learned per instrument and per answer regime.
- **Answer quality is capped by the instrument [A172], which is also EvidEO's main weakness today.** Water v1.1 answers about four times as many held-out chips at the 0.60 line as v1.0, with fewer wrong, but Indian chips stay hard, and positive change answers mostly abstain. The novelty claim is unaffected (the card behaves as designed); the usefulness claim (condition 2) is still the open problem.
- **Foundation models now target the beachhead tasks directly.** Galileo [A153], AnySat [A154] and Copernicus-FM [A155] cover flood and crop tasks with SAR and optical inputs; TESSERA ships open yearly embeddings [A152]; SoftCon gives small SAR encoders [A156]. None has a question interface, receipts, calibration or abstention, so they fit as calibrated second-opinion instruments behind the card, not as competitors to it.
- **Benchmarks keep exposing priors.** VRSBench answers are 83% "yes" among yes/no questions (measured in run 7), and the 2026 agent benchmarks [A166, A174] grade answers with an LLM judge, which adds its own error. EvidEO reports its numbers against non-learned baselines and hand-written test sets for the same reason.
- **New data for honest evaluation.** GEOID-Flood [A173] separates permanent water from flood water across 219 events, with a held-out set from after January 2026; it is the next external test for the water instruments, although mostly European.

### Run 8 evidence that strengthens or tests the claim

- **Grounded change answers are no longer new on their own.** QAG-360K and its VisTA model [A179] already answer plain-language change questions with a pixel mask, and expect an empty mask when nothing changed. CDVQA [A178] shows learned models answer change-ratio questions badly (about 39% right), which supports computing ratios from masks. EvidEO's claim must therefore rest on the combination: calibrated per-answer confidence, threshold abstention with a next step, Sentinel-1/2 scene IDs and dates, a re-runnable receipt, SAR-first monsoon handling, and delivery to non-experts for Indian districts. No archived system has more than two of these.
- **Small tuned models that choose tools and switch to SAR now exist.** EO-Gym [A176] trains a 4B LoRA model to call retrieval tools for older scenes and for paired optical and SAR views in a local benchmark (the SAR switch is a tool the question calls for, not a cloud test), beating a frontier model; RS-Agent [A195] and CangLing-KnowFlow [A194] show that classifying the task first and following expert workflow templates gives over 95% planning accuracy. This validates EvidEO's closed set of question types and code-chosen sensors, and removes "automatic SAR fallback" as a distinguishing claim by itself. None of them reports calibrated confidence or abstains.
- **Numbers are where agents fail.** TerraBench [A177] finds the best agent gets only 22.9% of numeric answers within tolerance, and wrong argument values are the top failure; JL1-CC&QA [A182] finds judges reject invented exact percentages. Both support EvidEO's rule that numbers come only from instruments and that parsed arguments are checked in code.
- **The field's own agenda matches EvidEO's design.** A 2026 position paper on agentic remote sensing [A193] asks for projection, time window, provenance and an uncertainty measure to be carried through every step, using flood area as its example, but offers no system, calibration method or abstention rule. EvidEO is a working instance of that agenda.
- **SAR VLMs still misread radar [A180, A192].** Even after heavy tuning, general VLMs need large SAR corpora, and a lightweight S1/S2 adaptation reaches only 0.77 F1 on per-patch flood calls with no area or confidence [A192]. This supports keeping the VLM away from backscatter.
- **Better physics exists for the weak instrument.** The Copernicus GFM Bayesian datacube method [A187] gives a per-pixel posterior water probability against each pixel's own seasonal history, plus a no-sensitivity mask, and a DEM input lifts flood F1 [A186]. Both are the concrete next steps for SOLUTION risk 15; neither is a question-answering system.
- **Reproducibility is now demonstrated, not only designed.** M6 re-ran every demo receipt from a cold start and found two defects (non-deterministic decimated reads and silent tile drop-outs) before fixing them (docs/QUALITY.md). The receipt claim is the only one in the comparison table that no other system even attempts, so its being measured matters.

### Run 9 evidence that strengthens or tests the claim

- **Abstention for flood maps now has published prior art.** SHRUG-FM [A202] (CVPR EarthVision 2026) flags unreliable foundation-model flood predictions (Sentinel-2, optical) using input out-of-distribution scores and prediction uncertainty, and rejects them. Its scores are explicitly not calibrated, it answers no questions and gives no next step. EvidEO's abstention claim is therefore narrowed again: "abstention over a calibrated measurement of a user's question, with a next step and a receipt", not "the first EO system that rejects outputs".
- **Live retrieval by an LLM agent is not new on its own.** UnivEARTH [A204] (ACL 2026 Findings) has agents write Google Earth Engine code that fetches real imagery; the best agent reaches about 40% zero-shot and 64.5% with self-debugging, with no abstention or calibration. This supports EvidEO's fixed instrument recipes and removes "fetches live data" as a standalone differentiator.
- **Deterministic re-runs of tool traces exist.** OpenEarthAgent [A205] (ECCV 2026) replays tool traces and computes NDVI, NBR and NDBI change. It overlaps EvidEO's receipt and index-change ideas, but carries no confidence, no abstention, no scene search and no SAR water or flood analysis (it uses SAR only for ship, aircraft and vehicle detection sets). The receipt claim becomes "a receipt tied to Sentinel scene IDs whose re-run is measured to reproduce the same output hash", which M6 demonstrated.
- **Pixel-grounded area answers exist.** TerraScope [A201] (CVPR 2026) answers area and change questions backed by masks from optical or SAR. It needs a GPU and has no calibration, provenance or abstention. Masks on their own are not a EvidEO novelty.
- **Faithful, step-grounded reasoning exists.** RSThinker [A206] (ICLR 2026) ties each reasoning step to an image box. EvidEO should not claim auditable reasoning in general, only auditable measurement.
- **The research agenda names EvidEO's features but does not build them.** ANASSA [A207] lists provenance, uncertainty and an "insufficient evidence" outcome as requirements without an implementation; the 2026 reasoning survey [A209] finds no RS reasoning system that evaluates calibration or abstention and no validated operational deployment. Being a working, measured system is part of the claim.
- **VLM self-reported confidence cannot replace instrument calibration.** A 2026 study [A224] finds VLM verbal confidence barely changes when the evidence changes. RSHBench [A203] measures 47% to 61% hallucination in RS VLM answers. Both support keeping the confidence meter tied to fitted instrument calibration, never to the language model.
- **Stronger trust tools are available to adopt.** Risk-controlling prediction sets [A218], conformal segmentation [A219] and conformal risk control over tool chains [A225] give finite-sample guarantees that EvidEO's Platt maps do not. They are an upgrade path, not a threat: none is packaged with Sentinel provenance for non-experts.

## 4. Closest threats to the claim (watch list)

- **SHRUG-FM [A202] plus a question interface.** It already rejects unreliable flood maps; calibrated scores and a plain-language front end would make it a direct competitor for flood extent.
- **UnivEARTH-style agents [A204] with abstention.** Live retrieval through Earth Engine plus a refusal rule would overlap; watch for follow-ups.
- **TerraScope [A201] or OpenEarthAgent [A205] adding confidence.** Either has most of the plumbing.

- **VisTA / QAG-360K [A179] with confidence.** It already returns a change mask with each answer; adding a calibrated score, abstention and Sentinel provenance would make it a direct competitor for change questions.
- **EO-Gym [A176] with calibrated answers.** It already has sensor-switching and scene-fetching tools (local benchmark, no live data, no flood-extent task); a reliability head would still overlap with its agent loop.

- **A calibrated RS VLM.** Conformal risk control [A133] and local temperature scaling [A131] are general tools; an RS VLM that ships with them and per-answer scene provenance would overlap strongly with EvidEO. None found as of run 7; ScaleEarth [A171] is the first 2026 RS model seen to abstain on calibrated uncertainty, but only for its own resolution estimate.
- **RSure-Agent [A164] with a user-facing confidence.** If its learned per-tool reliability were turned into a per-answer probability with scene provenance, it would overlap with EvidEO's trust claim. Watch for a follow-up or code release.
- **GeoDisaster [A174] adding uncertainty-aware answers**, which its authors list as future work; it already has a Sentinel-1 flood subset and Indian authors.
- **openEO and odc-stac based assistants** [A121, A125]: anyone could put a chat front end on these. Watch for one that adds confidence and abstention.

- **Google Earth AI** [A095] is now the closest threat, not just a product page: same headline (plain-language land questions answered by chaining models), Google's data and distribution. Gaps today: no refusal behaviour described, no per-answer scene receipts, high-resolution RGB rather than SAR time series, small rubric-based evaluation, US-gated. If it adds abstention and provenance, EvidEO's differentiation narrows to openness, offline deployment on Indian infrastructure, SAR-first monsoon handling and free data.
- **Earth-Agent** [A094] could add confidence and refusal with modest work. Watch for a follow-up.
- **VHM** [A078] shows honesty training for RS VLMs; a VHM-style model with calibrated scores would overlap with EvidEO's abstention claim.

- **EarthDial** [A003] is the closest model: Sentinel-1 plus Sentinel-2 plus change, and open. If a follow-up adds confidence and abstention, our differentiation narrows to receipts, live data and ease of deployment.
- **NRSC's multilingual Bhuvan chatbot** [E29] targets the same users inside ISRO. If deployed, EvidEO should position as its open, evidence-first engine rather than a rival.
- **Open EO foundation models with fine-tune recipes** [A052, A055, A057] could be wrapped by someone else into a non-expert assistant. Watch for a Prithvi or Clay based flood or crop chat tool with confidence output.
- **Google Earth AI** [E49] has the data and the distribution. Its India availability must be tracked.

## Run 9 summary of the claim

After 225 papers, every single ingredient of EvidEO exists somewhere: masks with answers [A179, A201], SAR switching [A176], live retrieval [A204], deterministic replays [A205], flood-map rejection [A202]. No archived system combines more than two of: calibrated per-answer confidence, threshold abstention with a next step, Sentinel scene receipts that are measured to reproduce, SAR-first monsoon handling, CPU or offline deployment, and plain-language delivery for Indian districts. The claim stands as a combination claim, and as the only one shown working end to end on live data with measured calibration.

---

## 5. M8 final verification (whole archive, 2026-10-10)

### 5.1 How the pass was done

1. `python tools/novelty_scan.py` searched the full text of all 225 entries for signals of the six ingredients below and wrote [docs/verification/archive_scan.csv](docs/verification/archive_scan.csv). Keyword hits only mean a paper *mentions* a topic (146 mention calibration, 163 abstention or refusal), so they were used to shortlist, not to judge.
2. 81 papers in system-building categories (rs-vlm, eo-agents, rs-benchmark, upcoming, trust-calibration, change-detection) had signals in three or more ingredients. Each was judged by hand from its entry: does *its own system* deliver the ingredient as EvidEO defines it?
3. Product claims (Google Earth AI, NRSC Bhuvan chatbot) were re-searched on 2026-10-10. No public evidence was found of Google Earth AI's geospatial reasoning being offered in India or of a deployed Bhuvan question-answering chatbot. That search was short and is not proof of absence; re-check before the final pitch.
4. Every claim below is tied to a prototype check in [docs/VERIFICATION.md](docs/VERIFICATION.md), re-run on 2026-10-10.

### 5.2 The six ingredients, defined strictly

| Key | Ingredient | Counts only if |
|---|---|---|
| C1 | Calibrated per-answer confidence | A probability attached to each user-facing answer, fitted on labelled data with a reported calibration error |
| C2 | Threshold abstention with a next step | The system declines to answer below a stated confidence line and tells the user what would fix it |
| C3 | Scene receipts that reproduce | Each answer names the exact scene IDs and dates used, and a re-run is shown to give the same output |
| C4 | SAR chosen automatically under cloud | Sensor choice is made by the system, not the user, and radar is used when optical is blocked |
| C5 | CPU or offline deployment | The full answer path runs without a GPU or a hosted LLM |
| C6 | Plain-language questions for non-experts | A non-GIS user types a question in their words (Indian place names and dates for EvidEO) |

### 5.3 Ingredient matrix for the closest systems

Yes = has it as defined; part = a weaker form (in brackets); blank = no or not described. "Full" counts only Yes.

| System | C1 | C2 | C3 | C4 | C5 | C6 | Full |
|---|---|---|---|---|---|---|---|
| EO-Gym agent [A176] | | | | tool call only | part (4B) | Yes | 2 |
| NRSC / NDEM flood maps [E3, E5, A046] | | | part (scene and date, no re-run) | Yes | Yes (government infrastructure) | | 2 |
| FloodReasonBench model [A183] | | | | | Yes (Jetson) | Yes (close-range imagery, not satellite) | 2 |
| Onboard crisis agents [A208] | part (agreement score, not calibrated) | | | part (routes to a SAR flood tool by hazard, not by cloud) | Yes (quantised, edge board) | | 1 |
| OpenEarthAgent [A205] | | | part (replays tool traces, no scene IDs) | | part (4B) | Yes | 1 |
| GeoDisaster agents [A174] | | | part (runnable workflows) | part (SAR subset, not automatic) | | Yes | 1 |
| RSure-Agent [A164] | part (per-tool reliability, internal) | part (internal reject, not shown to users) | | | | Yes | 1 |
| SHRUG-FM [A202] | (scores stated as not calibrated) | part (binary reject, no next step) | | | | | 0 |
| ScaleEarth [A171] | part (only for its resolution guess) | | | | | Yes | 1 |
| VHM [A078] | | part (learned refusal, no threshold) | | | | Yes | 1 |
| Google Earth AI [A095] | part (intervals on some model outputs) | | | | | Yes | 1 |
| Earth-Agent [A094], Earth-Agent-Pro [A166] | | | part (evidence log, A166) | | | Yes | 1 |
| UnivEARTH agents [A204] | | | | | | Yes (fetches live data via code) | 1 |
| TerraScope [A201], VisTA [A179] | | | | | | Yes (masks with answers) | 1 |
| EarthDial [A003] | | | | part (reads S1, user supplies it) | part (4B) | Yes | 1 |
| Selective tool use [A172], RS-Agent [A195], CangLing-KnowFlow [A194] | | | | | part (4B, A172) | Yes | 1 |
| GIS Copilot [A167] | | | | | | Yes (non-experts in QGIS) | 1 |
| ANASSA [A207], agentic RS position paper [A193] | requirement only | requirement only | requirement only | | | | 0 (no implementation) |
| **EvidEO** | **Yes** for water extent (Sen1Floods11) and water change (Kuro Siwo); crop change carries a visible "not yet calibrated" label | **Yes** | **Yes** (8 of 8 receipts identical, re-checked 2026-10-10 against run 8 receipts) | **Yes** (monsoon rule plus cloud fallback) | **Yes** (2 vCPU, no GPU, no hosted LLM) | **Yes** (735 districts, Indian date formats, Hindi and Hinglish keywords) | **6** |

**Result.** No system in the 225-paper archive delivers more than two of the six ingredients in full. The run 9 statement holds after the whole-archive pass. The closest, each at two, are EO-Gym (automatic SAR, plain language), the official NRSC flood products (SAR, government infrastructure) and FloodReasonBench (edge device, plain language, but not satellite data).

### 5.4 Claims in final wording

| # | Claim (final wording) | Closest prior art | What differs | Prototype evidence (VERIFICATION.md) | Status |
|---|---|---|---|---|---|
| N1 | **Combination.** EvidEO is the only system in the archive that delivers all six ingredients together, and it is shown working end to end on live Sentinel data | EO-Gym [A176], NRSC products [A046], A208 (two each) | The other four ingredients, together | Sections 2 to 7 | **Holds** (section 5.3) |
| N2 | **Numbers come only from versioned instruments**; the language layer parses and explains, never measures | Earth-Agent [A094], RS-Agent [A195], A172, OpenEarthAgent [A205] route to tools too | Fixed recipe per question type with set parameters (no free-form tool arguments, which agents get right 26% to 35% of the time [A092, A094]); confidence carried from the instrument to the card | V2: every card names `instrument` and `method`; the parser output is a five-key JSON | **Narrowed:** "tool grounding" alone is not new; the fixed, calibrated recipe is |
| N3 | **Calibrated confidence on each answer**, fitted on hand labels and published with its error | SHRUG-FM [A202] (uncalibrated reliability), RSure-Agent [A164] (internal), ScaleEarth [A171] (resolution only) | User-facing probability with a reported ECE and coverage; refit reproduces exactly | V3: water ECE 0.139 to 0.074 on held-out chips; change ECE 0.041; refit from committed rows gives identical numbers | **Holds for water; crop is labelled placeholder** |
| N4 | **Threshold abstention with a next step**, including one-tap follow-ups | SHRUG-FM [A202] (rejects, no next step), VHM [A078] (learned refusal), GeoBenchX [A093] (scores refusal) | Abstains over a calibrated measurement at a stated line (0.60), separates "needs one detail" from "not enough evidence", and offers what would help | V4: live change card abstains at 0.23 and offers two published extents; out-of-scope and ambiguous answers in 0.01 to 0.03 s | **Holds** |
| N5 | **Scene receipts measured to reproduce** | OpenEarthAgent [A205] (replays tool traces), W3C PROV-O [A222] (a model, not a system) | Receipt tied to Sentinel scene IDs whose cold re-run gives the same output hash, checked across days | V5: run 8 receipts re-run on 2026-10-10 with identical outputs | **Holds** |
| N6 | **SAR-first in monsoon, automatic** | EO-Gym [A176] (optical-to-SAR retrieval tool in a local benchmark), NRSC practice [E32] | Rule in code (monsoon months, cloud share), stated on the card in plain words | V2: `selection_notes` on the Barpeta card | **Not unique alone**; part of N1 |
| N7 | **Ease: CPU, free data, no training needed for day-one value** | A208 (edge), openEO and odc-stac [A121, A125] (data layer) | Whole answer path on a 2 vCPU machine with public catalogues; the trained model only improves parsing | V6: whole district in 54 to 98 s cold, 0.5 s warm; linear scaling with workers | **Holds as packaging**, not as a method claim |
| N8 | **Built for non-expert Indian users** | GIS Copilot [A167], GeoDisaster [A174] (Indian authors, benchmark) | District gazetteer, Indian date formats, Hindi and Hinglish, accessible mobile UI | V7: hand-written intent test 0.682 full match; keyboard walkthrough passes | **Holds as design; usefulness to real officers untested** |

### 5.5 What is not claimed

- A new model architecture, a better flood detector, or better VQA accuracy than RS VLMs.
- That tool grounding, SAR switching, live retrieval, masks with answers or rejecting bad outputs are new on their own (each has prior art, section 5.4).
- That the Barpeta 914 sq km figure is flood extent (it includes the river and wetlands; SOLUTION risks 12 and 23).
- That non-GIS users understand cards faster than maps (condition 4, untested).

### 5.6 Conditions, final status

| # | Condition (section 3) | Final status (2026-10-10) |
|---|---|---|
| 1 | No published RS assistant returns scene provenance plus calibrated confidence plus abstention | **Holds** over all 225 papers (section 5.3) |
| 2 | Instrument answers useful on Indian scenes at a reasonable coverage | **Partly.** Water v1.1 publishes 52% of Indian chips with 55% wrong when the fit never saw India; positive change answers mostly abstain. The card behaves honestly, but usefulness needs water v1.2 and Indian labels |
| 3 | Calibration transfers to India or Indian labels can be gathered | **Partly.** Degrades on new regions (India ECE 0.227 after fit); per-region refits needed |
| 4 | Non-GIS users understand cards faster than maps or chat | **Not tested.** The largest open gap in the evidence; a 10 to 15 person task-timing study is the next step |
| 5 | Public STAC plus COG fast enough for minutes, not hours, on CPU | **Holds.** 54 to 98 s per whole district cold on 2 vCPU, 0.5 s cached |
| 6 | Big platforms do not already ship this bundle in India | **Holds as far as a short search shows** (section 5.1 step 3) |

### 5.7 Final statement

EvidEO's novelty is a combination and delivery claim, verified against the whole archive: it is the only system found that gives a non-expert a plain-language answer about an Indian district with a calibrated confidence, a threshold abstention with a next step, Sentinel scene receipts that re-run identically, automatic SAR under monsoon cloud, and a CPU-only path on free data. Each ingredient exists elsewhere; the combination, built and measured, does not. The claim would weaken if any watch-list system (section 4) adds calibrated, user-facing confidence plus abstention to its existing ingredients, and it is only as useful as the instruments behind it, which for Indian floods still need work (condition 2).

## 5.8 Full-text re-check of the closest systems (2026-10-14)

Section 5.3 was judged from archive entries, many written from abstracts. On 2026-10-14 the 37 papers that the novelty claim or the paper draft depends on were re-read from raw full text (arXiv HTML or PDF converted locally, methods, tables, limitations and appendices, plus a keyword sweep for calibration, abstention, provenance, SAR, cloud, CPU and non-expert terms). 35 are now `read_depth: full`; A227 is partial (supplement not on arXiv) and A083 (Twele 2016) has no open full text. Each entry has a "Full-text check (2026-10-14)" section with section references.

### Revised matrix (full-text verdicts; Yes / part / blank)

| System | C1 | C2 | C3 | C4 | C5 | C6 | Full |
|---|---|---|---|---|---|---|---|
| Copernicus GFM ensemble [A213] | part (per-pixel likelihood, not fitted, no ECE) | part (exclusion layer; low-confidence pixels set to non-flood, not abstained) | part (scene timestamps, no re-run) | | | | 0 |
| RSure-Agent [A164] | (per tool-type success prior, not per answer) | part ("insufficient" observations with a reason; no threshold; goes to the agent, not the user) | part (sources and thresholds logged; no scene IDs or re-run) | | | part | 0 |
| EO-Gym [A176] | | | part (deterministic environment, no scene IDs in answers) | part (agent switches to SAR by question type, never by cloud) | part (offline data, H200 GPUs) | part (LLM-generated questions) | 0 |
| Onboard crisis agents [A208] | | | | part (routes floods to Sentinel-1 by hazard, not cloud) | **Yes** (whole pipeline on a 16-core ARM CPU board, no accelerator) | | 1 |
| Google Earth AI [A095] | (intervals across benchmark runs only) | (baselines told not to abstain) | (sources named, answers vary between runs) | | | **Yes** (built for non-experts) | 1 |
| TerraScope [A201] | | | | part (favours SAR features over clouded regions when the user supplies both images) | (A100) | part | 0 |
| SHRUG-FM [A202] | (scores deliberately uncalibrated, Sec. 3) | part (binary reject, next step is manual review) | | | | | 0 |
| OpenEarthAgent [A205], Earth-Agent [A094], Earth-Agent-Pro [A166] | | | part (replayable tool traces) | | | part | 0 |
| GeoBenchX [A093] (benchmark) | | part (scores a reject tool, no threshold) | part (frozen data, named datasets) | | | part | 0 |
| ANASSA [A207], agentic RS position paper [A193] | required only | required only | required only | A193 requires | | A207 requires | 0 (nothing built) |
| GeoChat, EarthGPT, EarthDial, LHRS-Bot, VHM, A179, A171, A172, A174, A183, A194, A195, A204 | | VHM part (learned false-premise rejection) | A174 part | | A179, A183 part | part | 0 |
| NRSC / NDEM flood maps [A046] (not a paper system; unchanged) | | | part | Yes | Yes | | 2 |

### What changed

1. **The claim got stronger in one way.** Read in full, no research system delivers more than one ingredient in full (A208 C5, A095 C6). Several abstract-level "part" credits were too generous (SHRUG-FM C1, EO-Gym C4 and C6, EarthDial C5, FloodReasonBench C5, whose language model runs on a remote server).
2. **It got narrower in three places,** which the claim wording must reflect:
   - C4: radar preference under cloud exists inside a model (TerraScope) and SAR routing exists by hazard type (A208) or question type (EO-Gym). EvidEO's distinct part is that the *system* detects cloud in the scene it fetched and goes to Sentinel-1 on its own.
   - C5: CPU-only LLM-plus-tools EO analysis is shown on a space-qualified board (A208). EvidEO cannot claim CPU feasibility as new, only as part of the combination.
   - C6: plain-language answers for non-experts are Google Earth AI's explicit goal. Not a differentiator alone.
3. **Closest single works to cite explicitly:** GFM ensemble likelihood (A213, three partial: per-pixel likelihood, exclusion layer, timestamps) and RSure-Agent (A164, three partial: insufficient-evidence observations, logged sources, natural-language tasks). Neither fits its confidence to labels or reports a calibration error, and neither abstains at a stated line in front of the user.
4. **The idea of combining these is not new; building and measuring it is.** A193 and A207 (2026) list provenance, uncertainty and abstention as requirements for agentic RS systems but implement none of them.

### Final wording (supersedes 5.4 N1 where they differ)

"Among the systems we read in full, none attaches a label-fitted, calibration-checked confidence to each answer and abstains at a stated threshold; the closest (GFM's per-pixel likelihood, RSure-Agent's insufficient-evidence observations) have unfitted or internal versions. EvidEO is, as far as we found, the first working system that combines that with Sentinel scene receipts shown to re-run identically, automatic radar fallback triggered by cloud in the fetched scene, a CPU-only path and plain-language questions, and it measures the result at the level of the answer."

### Number corrections found in the pass (applied to the paper on 2026-10-14)

- RSHallu: 69% hallucination-free is mPLUG-Owl3 (general model); best remote-sensing model is VHM at 68.3%. Expert scores use 300 sampled answers per model.
- GeoChat's RSVQA-LR result (printed average 90.70; sub-scores average 91.81) is not zero-shot: RSVQA-LR training questions are in its instruction set.
- The split-based thresholding citation now points to Martinis et al. 2009 (A084, read in full), which describes split selection plus Kittler-Illingworth thresholding; Twele 2016 could not be read.
- VRSBench: the 57.4% grounding figure is for unique objects only; GeoChat overall at IoU 0.5 is 49.8% (Table 4).
- A179's 82.6 mIoU in its text contradicts its own Table 2 (44.94); use the table.
- EarthGPT has no SAR metric and no BigEarthNet result; the deck's "cross-sensor MLLM evaluated on SAR and BigEarthNet" fits EarthDial, not EarthGPT (closes an open question in STATE.md).

## 6. What the full-text pass changed (batch 1, 2026-10-29)

Source: `docs/verification/paper_pass_50.md`. Ten papers read in full text (A013, A014, A033, A176, A201, A202, A204, A205, A213, A227). More batches will extend this table.

### 6.1 Implications

| Finding (where in the paper) | What it changes | Action for EvidEO | Status |
|---|---|---|---|
| VLMs are weak on precise tasks: GPT-4V IoU 0.16 vs 0.68 [A013, Table 7]; best GEOBench-VLM average 41.7% and best referring precision 0.34 [A014, Fig. 4, Table 4] | Supports "the model parses, instruments measure" | Keep the rule; cite the tables, not the abstracts | Holds |
| Hallucination is worst on image attributes such as sensor and resolution [A033, Table 1: HFIA 0.17 for two models with HFall up to 0.69] | The explanation layer, not only the measurement, needs a check | Compare sensor, resolution, date and every number in the explanation with the receipt fields before showing it | **To build** |
| Code-writing agents fail on syntax (21 to 30%) and empty collections (about 15%); feedback raises accuracy but also wrong answers (15.7 to 26.0%) [A204, Sections 4.1 to 4.4] | A better model will lower failures but not remove silent wrong answers | Run a head-to-head with a current model on our question set (section 6.2) | **To run** |
| EO-Gym and TerraScope switch between optical and SAR, as a tool call or as learned token choice [A176, A201] | Automatic SAR choice is not unique alone (N6 already says so) | Lead with answer reliability, receipts and abstention; keep SAR-first as part of the combination | Wording fixed |
| No agent paper reports confidence or abstention [A176, A201, A204, A205] | The gap we claim is real in this sample | Show calibrated answers with coverage numbers | Holds |
| Operational GFM likelihood is the mean of three algorithms' scores, checked with one Q-Q plot, no accuracy reported [A213, Sections III and V] | Even the official product ships an uncalibrated confidence index | Report agreement of two or three of our own water tests; do not call it a probability until calibrated | **To build** |
| GFM and DLR use slope, radar shadow and distance-to-drainage exclusions [A213, Sections II and IV] | A terrain mask is standard practice, and we have none | Add HAND or slope exclusion and a permanent-water layer (SOLUTION.md risks 12 and 15) | **Partly closed**: HAND and slope mask built (water v1.2, off by default, not yet refitted or run on a real scene); permanent-water layer still open. See docs/verification/nrsc_vs_evideo.md |
| Detection depends on land cover and flood type: cropland IoU 52%, tree cover and built-up 4%; riverine F1 0.69, cyclone 0.56, flash 0.55 (3 events) [A227, Section 4] | Calibration may need to vary by regime, not only by region | Test per-land-cover and per-flood-type calibration | **To test** |
| Fragmentation index below 5 went with F1 above 0.7 [A227, Section 4] | A label-free reliability signal | Test as an extra feature for the confidence head | **To test** |
| Selective rejection does not always win: SHRUG-FM is not best at 75% coverage on floods [A202, Table 2] | Our selective-prediction claim needs its own coverage curves | Publish risk against coverage per instrument | Planned (risk 8) |
| Reference products disagree by definition (SAR GFM vs optical DSWx) [A227] | Matching NRSC or GFM maps is not ground truth | Report disagreements as definitional, not as our error | Adopt |

### 6.2 How EvidEO answers the "modern AI" objection

Newer models will write working Earth Engine code more often than the 2025-era numbers in A204 and A176. The structural problems stay, so the design answers them without assuming the model gets better.

| Problem with a free-running agent | EvidEO mechanism | What is shown | What is not yet shown |
|---|---|---|---|
| Fluent answer from missing or empty data | Fixed instruments; scene IDs and dates on the card; abstain below a confidence threshold; say what would fix it | Card abstained at 0.35 on a Darbhanga scene-classification test (SOLUTION.md, instrument table) | Abstention rate on a realistic question set |
| Not repeatable | Versioned instrument, parameters and output hash in a receipt | Re-run reproduced the output hash (M6) | Reproducibility across other machines and months |
| Confidence not stated | Calibrated confidence per tile | Calibration is over-confident when moved to India by 20 points (draft, Fig. loeo) | A per-regime calibration that transfers |
| Reader cannot audit code | Plain-language card with observed versus inferred | Design stated | User test with a district officer |
| Sensor, resolution or date misdescribed | (planned) check the explanation against receipt fields | Nothing yet | Build the check, section 6.1 |
| Physical errors the model cannot know about (shadow, steep terrain) | HAND or slope exclusion (built, off by default) | Synthetic tests and live-DEM tile statistics only | Run on a real Sindhudurg scene; refit calibration with the mask on |

**Head-to-head experiment (not yet run).** Give a current frontier model free use of Earth Engine or STAC code on our question set, with no instruments. Compare with EvidEO on correctness against the NRSC or hand reference, agreement across five repeated runs, how often it abstains when the evidence is poor, and whether its stated confidence matches its error. Report coverage and risk for both. Until this is run, the claim rests on 2025-era numbers and on design reasoning only.

### 6.3 Reading rule

Take numbers from tables and body text, name the place, and check points against relative gain and preprint against peer review. Written into `archive/README.md`.
