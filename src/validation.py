from __future__ import annotations
import numpy as np


def validate_ndvi(ndvi: np.ndarray) -> dict:
    finite = ndvi[np.isfinite(ndvi)]
    if finite.size == 0:
        raise ValueError("NDVI contains no finite pixels.")
    minimum = float(finite.min())
    maximum = float(finite.max())
    if minimum < -1.0001 or maximum > 1.0001:
        raise ValueError(f"NDVI outside physical range: {minimum}, {maximum}")
    return {
        "valid_pixels": int(finite.size),
        "min": minimum,
        "max": maximum,
        "mean": float(finite.mean()),
        "median": float(np.median(finite)),
        "std": float(finite.std()),
        "vegetated_fraction_ndvi_gt_0_3": float((finite > 0.3).mean()),
    }
