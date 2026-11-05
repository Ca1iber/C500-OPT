# C500 profiling workflow

## Collection order

1. Run correctness and clean device-event benchmark without profiler attachment.
2. Use mcTracer in a separate run to identify device kernels, Step1/Step2 duration, auxiliary work, and launch gaps.
3. Use mcProfiler per kernel/stage with the smallest metric set that answers the hypothesis.
4. Sample read-only mx-smi concurrently with a sufficiently long/repeated workload.
5. Capture compiler resources, lowering, generated device code, and assembly from the exact kernel hash.

Never compare a profiler-instrumented duration directly with the clean benchmark as if both had identical overhead.

## mcTracer

Use it to answer:

- Which kernels execute and in what order?
- How much time belongs to Step1, Step2, auxiliary kernels, synchronization, and launch gaps?
- Is the selected stage material to end-to-end latency?
- Are first-run compile/initialization events excluded from steady state?

Run multiple stable samples for short kernels. Save the raw trace and a machine-readable stage summary.

## mcProfiler

Before interpreting results:

- record the actual binary path and version;
- record kernel names, profile range/count, shape, dtype, and source hash;
- enumerate available metrics rather than inventing NCU names;
- preserve raw JSON/text/CSV and native plots;
- confirm `MAX_Bandwith`, compute roof, clock, AP count, and processed field formulas.

Use Roofline first for classification, then collect targeted cache, memory, MMA, wait/stall, barrier, occupancy/resource, or instruction metrics if available. Missing metrics remain `UNKNOWN`.

`all_memacs`, VL1/L2 access counters, or similar fields are not automatically bytes. Compare them across same-tool/same-version candidates unless a documented conversion exists.

## mx-smi

Use only read-only queries. Capture:

```text
summary, hwinfo, memory, clock, HBM bandwidth, AP usage,
sGPU mode, scheduling class, time slice, remaining quota
```

Synchronize HBM sampling with a repeated workload, exclude idle/start/phase-transition samples, and report median plus distribution. `sgpu --show-usage` may return zero for millisecond kernels and cannot stand alone.

Never automatically run reset, kill, sGPU create/remove/set/enable/disable, firmware, power, or scheduling mutation commands.

## Cross-tool decision table

| Observation | Interpretation to test |
|---|---|
| mcTracer stage dominates; mcProfiler HBM side; mx-smi below measured roof | traffic, coalescing, cache, concurrency, or load/compute overlap |
| HBM transactions fall and latency falls while GB/s falls | successful traffic elimination, not bandwidth regression |
| mcProfiler compute side; generated MMA present but throughput low | operand feed, pipeline, instruction mix, tail/padding, resource pressure |
| High profiler utilization but end-to-end unchanged | wrong stage, launch/framework overhead, or profiler metric not causal |
| TileLang diff but identical lowering/assembly | compiler canonicalization; benchmark delta is likely noise/external state |
| Wider case improves GB/s | prologue/epilogue, time-slice, wave, or steady-state amortization may matter |

Do not announce a bottleneck until stage timing, roof choice, and at least one independent counter/compiler/hardware signal agree.
