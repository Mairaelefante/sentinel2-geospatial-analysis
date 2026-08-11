import numpy as np
from src.ndvi import calculate_ndvi
from src.validation import validate_ndvi

def test_ndvi_known_values():
    red = np.array([[1, 2], [0, 1]], dtype=float)
    nir = np.array([[3, 2], [0, 0]], dtype=float)
    out = calculate_ndvi(red, nir)
    assert np.isclose(out[0, 0], 0.5)
    assert np.isclose(out[0, 1], 0.0)
    assert np.isnan(out[1, 0])
    assert np.isclose(out[1, 1], -1.0)

def test_validation_range():
    stats = validate_ndvi(np.array([[-1.0, 0.0, 0.7, 1.0]], dtype=float))
    assert stats["valid_pixels"] == 4
    assert -1 <= stats["min"] <= stats["max"] <= 1
