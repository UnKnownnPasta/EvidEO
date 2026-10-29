# NRSC versus EvidEO: where we win, where we trail, what to build

Follows [nrsc_method_review.md](nrsc_method_review.md) (2026-10-29). Everything about NRSC below comes from that review; nothing here compares accuracy, because the metrics, sensors and scene selection differ.

## Where EvidEO wins (design, not accuracy)
| Axis | NRSC today | EvidEO | Status |
|---|---|---|---|
| Access and speed | Analyst works scene by scene: 67 maps (2022), 91 (2023), delivered as PDF sheets for officials | Any district or box in India, any two dates, about 40 s on a CPU (Barpeta, 117 tiles) | Built and measured |
| Provenance | Preliminary-use disclaimer; no scene list per number, no re-run | Scene IDs, dates, instrument version and a receipt that re-runs to an identical hash (8 of 8 reproduced) | Built and measured |
| Stated confidence | None per map | Fitted per-answer confidence, ECE reported; abstains and names the next useful pass | Built; fitted on Sen1Floods11, weak on Indian chips |
| Cloud | Optical references need cloud-free same-day pairs (the paper says these are hard to find) | Falls back to Sentinel-1 on its own | Built |
| Reproducibility of thresholds | Variable threshold per scene set from about 200 analyst-picked pixels per class | Fixed, versioned fit (split-based, Kittler-Illingworth); same input gives same output | Built |
| Plain language | Map sheets and technical documents | Question in English, Hindi or Hinglish; evidence card | Built; real-officer usefulness untested |

## Where NRSC leads (do not claim otherwise)
RISAT-1A/EOS-04 HH/HV data and the Indian-mission pipeline; analyst clean-up with land-use, hill and hill-shadow masks, river levels and rainfall; a pre-flood permanent-water and river-channel layer; flood depth from a DEM checked against CWC gauges; official standing and about 400 scenes a year. Their 2025 automated method is tile-based Otsu plus HAND 15 m plus river-mask subtraction. Ours was the same without the last two.

## Gap list, in order
1. **HAND and slope mask. Built in this change, off by default.** `backend/evideo/terrain.py`, wired into `sar_water_otsu` v1.2 behind `terrain.enabled`.
2. Permanent-water and river-channel subtraction (Sentinel-1 temporal-minimum exclusion map per district, A211). Not built. Needed so "flood" stops including the river.
3. Lee-type speckle filter before thresholding. Not built; check it against the Sen1Floods11 fit first.
4. Land-cover mask (WorldCover, already used by the land-cover instrument) to report built-up and forest as unassessable. Not built.
5. Flood depth from DEM plus extent (NHESS 2025 method). Out of scope for now.
6. **Head-to-head on an NRSC map** (Assam June 2024 or Odisha DANA, 26.10.2024): extent overlap and area against the NDEM sheet, with the sheet named as an analyst product, not truth. Not run.

## What the HAND implementation does
Slope over 5 degrees, or HAND of 10 m or more (shrunk one pixel), makes a pixel "not assessable". Those pixels leave the threshold fit, the water map and the measured area, and the card gets `not_assessable_km2`. Missing DEM data never excludes anything; if the DEM cannot be read the tile is measured without the mask and says so.

HAND is computed from Copernicus GLO-30 on a 60 m grid covering the tile plus one tile each side: priority-flood fill, D8 flow, accumulation, channels at 1 sq km upslope, height above the channel reached. Real DEM check (live reads, 20 m tile grids):

| Tile | Not assessable | Steep | HAND >= 10 m |
|---|---|---|---|
| Barpeta, Assam (flat floodplain) | 0.5% | 0.2% | 0.3% |
| Guwahati (hills and river) | 35% | 27% | 29% |
| Sindhudurg, Konkan (target case) | 61% | 25% | 55% |

Slope is taken at 60 m on purpose: at 20 m the 30 m surface model's tree and building noise marked 10.6% of flat Barpeta as steep.

## Not verified
- **No SAR flood result with the mask on a real scene**: Planetary Computer was unreachable from this session, so only the DEM half ran live. The mask is covered by 10 synthetic tests; the Sindhudurg radar-shadow case still needs a real run.
- **Off by default on purpose.** `fit_water.py` calibrates on Sen1Floods11 chips without terrain; switching it on changes which pixels are measured, so the confidence map should be refitted with it (STATE.md convention: change the shared core and the fit together). A refit needs a DEM per chip.
- **Thresholds (5 degrees, HAND 10 m versus NRSC's 15 m) are borrowed, not validated** on Indian floodplains. The channel threshold (1 sq km) is a guess. Tile edges can leave HAND unknown (5 to 8% of cells in the three tiles above); unknown is never excluded.
- The Copernicus DSM is not hydrologically conditioned; the fill is a light substitute for MERIT Hydro HAND.
