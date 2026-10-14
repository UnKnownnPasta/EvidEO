---
id: 208
title: "Beyond detection: cooperative multi-agent reasoning for rapid onboard EO crisis response"
authors: "Alejandro D. Mousist, Pedro Delgado de Robles Martín, Raquel Lladró Climent, Julian Cobos Aparicio"
year: 2026
venue: "Accepted for presentation at ESA 4S Symposium 2026 (per arXiv comment); arXiv:2603.19858 (v1 March 2026); authors at Thales Alenia Space España"
link: https://arxiv.org/abs/2603.19858
code: "None stated in the text read"
category: eo-agents
era: upcoming
tags: [onboard-ai, multi-agent, edge-computing, cpu-only, qwen2-vl-2b, qwen2.5-3b, quantized, sentinel-1-flood, sentinel-2-wildfire, routing, structured-json]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2603.19858 (title, authors, date, 4S Symposium comment, abstract) and curl of https://arxiv.org/html/2603.19858v1 (agent design, models and quantisation, flood specialist using Sentinel-1, IoU 0.554 on CEMS from SenForFlood, decision agent confidence definition, 27-sample testbench, conclusions); 2026-10-14 full-text read via curl of https://arxiv.org/html/2603.19858v1 converted to text (sections read: Abstract, 1 Introduction, 2 Related Work, 3 Architecture, 4 Reference Implementation incl. all agents and tools, 5 Experimental Results incl. Table 1 and Figs 7 to 10, 6 General Discussion, 7 Conclusions)"
read_depth: "full"
takeaway: "Small quantised models (Qwen2-VL-2B at 4-bit, Qwen2.5-3B at 8-bit) plus classical and DeepLabV3+ tools run end to end on a 16-core ARM CPU board (IMAGIN-e engineering model) with no AI accelerator, routing Sentinel-2 scenes to wildfire or Sentinel-1 SAR flood specialists and fusing JSON reports into an alert with an agreement-based confidence; strong evidence that a CPU-only LLM-plus-tools EO pipeline is feasible, but the confidence is uncalibrated, routing is by hazard type not cloud, and there is no abstention or receipt"
---

# Mousist et al. 2026, onboard multi-agent EO crisis response

## Problem
Disaster alerts from satellites are slowed by downlink limits and by running every analysis on every scene. The authors want agents onboard that only run expensive analyses when a quick check suggests a hazard.

## Approach
- Architecture (Sec 3): a hierarchical, event-driven swarm in which Early Warning nodes screen scenes, specialist nodes run only when triggered, and a Decision node fuses evidence. The demonstrator (Sec 4) emulates a four-satellite diamond topology as containers, orchestrated by a fifth node with Prefect over REST.
- Early Warning agent (Sec 4.1): Qwen2-VL-2B instruct, 4-bit quantised, reads a Sentinel-2 RGB composite and emits a short JSON hypothesis (suspected hazard type plus a brief explanation).
- Specialist agents run fixed tool sequences (the authors found free tool choice caused repeated calls and loops, Sec 6), then a shared Qwen2.5-3B instruct model (8-bit) summarises tool outputs into JSON:
  - Wildfire agent (Sec 4.2): DeepLabV3+ ResNet-50 active-fire segmenter on B8, B11, B12; Normalized Hotspot Indexes with an MNDWI water mask; a burned-area tool requiring agreement of relaxed NHI and the Burned Area Index.
  - Flood agent (Sec 4.3): DeepLabV3+ ResNet-50 on Sentinel-1 VV, VH and VV/VH, trained on SenForFlood with flood, permanent water and dry classes, merged to flood vs non-flood with a fixed threshold.
- Decision agent (Sec 4.4): fuses the early hypothesis and specialist reports into a final event type, a confidence score reflecting agreement across sources, and an explanation.
- Compared with a static baseline that always runs both specialists.

## Data and benchmarks
- 27 curated samples, each a paired Sentinel-2 MSI and Sentinel-1 GRD scene of the same area, labelled wildfire, flood or no disaster (Sec 5.1).
- Hardware: engineering model of the IMAGIN-e edge computing platform, which flies on the International Space Station; ARM, 16 CPU cores, 32 GB RAM, no dedicated AI accelerator (Sec 5.1, Sec 6).
- The flood segmenter reports IoU 0.554 on the CEMS subset of SenForFlood (Fig 5 caption).

## Key results
- Table 1: no-event scenes speed-up 4.78 ± 2.54 (time reduction 73.2 ± 14.1%); event scenes 1.3 ± 0.45 (13.5 ± 30.8%). On small event scenes the early-warning overhead can make routing slightly slower than the static baseline.
- Speed-up vs scene area: global correlation 0.08, but 0.99 within no-event and 0.92 within event samples (Sec 5.2).
- Qualitative cases (Figs 7 to 10): the Decision agent rejects a wrong early wildfire hypothesis when all three fire tools report 0 km2, and the routed pipeline labels a burn scar as past rather than active fire where the baseline did not.

## Limitations
- Very small evaluation (27 samples) focused on compute; the authors explicitly do not benchmark detection accuracy and call it a proof of concept (Sec 5, Sec 6).
- Confidence is LLM-reported agreement between agents, never quantified or calibrated; there is no abstention path, only alert or no alert.
- The early-warning VLM is generic (not EO fine-tuned) and RGB only, so a cloudy optical scene could misroute the pipeline; specialists use fixed tool orders.
- Flood segmenter IoU of 0.554 is modest.
- The arXiv HTML still contains unedited draft notes (lines marked "XXX" and Spanish comments) in the related-work section; conference acceptance is for presentation at a symposium.

## What it means for EvidEO
- Adopt: the routing idea. A cheap first check (cloud fraction, quick water index) deciding whether to run the SAR chain matches EvidEO's automatic SAR fallback and keeps CPU time low. EvidEO should route on cloud and data availability, not only on hazard type.
- Adopt: small quantised models (2B to 3B) are enough for structured JSON hypotheses and summaries on a CPU-only board, consistent with EvidEO's CPU target. Fixed tool sequences beat free tool choice at this scale.
- Beat: replace agreement-as-confidence with a calibrated score, and add an abstain outcome when optical and SAR disagree.
- Novelty: weakens the claim on C5. It shows that a VLM plus LLM plus classical-tool pipeline including a Sentinel-1 SAR flood tool runs fully on CPU hardware, so "LLM-fronted SAR flood analysis without a GPU" is not new. Calibration, abstention, receipts, live archive retrieval and a non-expert question interface are absent, so EvidEO's combination claim stands.

## Full-text check (2026-10-14)
Ingredients (paper's own system as built and evaluated):
- C1 Calibrated per-answer confidence: No. The Decision agent's confidence is described only as level of agreement across sources (Sec 4.4); no numbers, no calibration.
- C2 Threshold abstention with a next step: No. Output is alert or no alert (Fig 7); a second-opinion request is only mentioned as a possible extension (Sec 6).
- C3 Scene receipts that reproduce: No. JSON outputs are said to aid traceability (Sec 4.1) but no scene IDs, dates or re-run checks are reported.
- C4 SAR chosen automatically under cloud: part. The system, not the user, sends flood hypotheses to a Sentinel-1 specialist, and the authors cite SAR's cloud independence (Sec 4.3), but the trigger is hazard type from an optical RGB screen, not optical blockage, and every sample is pre-paired S1 plus S2.
- C5 CPU or offline deployment: Yes. Full path (VLM, segmenters, LLM summariser, decision LLM) runs on a 16-core ARM CPU board with 32 GB RAM and no AI accelerator, with no hosted model (Sec 5.1, Sec 6).
- C6 Plain-language questions for non-experts: No. There is no question input; outputs include short plain-language explanations (Figs 7 to 10), which is the nearest overlap.

What the abstract-level entry got wrong or left unconfirmed:
- Table 1 speed-ups are now recovered (4.78x no event, 1.3x event).
- The board is the IMAGIN-e engineering model, whose flight unit is on the ISS; it is CPU only, which the earlier entry did not state and which makes this a full C5 match.
- The earlier entry linked its routing directly to EvidEO's SAR fallback; the full text shows routing is by suspected hazard type, not by cloud, so the match to C4 is only partial.

Novelty implications: one Yes (C5) and one part (C4). Does not exceed two, so the claim holds, but EvidEO can no longer present CPU-only LLM-plus-tools EO analysis as a novelty on its own; it must lean on the combination with C1 to C3.
