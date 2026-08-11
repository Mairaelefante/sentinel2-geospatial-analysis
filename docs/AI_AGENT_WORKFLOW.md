# AI Coding Agent Workflow

This project is designed to document *agentic* coding work rather than treating an AI system as a chat-only assistant.

## Workflow record

### Task
Build an end-to-end Sentinel-2 NDVI pipeline with explicit geospatial validation.

### Agent role
Codex-assisted project scaffolding, implementation planning, code generation, test design, and debugging support.

### Human verification contract
Agent output is never accepted solely because it runs. Each geospatial change is checked for:
1. CRS compatibility.
2. Raster grid alignment (transform, width, height, resolution).
3. Expected spectral-band semantics (B04 = red, B08 = NIR for Sentinel-2).
4. NDVI finite-value range [-1, 1].
5. Reproducible outputs and explicit statistics.

### Representative failure mode: CRS mismatch
A vector ROI and satellite raster may use different coordinate reference systems. Passing the vector geometry directly to a raster mask can yield an empty or geographically incorrect crop. The safe workflow is to inspect both CRSs and reproject the ROI to the raster CRS before masking. `clip_raster()` implements that invariant.

### Representative failure mode: raster misalignment
Even when two rasters describe the same region, they must share a grid before pixel-wise arithmetic. The pipeline checks CRS, affine transform, width and height before calculating NDVI. `align_to_reference()` is provided for controlled reprojection/resampling.

### Validation
Unit tests cover known NDVI values and range checks. Runtime validation records valid-pixel count, minimum, maximum, mean, median, standard deviation and a simple vegetation fraction.

## Interview-ready summary
The agent accelerated implementation, but geospatial correctness remained a human-controlled contract. I explicitly checked CRS, grid alignment, band semantics and numerical invariants, and I rejected or corrected changes that violated those constraints.
