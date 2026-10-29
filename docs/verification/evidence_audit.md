# Evidence audit of docs/reference/problem-evidence.md

Audit date: 2026-10-29. Method: every cited URL was fetched (curl with a browser user agent, plus Claude in Chrome for pages that block scripts). Numbers were then checked against the **full text and tables** of the source, not the abstract or headline. Only items marked "full text" were checked that way.

Scope so far: link status for all 49 URLs; full-text number checks for the items below. Everything else is listed under "Not yet checked".

## Link status

| Status | Entries | URL |
|---|---|---|
| **Dead (404)** | 21, 22, 23 | education.gov.in/.../RportNTFGE2013.pdf |
| **Dead (404)** | 3, 32 | nrsc.gov.in/.../SatellitebasedAnalysis-FloodMappingMonitoringinUP.pdf |
| **Dead (404)** | 8 | disasterscharter.org/.../flood-in-india-activation-582- |
| No connection | 15 | eparlib.sansad.in/.../AU1213_TGEWQ3.pdf |
| No connection | 9 | nidm.gov.in/.../ED RinadequacySDMA&DDMA.pdf |
| Live, PDF unreadable by pdftotext | 4 | un-spider.org NIDM-UNOOSA workshop slides |
| Blocks scripts, live in Chrome | 18, 30, 34-note | gijn.org, mdpi.com, wionews.com |
| Blocked by Cloudflare even in Chrome | 7 | archive.opengovasia.com |
| Still to open in Chrome | 51, 54 | esri blog June 2026, softwareadvice Picterra |

All other links returned 200. The "accessed 2026-10-04" stamp therefore cannot be true for the three 404 links above.

## Claims confirmed in the full text

| Entry | Claim | Where it was confirmed |
|---|---|---|
| 21 | ~800-1,200 educated professionals; need ~5,000-8,000 by end of 2015 | Task Force report, summary table ("Present availability" and "Estimated additional need by end of 2015") |
| 22 | ~25,000-50,000 trained users; need ~500,000 at ~50-100K per year | Same table. Also "aim to train at least 500,000 users ... over the next five years", and GTOP budget line |
| 23 | Decision-makers need orientation | Report text lists "decision-makers and even elected representatives" among the 500,000 to train |
| 2 | ~300 flood inundation maps and products in 2024 | India statement to COPUOS STSC 2025. The same text says 16 States were monitored |
| 5, 6 | Map of 2 Jun 2024 issued 04.06.2024; map of 26 Jun 2024 issued 26.06.2024; "preliminary", "No ground verification" | Both NDEM map PDFs, footer text |
| 24 | ~10 lakh jobs by 2030 | DST GSI 2025 slides |
| 26 | "Acute shortage of high caliber" | Mathur GSI 2025 slides |
| 27 | >1,000 institutions, >1.2 lakh participants | ISRO CEOS slides: 1,047 institutions, 126,686 participants |
| 29 | Chatbot framework proposed | ISPRS Annals paper ("proposes a framework"); not deployed |
| 30 | >60% cloud for most areas in the monsoon; Tamil Nadu and the north <40% | MDPI paper body text |
| 18 | Sentinel-2/Landsat via EO Browser; GEE needs coding | GIJN guide. Note: it says the Code Editor needs JavaScript and that R and Python are alternatives |
| 35 | GPT-4V mean IoU 0.16 vs 0.68 specialist | arXiv 2401.17600 text and Table 7 (specialist is MGVLF) |
| 37 | 14 VLMs benchmarked; cross-sensor gap and counting insensitivity | DisasterM3 intro and abstract |
| 39 | Provenance and audit-trail calls | UNOOSA brief; "provenance" appears in the recommendations |

## Claims that need a wording change

1. **Entries 21-23:** replace the dead MoE link with the working copy at
   `https://www.dohe-education.gov.in/static/uploads/2025/09/5c4fbf0b092193ada8857274b4ea57ef.pdf`
   (120 pages, same report). Add the PIB press release, Release ID 98953, 30 Aug 2013, as evidence that the Task Force and report exist. Note that the 500,000 figure is a *training target* over five years; the "need" wording in entry 22 is the report's own table label ("Estimated additional need by end of 2015").
2. **Entry 31 (PLOS ONE, Uday et al. 2025):** the abstract says July-August cloud of 92% and 90% "resulted in" 25% and 23% of surface water unmapped. The full text, Figure 7 caption, calls 25% and 23% the **annual average**, while July-August maximum cloud was 100%. Do not write that a quarter of water is missed *in July and August*. `SOLUTION.md` point 3 currently implies that. Safer: "cloud cover of 90-92% in July-August; JRC's optical product left about 23-25% of surface water unmapped on an annual average".
3. **Entry 36 (GPT-4V):** the R squared of 0.10 is for the "destroyed" damage category, not building damage overall. The tree-counting R squared is 0.20 in the paper's summary text but Table 8 shows 0.249. Use "about 0.2" or cite the table.
4. **Entry 34 and the WION note:** confirmed that the 95% appears only in the headline. The body text has no such figure. Keep it excluded.

## A finding that bears on the product

The same PLOS ONE paper reports that Sentinel-1 water mapping in Sindhudurg had a user accuracy of 90.45% (commission error) that "appears to be due to radar shadow caused by steep mountainous terrain". EvidEO applies no terrain mask (`aggregate.py:32` already says so on the card). This is a published example, in an Indian Western Ghats district, of the error our SAR instrument would make, and it supports adding a slope/HAND mask.

## Second pass (same day): remaining entries

Applied to `problem-evidence.md` and `SOLUTION.md`. Full-text confirmed, no change needed: 1, 2, 5, 6, 10, 11 (smart sampling by all states; the "biggest challenge" wording was not found in the PRS summary, which says claims depend on delayed yield data), 13, 14 (30-70% fewer crop cutting experiments; 96 districts in 9 states, rice, Kharif 2019), 16, 17 (65% of 7,933; 42% of 3,945 sanctioned posts; 8,268 lateral posts), 19 (13 of 101), 28, 33 (full PDF intro), 38, 41-48, 49, 50, 51, 52, 53, 55.

Corrected:
- **3 (NRSC UP report): the figure "21 districts" was wrong.** Table 2 lists 54 districts, 639,061 ha; "21" is the page number of Figure 8. Working copy is on ndem.nrsc.gov.in. Figure 5 is a calendar of map-issue days, not a delivery lag, so "no published delivery time" still stands.
- **7 (OpenGov Asia):** the article is a 27 June 2024 preview ("will launch ... on 28 June"), not a report of the launch.
- **8 (Charter 582):** now **[UNVERIFIED]**. The live page confirms the Kerala activation but does not list the four products, sensors or "14 districts" (that phrase is about school closures).
- **15 (Lok Sabha 1213):** the PDF is unreachable, but PIB carries the text (PRID 2101838): 30% mandatory weightage, paddy and wheat, Kharif 2023. It also says "no dispute has been reported", which conflicts with entry 16.
- **32:** the report states radar's advantage; it does not say NRSC "prefers" radar, and it used optical scenes too.
- **43:** dates are 24 June (1C resumes) and 29 June (1A terminated); the wording was tightened.
- **54 (Picterra):** "pricing available upon request" confirmed; "no-code" is not on the page.

Workforce figures, newer evidence: none found. DST's slides dated 7 Jan 2026 reuse the 2013 Task Force numbers plus a 2022 Mathur talk (technical professionals 6,000-10,000 available vs 15,000 needed; GIS operators 5,000-10,000 available vs 100,000 needed). The MSDE and NCAER 2025 skill-gap study has no geospatial headcount, and the WGIC report is gated by a form (not filled in).

## Still unverified

- **4** (NIDM and UN-OOSA workshop slides, Kosi "3 to 4 days"): the PDF is damaged for pdftotext and Chrome's debugger cannot attach to a PDF tab.
- **9** is now **verified** (read from screenshots of the PDF in Chrome after the user opened it past the certificate warning): SDMA 542 sanctioned, 360 filled, 182 vacant; DDMA 1,757 sanctioned, 1,700 filled, 57 vacant; 23 States/UTs replied; contractual staff excluded. The brief had quoted only the SDMA row. District-level posts are mostly filled, so the staffing evidence does not by itself show a district-level vacancy problem. A later slide has a state table "as on 01.05.2026" not yet transcribed.
- **25** (dst.gov.in page): the page body does not render for any fetch method; the "democratised access" and "skilled manpower" wording is unconfirmed. The DST slides (entry 24) do confirm the capacity-building theme.
- **8**, as above.
- **51**: exact ArcGIS user type prices still not shown (already marked in the brief).

Not re-opened because they were not in scope for this audit: archive paper summaries under `archive/`, `NOVELTY.md` and the IEEE paper draft. That is the next pass.
