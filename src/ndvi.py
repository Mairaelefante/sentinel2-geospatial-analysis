from __future__ import annotations
import numpy as np


def calculate_ndvi(red: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """Calculate NDVI safely from co-registered red and NIR arrays."""
    if red.shape != nir.shape:
        raise ValueError("Red and NIR arrays must have identical shapes.")
    red = red.astype("float32", copy=False)
    nir = nir.astype("float32", copy=False)
    denominator = nir + red
    ndvi = np.full(red.shape, np.nan, dtype="float32")
    valid = denominator != 0
    ndvi[valid] = (nir[valid] - red[valid]) / denominator[valid]
    return np.clip(ndvi, -1.0, 1.0)
