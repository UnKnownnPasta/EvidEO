# Tellio technical guide, from zero

**Who this is for:** you know Python and JavaScript. You know nothing about satellites, remote sensing, GIS, statistics for classifiers, or queues. After one read you should be able to open any file in `backend/evideo/` and know why it exists.

**How it is organised:** Part 1 is the domain you are missing (what the data is). Part 2 follows one question through the system in order. Part 3 explains the maths we use to say "how sure are we". Part 4 is the new terrain mask (HAND). Part 5 is the code map, how to run and test it, and a glossary. Code shown here is simplified; the real file is named under each heading.

---

## Part 1. The domain you are missing

### 1.1 What a satellite image is, in programmer terms
A satellite image is a 2D array (`numpy` array of floats) plus two pieces of metadata:
- **a CRS** (coordinate reference system): which map projection the rows and columns live in. Latitude/longitude is `EPSG:4326`. For measuring areas we use **UTM** (`EPSG:32646` for eastern India), where one pixel step is a fixed number of metres.
- **a transform**: a small matrix (an "affine transform") that converts `(row, col)` to `(x, y)` in that CRS. Python library `rasterio` holds both.

A pixel is a square of ground, for example 20 m x 20 m = 0.0004 sq km. "Area of water" is therefore `number_of_water_pixels * pixel_area`. Almost every number Tellio reports is that one multiplication, so the hard part is deciding which pixels are water.

### 1.2 The two satellites we use (Copernicus Sentinel)
| | Sentinel-1 ("radar", S1) | Sentinel-2 ("optical", S2) |
|---|---|---|
| What it does | Sends its own microwave pulse and listens to the echo | Takes a colour photo with 13 spectral bands (a normal camera plus infrared) |
| Works at night / through cloud? | **Yes** | **No**: clouds block the view |
| Why it matters in India | Monsoon (June to September) is cloudy over most of India, exactly when floods happen | Great in dry season |
| Pixels | Backscatter strength per polarisation | Reflectance per band |
| Free? | Yes, public | Yes, public |

Both revisit a given spot every few days (the exact gap depends on place and which satellites are in orbit). No tool, ours or anyone's, can see a flood on a day when no satellite passed over it. What we control is how fast the answer comes once data exists.

### 1.3 How radar sees water (the idea behind our main instrument)
Radar sends a pulse at a slant angle. A **calm water surface acts like a mirror**: the pulse bounces away from the satellite, so almost nothing returns and the pixel is **dark**. Land is rough, scatters energy back, and is brighter. So "dark pixel in a radar image" is a good first guess for "water".

Backscatter values span a huge range, so they are shown in **decibels (dB)**: `db = 10 * log10(linear)`. Typical numbers: water -20 dB or lower, land -10 to -5 dB. A **polarisation** is the orientation of the radar wave. **VV** (sent vertical, received vertical) is the standard; **VH** (cross-polarised) helps with rough water and flooded vegetation. The code reads both (`instruments/water.py`).

Radar traps (we name them on every card): radar **shadow** (hills block the beam, dark but not water), smooth tarmac or sand (dark but not water), water under dense plants (not dark), and **speckle** (random grain in every radar image, handled by dropping blobs under 10 pixels).

### 1.4 How optical sees water and plants
Optical indices are just arithmetic on two bands:
```python
ndwi = (green - nir) / (green + nir)    # water if > 0 (McFeeters)
ndvi = (nir - red)  / (nir + red)       # plants: high value = green and healthy
```
We use NDWI for water and NDVI for crop decline (`instruments/vegetation.py`). A "cloud mask" band (**SCL**) tells us which pixels are cloud or shadow; we only use clear pixels.

### 1.5 Where the data lives: STAC and COG
- **STAC** is a standard JSON web API for searching satellite scenes ("give me Sentinel-1 over this box between these dates"). Think of it as a REST search endpoint. We query three public ones with automatic failover (`data/stac.py`).
- **COG (Cloud Optimized GeoTIFF)** is an image file organised in internal blocks so you can fetch just one rectangle with HTTP range requests, like reading bytes 1000..2000 of a huge file. So we **never download a scene** (about 1 GB); we download only the few hundred KB covering the district (`data/cog.py`).

### 1.6 District boundaries
A bundled GeoJSON of 735 Indian district outlines (`resources/districts.json`, from geoBoundaries, ODbL licence) lets "Barpeta" become a polygon. `gazetteer.py` looks names up; if two districts share a name (Aurangabad in Bihar and in Maharashtra) the system asks which one instead of guessing.

---

## Part 2. One question, end to end

Use the question *"How much of Barpeta was under water on 2024-07-11?"*

```
Browser (HTML+JS) --POST /v1/queries--> FastAPI --parse--> tile jobs --> queue --> workers
                                                              |                      |
   <-- SSE stream of tile results <------------ aggregate <---+--- instrument <-- COG reads
```

### 2.1 Frontend (`frontend/index.html`, `app.js`, `styles.css`)
Plain HTML/CSS/JS with **no build step and no framework**. The page is a three-step wizard with the map always on the right: (1) a single question box; (2) a configuration screen, filled by `POST /v1/parse` (parse only, reads no pixels), showing the parsed analysis, district and dates as editable fields plus the read-only technical settings (instrument and version, satellite rule, tile count, publication threshold, terrain mask), re-parsed live whenever you change a field and blocking the Run button while anything is missing or ambiguous; (3) `fetch('/v1/queries', {method:'POST', ...})` to run it, then it opens an `EventSource` (Server-Sent Events: a one-way stream from server to browser over plain HTTP, simpler than WebSockets) on `/v1/jobs/<id>/events`. Each tile result updates a progress bar; the final event is the evidence card. The map is **Leaflet** (a JS map library, bundled in `frontend/vendor/` so it works offline). The UI is built for accessibility: keyboard-only use, contrast of at least 4.5:1, 44 px touch targets, light and dark themes.

### 2.2 API (`backend/evideo/api/main.py`)
**FastAPI** (a Python web framework, like Express for Python) with **Pydantic** models (`models.py`) that validate every request and response. Endpoints you will meet: `POST /v1/parse` (parse and describe the configuration, no data read), `POST /v1/queries` (start), `GET /v1/jobs/{id}/events` (SSE stream), `GET /v1/receipts/{id}`, `GET /v1/masks/{name}` (the PNG overlays), `GET /v1/regions` (district search). The API is **stateless**: any replica can serve any request because job state lives in the queue.

### 2.3 Understanding the question (`parser.py`, `gazetteer.py`)
A **rule-based parser** (keyword lists in English, Hindi and romanised Hindi "Hinglish", plus multi-format date parsing) turns text into a `ParsedQuery`:
```python
ParsedQuery(intent="water_extent", region="barpeta-assam", windows=[2024-07-05 .. 2024-07-17], ...)
```
Dates become a window of plus or minus 6 days, because satellites do not pass every day. Anything unsupported ("count the boats", "will it flood tomorrow") is refused with an example question in about 0.01 s and **no data is read**. The parse is shown back to the user ("I understood your question as...") before the answer, so a misread is caught immediately.

**Important design rule:** the language layer **never produces a number**. An optional LoRA-trained vision-language model (`training/lora/`) could replace the keyword parser, but it may only output a five-key JSON; the same deterministic code then resolves places and dates. A wrong parse can cost the user a correction, never a wrong map.

### 2.4 Tiling (`tiling.py`)
The district is cut into a fixed global grid of squares of 0.05 degrees (about 5.5 km). Barpeta is 117 tiles. Tile IDs are deterministic (`z0.05_col_row`), so two users asking about overlapping areas share tiles. Only tiles touching the district outline are queued, and inside each tile the outline is rasterised into a boolean mask so pixels outside the district are not counted. **Why tiles:** each is independent, so they run in parallel, can be cached, and can be retried alone.

### 2.5 Queue and workers (`jobqueue.py`, `worker.py`, `cache.py`)
- **Queue:** a list of pending tile jobs. In development an in-process thread pool (no extra software). In production **Redis** (an in-memory data store): jobs go in a list, workers do blocking pops, and a *visibility timeout* puts a job back if a worker dies (at-least-once delivery). Jobs are idempotent, so running one twice is harmless.
- **Worker** (`worker.py`): take a job, look in the **cache** (key = hash of tile, instrument version, dates, region), otherwise run the instrument and store the result. A failing tile is retried once after 3 s.
- **Scaling:** add worker processes. Measured: 2.0, 4.0, 7.8 tiles/s for 1, 2, 4 workers. Threads in one Python process do not speed up the maths (the GIL), processes do.

### 2.6 Choosing scenes (`data/select.py`, `data/provider.py`)
Rules, all written as plain Python and each producing a sentence shown on the card:
1. June to September and a water question: **radar first** (cloud cannot block it).
2. Otherwise optical if the tile's own cloud share is under 30%; if not, fall back to radar automatically.
3. Pick the scene closest to the middle of the requested window, within 12 days.
4. For change questions, pair two Sentinel-1 scenes from the **same orbit** (same viewing angle), so differences are real, not geometry.

A catalogue search is cached per 1 degree cell, so all 117 tiles share one search.

### 2.7 Reading pixels (`data/cog.py`)
Opens the COG by URL, converts the tile's lon/lat box to the raster's CRS, reads just those blocks, resizes to 20 m with numpy. **Determinism fix (run 8):** letting the GDAL library downsample gave different pixels under concurrent reads, which broke reproducibility, so we always read at native resolution and resize ourselves in numpy. Reads retry 4 times; a tile that still fails is reported as an error, lowers confidence, and the card says "N tiles could not be read".

### 2.8 The measurement: the water instrument (`instruments/water.py`)
This is the core. A function that gets a tile of VV (and VH) in dB and returns a boolean "water" array. The hard part is the **threshold**: how dark is dark? It differs per scene (wind, incidence angle, season), which is why NRSC's analysts hand-pick thresholds per scene. We **fit it automatically per tile**:

1. Cut the tile into about 1 km blocks (half-overlapping).
2. Keep only blocks that are **bimodal**, meaning their histogram clearly has two humps (a water hump and a land hump). A block that is all land teaches us nothing. The test: split with **Otsu's method** (pick the cut that best separates two groups), then require **Ashman's D** at least 3 (the two humps are far apart relative to their spread), class means at least 3 dB apart, and the smaller class at least 10% of the block.
3. Pool the kept blocks and run the **Kittler-Illingworth minimum-error threshold** on the pool. (Otsu assumes equal spread of the two classes; radar land is far more variable than calm water, which pulled Otsu to -10.8 dB on a clearly bimodal Barpeta histogram where the true valley was near -14 dB. This was a real bug found on live data.)
4. If no block is bimodal, repeat on the 3 x 3 neighbouring tiles; if that also fails, use a default (-17 dB) and say so on the card.
5. A pixel is water if **VV is below its threshold OR VH is below its own**. Remove blobs under 10 pixels (speckle).

Simplified:
```python
def otsu(values):                          # real code: instruments/common.py
    hist, edges = np.histogram(values[np.isfinite(values)], bins=256)
    centres = (edges[:-1] + edges[1:]) / 2
    w0 = np.cumsum(hist); w1 = w0[-1] - w0
    m = np.cumsum(hist * centres)
    mu0 = m / w0; mu1 = (m[-1] - m) / w1
    return centres[np.argmax(w0 * w1 * (mu0 - mu1) ** 2)]   # cut with the biggest between-class gap

water = (vv_db < t_vv) | (vh_db < t_vh)
```
The result also carries `fit` (the thresholds and why) and a **raw quality score** (Part 3).

Sibling instruments: `sar_logratio_change` (two same-orbit radar scenes; new water = water after, not water before, and the signal dropped at least 3 dB: a **log-ratio**, which in dB is just subtraction), `ndvi_difference` (crop decline = NDVI fell by at least 0.15 on pixels that were green before), `index_caption` (shares of water, dense and sparse vegetation), `zero_shot_landcover` (a CLIP model, **experimental**, the only learned instrument).

### 2.9 Aggregating into a card (`aggregate.py`)
Sum the tile areas; propagate each tile's uncertainty (summed, the conservative case, because tiles share one scene and method); run the **calibration map** (Part 3) to get the final confidence; compare with the publication threshold (**0.60**). If it clears: a published **evidence card** with number, scenes, dates, map overlay, plain-language caveats. If not: "Insufficient evidence", the reason, and what would help (for a change question, two buttons for the water extent on each date). It also abstains if fewer than half the tiles could be measured.

### 2.10 Receipts (`receipt.py`)
After every answer we build a JSON "receipt": the parsed question, every tile's scenes, parameters and values. Then `sha256(json.dumps(receipt, sort_keys=True))`. Same inputs must give the same hash. We tested it: 8 receipts written on 8 October were re-run in a fresh container on 10 October, **8 of 8 hashes identical**. This is how a district officer's number can be audited later.

---

## Part 3. How we say "how sure are we"

### 3.1 Raw quality score
The instrument asks: "if my threshold were 1 dB off, would my area change by more than 20%?" It counts the share of pixels within 1 dB of the threshold. Many pixels near the threshold means the area is fragile. Formally `P(area within +/-20%) = erf(0.2 / (sd_rel * sqrt 2))`, multiplied by an evidence factor (0.75 to 1.0: lower when we fell back on a default threshold). This number is **not yet a probability**; it is a score.

### 3.2 Calibration: turning a score into a true probability
Take a labelled dataset where humans drew the true flood maps (Sen1Floods11: 446 hand-labelled chips, 68 of them in India; Kuro Siwo for change). Run our exact production function on each chip, record the raw score and whether the area ended up within 20% of the human map. Then fit a small curve that maps score to observed hit rate. We choose between **Platt scaling** (a logistic curve, 2 numbers) and **isotonic regression** (a monotone staircase) by error on a validation split. The fitted maps live in `config/calibration/*.json`; the fitting code (`training/calibration/fit_water.py`) imports the same `classify_sar_water` the app uses, so the calibration belongs to exactly the running code.

**ECE (expected calibration error)** is the standard score of this: bin answers by stated confidence, compare stated confidence with actual hit rate in each bin, average the gaps. Lower is better. Water ECE improved from 0.139 to 0.074 on held-out chips. The reliability plot (`training/calibration/reports/sar_water_otsu_reliability.png`) shows it; the right panel (risk-coverage) shows error among the answers we choose to publish at each cut-off.

### 3.3 Abstention
`confidence < 0.60` means no number. The line is a policy choice from the risk-coverage curve. This is why the first real calibration changed the product: the uncalibrated Barpeta flood answer looked confident at 0.66 and would have been published; after calibration the same data scored lower and the card abstained, until we added VH to the instrument and refitted. We report this openly.

### 3.4 What can still go wrong (we show these)
Calibration on world-wide chips transfers imperfectly: held out of India, the water fit published 52% of Indian chips at a 55% wrong rate. Hence "needs per-region refits and Indian labels" on our roadmap. Crop-change confidence has no fitted map (no open Indian crop labels); the card says "not yet calibrated".

---

## Part 4. The terrain mask (water v1.2): what HAND is

### 4.1 The problem
Steep terrain throws radar **shadow**: dark pixels on a hillside that are not water. In the Western Ghats and the Konkan, a threshold instrument will count them. A real flood also cannot happen on a pixel that is 40 m above the nearest river. So we mark those pixels **"not assessable"**: not "dry", not "wet", simply outside what radar can judge, and we report their area.

### 4.2 Two terrain quantities (`backend/evideo/terrain.py`)
Needs a **DEM** (digital elevation model: a raster of heights). We read the public **Copernicus 30 m** DEM straight from its S3 bucket with the same COG reader.
- **Slope**: steepness in degrees, from the height gradient (`np.gradient`). Over 5 degrees is excluded (a cut taken from the published DLR and Copernicus GFM flood chain).
- **HAND (Height Above Nearest Drainage)**: for each pixel, how many metres higher it sits than the river channel its rain would drain to. A hilltop at 300 m can have HAND 5 m in one valley and 80 m in another; plain elevation cannot say that, HAND can. HAND of 10 m or more is excluded (Copernicus: 10 m; NRSC: 15 m).

### 4.3 How HAND is computed, step by step
It is a small graph algorithm on the height grid:
1. **Fill pits.** DEMs have fake holes where water would be trapped. A *priority-flood* walks inward from the edges using a min-heap (`heapq`), raising every pit to the level of its lowest spill point (plus a tiny epsilon) so every cell has a downhill path to the edge. `terrain._fill`.
2. **Flow direction (D8).** Each cell points to whichever of its 8 neighbours is steepest downhill.
3. **Flow accumulation.** Process cells from highest to lowest; each passes its count of upstream cells to the cell it flows into. A cell's accumulation equals the number of cells draining through it.
4. **Channels.** Cells draining at least 1 sq km are "river".
5. **HAND.** Process cells from lowest to highest; a channel cell's reference is its own height; any other cell inherits the reference of the cell it flows into. `HAND = height - reference`.
Cells whose water leaves the map before meeting a channel get `NaN` (unknown). **Unknown is never excluded**: missing information is reported, not guessed.

### 4.4 Practical details that matter
- Computed on a coarse 60 m grid over the tile **plus one tile on each side**, so a river just outside the tile still drains it. Python loops over cells are slow, so coarse is a deliberate speed choice (about 1 to 3 s per tile).
- Slope is also taken at 60 m. At 20 m, tree and building noise in the 30 m surface model made 10.6% of **flat Barpeta** look steeper than 5 degrees; at 60 m, 0.2%.
- The mask is shrunk by one pixel (`erode1`) so a thin edge does not remove real flood water.
- Excluded pixels are left out of the threshold fit (so shadows cannot pull the threshold), out of the water map, and out of the "measured area".

### 4.5 Status and honesty
Built, tested (10 tests), checked on real DEM data (table in `docs/REPORT.md`), wired into the instrument behind a config switch that is **off by default**. Why off: the confidence calibration was fitted without the mask; changing which pixels are measured should be done together with a refit. Not yet run on a real radar scene (the sandbox could not reach the catalogue). Thresholds are borrowed from other services, not validated on Indian floodplains.

Try it with no radar needed: `python tools/terrain_check.py --figure out.png`.

---

## Part 5. Code map, running, testing, vocabulary

### 5.1 Where things are
```
backend/evideo/
  api/main.py        web endpoints (FastAPI)          models.py     Pydantic data shapes
  parser.py          keywords -> ParsedQuery          gazetteer.py  district names and outlines
  tiling.py          global tile grid                 jobqueue.py   in-process and Redis queues
  worker.py          one tile job                     cache.py      tile result cache
  aggregate.py       tiles -> evidence card           receipt.py    JSON + sha256
  calibration.py     score -> probability             config.py     YAML + env overrides
  terrain.py         slope, HAND, assessable mask     livecheck.py  run live questions in a script
  data/              stac.py scene.py select.py provider.py cog.py   (finding and reading pixels)
  instruments/       water.py vegetation.py landcover.py common.py   (all the measuring)
frontend/            index.html app.js styles.css (+ vendored Leaflet)
config/              evideo.yaml  calibration/*.json (fitted confidence maps)
training/            calibration fits, LoRA parser pipeline, evaluation, Colab notebook
tools/               demo.py reproduce.py loadtest.py terrain_check.py screenshots.py ...
archive/             227 verified paper notes + index.csv (the research behind each decision)
docs/                this guide, REPORT.md, ARCHITECTURE.md, VERIFICATION.md, QUALITY.md
```

### 5.2 Run it
```bash
cd backend && python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m uvicorn evideo.api.main:app --reload     # UI at http://localhost:8000
python -m pytest -q                                 # offline tests
python -m evideo.livecheck "How much of Barpeta was under water on 2024-07-11?"   # live, needs internet
EVIDEO_TERRAIN__ENABLED=true python -m evideo.livecheck "How much was under water on 2024-07-11? bbox: 73.70, 16.05, 73.75, 16.10"
```
Any config key can be overridden by an environment variable: `EVIDEO_<SECTION>__<KEY>` (double underscore for nesting).

### 5.3 How the tests work
Tests run **offline**. A `FakeProvider` in `tests/test_instruments.py` serves synthetic numpy arrays on a real UTM grid (for example a tile whose left 40% is -21 dB "water" with noise), so thresholds, areas, clipping, overlays and abstention are checked exactly. Terrain tests build synthetic valleys and hillsides and assert that HAND equals the known height above the channel. Live behaviour is checked separately by `tools/demo.py`, `tools/reproduce.py` and `tools/terrain_check.py`.

### 5.4 Glossary
| Term | Meaning |
|---|---|
| AOI | Area of interest: the district or box asked about |
| Backscatter / sigma0, gamma0 | Radar echo strength, with two slightly different normalisations (about 1 dB apart) |
| Bimodal | A histogram with two humps (here: water and land) |
| CRS / UTM | Map projection / the metre-based projection used for areas |
| DEM / DSM | Elevation raster / one that includes trees and buildings (Copernicus is a DSM) |
| ECE | Expected calibration error: average gap between stated and actual hit rate |
| HAND | Height above nearest drainage |
| IoU | Overlap of two masks: intersection divided by union |
| Isotonic / Platt | Two ways of fitting a score-to-probability curve |
| Kittler-Illingworth | Threshold method allowing the two classes different spreads |
| NDWI / NDVI | Water / vegetation index from two optical bands |
| NRSC / NDEM / Bhuvan | India's national remote-sensing centre / its disaster map service / its geoportal |
| Orbit | A satellite's repeat path; "same orbit" keeps viewing geometry equal |
| Polarisation (VV, VH) | Orientation of the radar wave sent and received |
| Receipt | JSON plus hash proving what was measured from which scenes |
| SSE | Server-Sent Events: one-way server-to-browser stream |
| STAC / COG | Searchable scene catalogue standard / range-readable image file format |
| Tile | One 0.05 degree square, the unit of parallel work and caching |
