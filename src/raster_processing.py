from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import Resampling, reproject


def read_band(path: str | Path):
    """Read the first raster band and return its data and geospatial metadata."""
    with rasterio.open(path) as src:
        return (
            src.read(1),
            src.profile.copy(),
            src.crs,
            src.transform,
        )


def align_to_reference(
    source_path: str | Path,
    reference_path: str | Path,
) -> np.ndarray:
    """
    Reproject/resample a source raster onto the exact grid
    of a reference raster.
    """
    with rasterio.open(reference_path) as ref, rasterio.open(source_path) as src:

        destination = np.empty(
            (ref.height, ref.width),
            dtype="float32",
        )

        reproject(
            source=src.read(1),
            destination=destination,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=ref.transform,
            dst_crs=ref.crs,
            resampling=Resampling.bilinear,
        )

        return destination


def clip_raster(
    raster_path: str | Path,
    roi_path: str | Path,
    output_path: str | Path,
) -> Path:
    """
    Clip a raster to a vector ROI.

    The ROI is automatically reprojected to the raster CRS before
    masking. The result is written as a GeoTIFF.
    """
    raster_path = Path(raster_path)
    roi_path = Path(roi_path)
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    roi = gpd.read_file(roi_path)

    if roi.empty:
        raise ValueError("ROI contains no geometries.")

    if roi.crs is None:
        raise ValueError("ROI has no CRS.")

    with rasterio.open(raster_path) as src:

        # Reproject ROI from its own CRS (normally EPSG:4326)
        # into the CRS used by the Sentinel-2 raster.
        roi_projected = roi.to_crs(src.crs)

        clipped, transform = mask(
            src,
            roi_projected.geometry,
            crop=True,
        )

        profile = src.profile.copy()

        profile.update(
            driver="GTiff",
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform,
            compress="deflate",
        )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(clipped)

    return output_path
