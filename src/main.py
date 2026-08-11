from __future__ import annotations
import argparse
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from .ndvi import calculate_ndvi
from .validation import validate_ndvi


def run(red_path: Path, nir_path: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    with rasterio.open(red_path) as red_src, rasterio.open(nir_path) as nir_src:
        if (red_src.crs != nir_src.crs or red_src.transform != nir_src.transform or
                red_src.width != nir_src.width or red_src.height != nir_src.height):
            raise ValueError("Bands are not co-registered. Align/reproject them before NDVI.")
        red = red_src.read(1)
        nir = nir_src.read(1)
        profile = red_src.profile.copy()
    ndvi = calculate_ndvi(red, nir)
    stats = validate_ndvi(ndvi)
    profile.update(
    driver="GTiff",
    dtype="float32",
    count=1,
    nodata=np.nan,
    compress="deflate"
    )
    
    ndvi_path = output_dir / "ndvi.tif"
    with rasterio.open(ndvi_path, "w", **profile) as dst:
        dst.write(ndvi, 1)
    stats_path = output_dir / "ndvi_statistics.json"
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(ndvi, vmin=-1, vmax=1)
    ax.set_title("Sentinel-2 NDVI")
    ax.set_axis_off()
    fig.colorbar(im, ax=ax, label="NDVI")
    fig.tight_layout()
    fig.savefig(output_dir / "ndvi_map.png", dpi=180)
    plt.close(fig)
    return stats


def cli():
    p = argparse.ArgumentParser(description="Calculate and validate NDVI from co-registered Sentinel-2 B04/B08 rasters.")
    p.add_argument("--red", type=Path, required=True)
    p.add_argument("--nir", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("outputs"))
    args = p.parse_args()
    print(json.dumps(run(args.red, args.nir, args.output), indent=2))

if __name__ == "__main__":
    cli()
