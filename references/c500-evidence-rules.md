# C500 evidence rules

## Levels

| Level | Meaning |
|---|---|
| `OFFICIAL` | MetaX product page, manual, or official technical material states the fact |
| `DRIVER` | mx-smi, runtime, compiler, tracer, or profiler reports the current environment fact |
| `BENCHMARK` | Reproducible experiment and raw data support a machine/workload-specific value |
| `INFERRED` | Formula combines facts but no direct specification states the result |
| `UNKNOWN` | Not documented or measured; leave TODO |

## Required provenance

Record value/unit, scope, evidence level, timestamp, machine, software versions, command/source path, reproduction command, and notes.

## Conflict resolution

Check, in order:

1. GB/s versus GiB/s, MB versus MiB, FLOP versus instruction, and read/write versus aggregate traffic;
2. physical theoretical versus sGPU-visible versus physical counter versus profiler-derived scope;
3. sampling window, warmup, workload phase, clock, contention, and software version;
4. algorithmic compulsory bytes versus actual transactions/cache/replay.

Retain explainable multiple values. Replace a fact only when new evidence covers the same scope and method.

## Forbidden inferences

- VRAM percentage → HBM/L2/PCIe/AP/clock/power percentage.
- Compute percentage → fixed visible AP count.
- One profiler point → platform guarantee.
- Peak sample → sustained median.
- mcProfiler-derived bandwidth → byte-identical equivalence with STREAM/mx-smi traffic.
