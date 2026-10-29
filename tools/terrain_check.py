"""Check the water v1.2 terrain mask on real elevation data (no radar needed, only the public Copernicus DEM).
Runs the same terrain_for_tile() the instrument runs, on a 0.05 degree tile at 20 m, and prints how much of the
tile would be "not assessable". With --figure it also draws DEM, HAND and the mask.

    python tools/terrain_check.py                                  # three reference tiles
    python tools/terrain_check.py --bbox 73.70 16.05 73.75 16.10   # your own tile (lon/lat west south east north)
    python tools/terrain_check.py --figure docs/figures/terrain.png
Run from the repo root with the backend installed (cd backend && pip install -e ".[dev]")."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

import numpy as np  # noqa: E402
from rasterio.warp import transform_bounds  # noqa: E402

from evideo import terrain  # noqa: E402
from evideo.config import load_settings  # noqa: E402
from evideo.data.cog import read_dem_on_grid  # noqa: E402

TILES = {
    "Barpeta, Assam (flat floodplain)": (91.00, 26.30, 91.05, 26.35),
    "Guwahati (hills and river)": (91.70, 26.15, 91.75, 26.20),
    "Sindhudurg, Konkan (radar-shadow case)": (73.70, 16.05, 73.75, 16.10),
}


def analyse(bbox, res=20.0):
    crs = f"EPSG:{32600 + int((bbox[0] + bbox[2]) / 2 + 180) // 6 + 1}"
    l, b, r, t = transform_bounds("EPSG:4326", crs, *bbox, densify_pts=21)
    shape = (int(round((t - b) / res)), int(round((r - l) / res)))
    out = terrain.terrain_for_tile(crs, (l, b, r, t), shape, load_settings(environ={}))
    out["dem"] = read_dem_on_grid(crs, (l, b, r, t), shape)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bbox", nargs=4, type=float, metavar=("W", "S", "E", "N"))
    ap.add_argument("--figure", help="write a PNG with DEM, HAND and the mask for every tile")
    a = ap.parse_args()
    tiles = {"your tile": tuple(a.bbox)} if a.bbox else TILES
    results = {}
    print(f"{'tile':42} {'not assessable':>15} {'steep':>7} {'HAND>=10m':>10} {'HAND unknown':>13}")
    for name, bbox in tiles.items():
        o = results[name] = analyse(bbox)
        s = o["stats"]
        print(f"{name:42} {s['not_assessable_share']:>15.1%} {s['steep_share']:>7.1%} {s['high_hand_share']:>10.1%} "
              f"{s['hand_unknown_share']:>13.1%}")
    if a.figure:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(len(results), 3, figsize=(10, 3.3 * len(results)), squeeze=False)
        for i, (name, o) in enumerate(results.items()):
            ax[i][0].imshow(o["dem"], cmap="terrain"); ax[i][0].set_title(f"{name}\nheight (m)", fontsize=8)
            ax[i][1].imshow(np.clip(o["hand"], 0, 30), cmap="viridis_r"); ax[i][1].set_title("height above nearest drainage (0 to 30 m)", fontsize=8)
            ax[i][2].imshow(np.where(o["assessable"], 0.0, 1.0), cmap="Reds", vmin=0, vmax=1.4)
            ax[i][2].set_title(f"not assessable: {o['stats']['not_assessable_share']:.0%}", fontsize=8)
            for x in ax[i]:
                x.axis("off")
        fig.tight_layout()
        fig.savefig(a.figure, dpi=110)
        print("wrote", a.figure)


if __name__ == "__main__":
    main()
