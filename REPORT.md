# Sentinel-2 Geospatial Analysis: Technical Review and Development Roadmap

**Repository:** https://github.com/Mairaelefante/sentinel2-geospatial-analysis  
**Review date:** 2026-11-09  
**Status:** Existing Python geospatial pipeline. Review based on source inspection; no new processing run, test execution, or complete history/secret scan was performed.

## Project purpose

A personal scientific software project processing Copernicus Sentinel-2 Level-2A multispectral data. It provides red/NIR band handling, NDVI computation, geospatial utilities for raster alignment and AOI clipping, summary statistics, GeoTIFF/JSON outputs and a PNG map. The documented example processes a Rome-area scene. The pipeline uses public satellite imagery, not private individual records.

## Existing code verified

- `src/main.py`: command-line NDVI calculation from pre-aligned red/NIR rasters; rejects mismatched grids; writes GeoTIFF, JSON statistics and a PNG map.
- `src/ndvi.py`: vectorized NDVI with NaNs where the denominator is zero and final clipping to [-1, 1].
- `src/raster_processing.py`: raster reading, resampling to a reference grid and clipping to a reprojected region of interest.
- `src/validation.py`: finite-value counts, range checks, mean, median, standard deviation and high-NDVI fraction.
- `tests/test_ndvi.py`: two small unit tests for known NDVI values and aggregate range checks.
- `README.md`: detailed documentation and reproducibility examples; describes July 2026 Copernicus imagery, a Rome AOI and derived outputs.
- `LICENSE`: MIT license already exists; no license replacement necessary.

The main CLI currently requires co-registered rasters, even though separate alignment/clipping helpers exist. Integrating the helpers into an end-to-end command would be meaningful future work.

## Technical review and risks

### No-data and invalid measurements

`calculate_ndvi` masks a zero denominator but does not explicitly apply source raster nodata masks or reject non-finite inputs. Clipping the computed NDVI to [-1,1] can also obscure invalid or unexpectedly scaled reflectances. Investigate actual Sentinel-2 reflectance scaling and flag unexpected values rather than relying on clipping alone.

### Raster alignment and masking

`align_to_reference` allocates a destination array with `np.empty` and calls `reproject` without explicit source/destination nodata policy. Add deterministic initialization, nodata transfer and regression tests for partial overlap and unmatched extents. Tests should also verify CRS reprojection, geotransforms and AOI clipping.

### Cloud and quality handling

The pipeline does not yet integrate Sentinel-2 Scene Classification Layer masks to screen cloud, cloud-shadow and poor-quality observations. This matters for physically interpretable vegetation statistics.

### Tests and scientific traceability

Two unit tests cover core arithmetic and ranges, not full input/output integration. Build synthetic GeoTIFF fixtures and tests for output metadata, JSON schema, masked areas and reprojection edge cases. Keep source imagery metadata and all assumptions in result manifests.

### Performance and usability

Large-area processing may need chunking/windowed operations, memory-awareness, and clear failure paths. A documented, parameter-driven CLI for AOI, alignment, masks and output selection would make the system easier to reuse.

## Proposed future development (not yet implemented)

| Workstream | Proposed deliverable | Estimated effort |
| --- | --- | ---: |
| Valid-data and SCL masks | Handle nodata, cloud and cloud-shadow classes with tests | 6 h |
| Reprojection validation | Reliable resampling, nodata initialization and grid/AOI integration tests | 5 h |
| End-to-end CLI | Integrate AOI clipping and optional alignment with robust argument validation | 5 h |
| Multi-date workflow | Compare two time points and produce NDVI change maps with metadata | 6 h |
| Quality and reproducibility | Synthetic fixture tests, provenance manifest, clearer errors and documentation | 5 h |
| **Total proposed effort** | | **27 h** |

These are **planning estimates**, not hours already worked or promised paid time. Include them in a BYOP submission only if the owner genuinely intends to carry out this personal software development.

## Suggested acceptance criteria

1. Known synthetic raster inputs produce expected NDVI pixels and summary statistics, with nodata correctly excluded.
2. Spatial reprojection and clipping preserve and validate CRS, transform, alignment and output extent.
3. SCL masks exclude documented unsuitable classes without inadvertently discarding valid samples.
4. The CLI supports a reproducible workflow from supplied rasters and AOI to GeoTIFF, PNG and JSON outputs.
5. Multi-date comparison aligns grids explicitly and reports valid-pixel coverage and per-pixel NDVI difference.
6. Tests execute from a clean checkout with declared dependencies; no real personal or regulated data is required.

## BYOP-specific eligibility and verification checklist

- **Public repository:** observed; keep original commit history.
- **License:** existing MIT license at repository root; no change made.
- **Work remaining:** 27-hour *proposed* development roadmap above.
- **Ownership:** individual GitHub account is not sufficient evidence of legal ownership. Owner must confirm the project was personally developed and is not an employer/client/university deliverable or subject to any NDA.
- **Data rights:** use publicly redistributable synthetic fixtures and respect Copernicus data attribution and distribution requirements.
- **Scope:** geospatial software and satellite-image processing, **not AI-model training or evaluation**.
- **Secrets scan:** complete working tree and Git history have not been audited.
- **Runtime verification:** no tests or processing runs were executed for this report; no new performance or numerical claims are made.

## Recommended first development step

Implement explicit nodata/non-finite masking in NDVI calculations and add synthetic-raster regression tests. Follow with robust grid alignment and SCL cloud masking, preserving ordinary development commits.
