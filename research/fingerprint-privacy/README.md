# Fingerprint auto-blur and extraction difficulty: case analysis and prior art

Status: scratch research notes (2026-10-17). Unrelated to EvidEO itself; this repo is only used as a dump.

**Evidence caveat:** WebFetch could not reach any host from the sandbox (DNS failure), so no paper was read in full. Everything below comes from search snippets. Treat numbers as leads to verify, not citations.

## 1. Prior art

### A. Extraction from photos (attack side)

| Work | What it shows | Status |
|---|---|---|
| NII / Echizen, 2017 (press: [Gulf News](https://gulfnews.com/world/asia/researchers-say-fingerprint-data-vulnerable-in-peace-photos-1.1962761), [Arab News](https://www.arabnews.com/node/1037351)) | Fingerprints reproduced from photos taken about 3 m away with a 135 mm lens, in focus and well lit. Proposed a titanium-oxide anti-capture film. | Press only. [Boing Boing](https://boingboing.net/2017/01/12/moral-panic-japanese-girls-ri.html) notes it was unreviewed. |
| [Fingerprint Extraction Using Smartphone Camera (arXiv 1708.00884)](https://arxiv.org/pdf/1708.00884) | Smartphone-camera extraction of fingerprints. | Title only seen; not read. |
| 2025-26 press on "AI steals fingerprints from selfies" ([TechSpot](https://www.techspot.com/news/112427-ai-could-steal-fingerprints-high-resolution-selfies-experts.html)) | Claims of risk at about 5 ft. | **Unverified.** No peer-reviewed source found. |
| [MUST J. Res. Dev., 2025](https://mjrd.must.ac.tz/index.php/mjrd/article/download/122/165/1092) | Public photos plus contrast enhancement and ridge extraction. | Says the resolution effect is unquantified. |
| Contactless fingerprint research: [RidgeBase](https://arxiv.org/pdf/2307.05563), NIST NISTIR 8307, [segmentation](https://arxiv.org/html/2311.15163), [TipSegNet](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11946156/) | Mature fingerphoto segmentation, unwarping and matching vs contact prints. Smartphone captures score lowest; multi-finger helps. | Cooperative captures, not ambient photos. |
| Template inversion ([Wijewardena et al., 2205.03809](https://arxiv.org/pdf/2205.03809)); [DeepMasterPrint](https://arxiv.org/abs/1705.07386v2) | Reconstruction from templates; synthetic prints matching many people. | Adjacent, not photo attacks. |

### B. Protection and obfuscation (defense side)

- [FingerSafe, arXiv 2208.10688](https://arxiv.org/pdf/2208.10688): adversarial perturbation against fingerprint matchers, with a social-media test. Closest direct prior art; results not read.
- [FingerLeak](https://github.com/Amara-ch/fingerleak) and a [Zenodo student paper](https://zenodo.org/records/22049886): MediaPipe fingertip detection, risk score, then blur/pixelate/blackout. No real-matcher validation, not peer-reviewed.
- Generic obfuscation robustness (face domain):
  - [Revelio](https://arxiv.org/html/2506.12344v1): diffusion undoes Gaussian blur, 95.9% re-identification.
  - [Privacy Blur, 2512.16086](https://arxiv.org/pdf/2512.16086): OpenCV/PIL blur approximately reversible; coarse pixelation and DP-Pix hold up better.
  - [McPherson et al., 1609.00408](https://arxiv.org/abs/1609.00408): learned models defeat blur and pixelation.

### C. Gap (novelty claim, to verify with Scholar / IEEE Xplore / BIOSIG / IJCB / ICB)

No paper found that:
1. Evaluates fingerprint auto-redaction end to end (detect, decide, redact).
2. Measures residual matchability per obfuscation against modern deep and commercial matchers.
3. Models extraction difficulty vs pixels across the finger, blur, compression and angle, with calibrated thresholds.
4. Tests reversal attacks (deblurring, diffusion restoration) on fingerprint-specific obfuscation.

## 2. Case analysis

**Attack axes:** ridge pitch about 0.5 mm, so roughly 10+ px per ridge (about 500 ppi on the fingertip; an estimate, check against standards). Photo resolution, distance and focal length set pixels on the fingertip. Finger orientation (palmar side toward lens is worst). Focus, motion blur, lighting, recompression, multi-frame/video fusion. Matcher type (partial low-quality prints may still enable spoofing or population filtering).

| Case | Capture | Expected risk | Redact? |
|---|---|---|---|
| 1 | Selfie, fingers toward lens, within 1 m, 12 MP+ | Medium-high | Yes |
| 2 | Peace sign at 3 m, DSLR tele lens | High (matches NII claim) | Yes |
| 3 | Group photo recompressed to about 1-2 MP | Low | Probably not; measure |
| 4 | Video | Elevated (frame fusion) | Yes |
| 5 | Evidence/forensic photos | Mixed | Must be auditable |
| 6 | Back of hand, gloves | Negligible for fingerprints | No |

| Redaction method | Expected outcome | Evidence |
|---|---|---|
| Gaussian blur | Weak; restoration may recover detail | Face-domain only |
| Coarse pixelation | Better (information destroyed) if below ridge Nyquist | Face-domain only |
| Solid fill | Strongest, utility cost | Trivial; check metadata/thumbnails |
| Downsample fingertip | Irreversible, cheap | Needs measurement |
| Adversarial noise (FingerSafe) | Keeps appearance; fragile to new models and JPEG | FingerSafe |
| Inpainting / synthetic ridges | Risk of hallucinating real-looking prints | None found |

**Pipeline failure modes:** missed fingertips (occlusion, odd angles, skin-tone bias in detectors); mask too tight so ridge detail bleeds; originals surviving in EXIF thumbnails, edit history or caches.

## 3. Proposed paper

**Title idea:** *How Blurry Is Blurry Enough? Quantifying Fingerprint Exposure in Photos and the Adequacy of Automatic Redaction.*

1. Data: consented photos of researchers' own hands at controlled distances (0.5, 1, 2, 3 m), megapixel levels and angles; live-scan references from the same participants; public contactless data (RidgeBase). Ethics review first; never publish extracted prints.
2. Exposure metric: matcher-agnostic quality (NFIQ2 or similar) plus match rate, as a function of pixels-per-ridge.
3. Redaction suite from the table, with the auto-detect front end evaluated alone (fingertip recall).
4. Adversary tiers: naive (commercial matcher), adaptive (deblur/diffusion), multi-frame.
5. Outputs: decision rule (pixels-per-ridge threshold and method/strength) and an open-source tool.
6. Ethics: dual-use. Release thresholds and defensive code, not a ready fingerprint-lifting pipeline.

## 4. Open questions

- Standalone paper or tied to a redaction product?
- Ethics approval and participants available for original data? Otherwise fall back to synthetic hands and public datasets (weaker).
