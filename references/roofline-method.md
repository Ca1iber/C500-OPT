# C500 Roofline method

## Per-stage formulas

For each case and Step1/Step2 kernel, compute:

```text
AI = FLOPs / bytes
memory_roof_TFLOPS = AI × bandwidth_GBps / 1000
ridge_FLOP_per_B = compute_roof_TFLOPS × 1000 / bandwidth_GBps
attainable_TFLOPS = min(compute_roof_TFLOPS, memory_roof_TFLOPS)
roof_efficiency = achieved_TFLOPS / attainable_TFLOPS
derived_bandwidth_GBps = achieved_TFLOPS × 1000 / AI
```

Maintain two byte models:

- compulsory algorithmic bytes: minimum reads/writes implied by the dataflow;
- profiler transaction/access model: observed traffic proxy, with documented units.

List input, gate/up/down weights, intermediate, output, router/index, padding, repeated CTA weight loads, and cache/replay effects separately.

## Required roofs

Plot at least:

- `physical_theoretical`: 1843.2 GB/s;
- `sc16_measured_conservative`: 1400 GB/s for current idle single-tenant engineering analysis;
- a compute roof justified by actual dtype, MMA path, clock, and slice model.

Optionally show 460.8 GB/s as `linear_25pct_sensitivity`, never as a verified cap.

mcProfiler native images may normalize against the physical theoretical roof. Preserve them, then generate a separate re-normalized combined figure with clearly labeled roofs.

## CSV point schema

The bundled renderer expects:

```csv
label,ai_flop_per_byte,tflops
C1 S1,980.786,877.070
C1 S2,1387.734,804.560
```

Additional columns may be retained. Never substitute OJ end-to-end effective TFLOP/s for mcProfiler's native per-kernel point without labeling it as a different metric.

## Interpretation

- Memory side does not prove HBM is saturated; check achieved/available bandwidth, transactions, cache, and stalls.
- Compute side does not prove MMA saturation; check actual MMA instructions, operand feed, utilization, and resource stalls.
- A point near the ridge is sensitive to roof choice; report both physical and sc-16g classifications.
- Compare Roofline changes only with the same profiler/toolchain formula or explicitly rebuild all points from a common model.
