"""Extract the red "Flood / Rain Affected" layer from an NRSC GeoPDF map sheet into georeferenced masks.

Georeferencing comes from the main frame's own /Viewport and /GPTS entries. The result is checked against the
known position of towns printed on the sheet, and the run stops if they disagree.

Run from the repo root: python research/flood_area/nrsc_extract.py <sheet.pdf> <out_dir> [dpi]
Writes nrsc_flood.tif and nrsc_river.tif (uint8, EPSG:4326). Labels and lines drawn over the flood layer are
lost, so the area is a small underestimate.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_bounds
from scipy import ndimage

# Approximate coordinates of towns marked on the Assam sheet, used only to test georeferencing.
TOWNS = {"Jorhat": (26.757, 94.203), "Tezpur": (26.633, 92.800), "Golaghat": (26.519, 93.960), "Itanagar": (27.085, 93.605)}
TOLERANCE_DEG = 0.04


def classify(rgb):
    """rgb: 3 x H x W uint8. Legend colours are pure red and a saturated blue; anti-aliased edges are left out."""
    r, g, b = [c.astype(int) for c in rgb[:3]]
    return (r > 190) & (g < 70) & (b < 70), (b > 200) & (r < 60) & (g > 90) & (g < 150)


def viewport(pdf, name="MainFrame"):
    """Page box and lat/lon corners of a named viewport. Names are stored as UTF-16 in the PDF."""
    raw = Path(pdf).read_bytes()
    label = b"\xfe\xff" + name.encode("utf-16-be")
    m = re.search(rb"/BBox \[([^\]]+)\]/Name \(" + re.escape(label) + rb"\)/Measure.*?/GPTS \[([^\]]+)\]", raw, re.S)
    if not m:
        raise ValueError(f"viewport {name} not found")
    box = [float(x) for x in m.group(1).split()]
    pts = [float(x) for x in m.group(2).split()]
    return box, min(pts[0::2]), max(pts[0::2]), min(pts[1::2]), max(pts[1::2])


def check_towns(rgb, transform):
    """Green town dots must land on the towns' real positions. Town markers are the only pure green on the sheet."""
    r, g, b = [c.astype(int) for c in rgb[:3]]
    lab, n = ndimage.label((g > 200) & (r < 90) & (b < 90))
    if n == 0:
        raise ValueError("no town markers found")
    centres = np.array(ndimage.center_of_mass(np.ones_like(lab), lab, range(1, n + 1)))
    lons, lats = transform * (centres[:, 1] + 0.5, centres[:, 0] + 0.5)
    report = {}
    for town, (lat, lon) in TOWNS.items():
        d = np.hypot(lats - lat, lons - lon).min()
        report[town] = round(float(d), 4)
        if d > TOLERANCE_DEG:
            raise ValueError(f"{town} is {d:.3f} deg from the nearest marker; georeferencing is wrong")
    return report


def self_check():
    rgb = np.zeros((3, 1, 3), dtype=np.uint8)
    rgb[:, 0, 0] = (255, 0, 0)
    rgb[:, 0, 1] = (0, 112, 255)
    rgb[:, 0, 2] = (255, 255, 255)
    flood, river = classify(rgb)
    assert flood.tolist() == [[True, False, False]] and river.tolist() == [[False, True, False]]


def main(pdf, out, dpi=300):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (x0, y0, x1, y1), lat0, lat1, lon0, lon1 = viewport(pdf)
    with open(pdf, "rb") as f:
        head = f.read()
    page_h = float(re.search(rb"/MediaBox \[\s*[\d.]+ [\d.]+ [\d.]+ ([\d.]+)", head).group(1))
    s = dpi / 72
    left, top, w, h = round(x0 * s), round((page_h - y1) * s), round((x1 - x0) * s), round((y1 - y0) * s)
    png = out / "frame.png"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-x", str(left), "-y", str(top), "-W", str(w), "-H", str(h), "-png", "-singlefile",
                    str(pdf), str(png.with_suffix(""))], check=True)
    with rasterio.open(png) as ds:
        rgb = ds.read()
    h, w = rgb.shape[1:]
    transform = from_bounds(lon0, lat0, lon1, lat1, w, h)
    towns = check_towns(rgb, transform)
    flood, river = classify(rgb)
    prof = dict(driver="GTiff", height=h, width=w, count=1, dtype="uint8", crs="EPSG:4326", transform=transform, compress="deflate")
    for name, m in (("nrsc_flood", flood), ("nrsc_river", river)):
        with rasterio.open(out / f"{name}.tif", "w", **prof) as dst:
            dst.write(m.astype("uint8"), 1)
    rows = np.arange(h)
    lat = lat1 - (rows + 0.5) * (lat1 - lat0) / h
    km2 = abs(transform.a * transform.e) * 111.32**2 * np.cos(np.radians(lat))
    info = {"size": [w, h], "pixel_deg": transform.a, "pixel_m_approx": round(transform.a * 111320 * math.cos(math.radians(26.7))),
            "town_error_deg": towns, "flood_km2": round(float((flood.sum(1) * km2).sum()), 1), "river_km2": round(float((river.sum(1) * km2).sum()), 1),
            "frame_km2": round(float((w * km2).sum()))}
    (out / "nrsc_extract.json").write_text(json.dumps(info, indent=1))
    png.unlink()
    print(json.dumps(info))


if __name__ == "__main__":
    self_check()
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 300)
