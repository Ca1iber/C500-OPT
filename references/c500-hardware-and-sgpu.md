# C500 hardware and sGPU model

Snapshot source: curated from the installed `c500-hardware-awareness` Skill on 2026-08-11. Treat that Skill as the canonical place for later hardware fact updates.

## Stable and current working facts

| Parameter | Working value | Evidence | Scope |
|---|---:|---|---|
| Physical VRAM | 64 GB HBM2e | OFFICIAL + DRIVER | C500 physical card |
| Physical AP count | 104 | DRIVER | Runtime enumeration and 8 DPC × 13 AP view |
| L2 | 8 MiB | DRIVER | Physical card/runtime view |
| Maximum board power | 350 W | OFFICIAL + DRIVER | Physical card |
| Observed MC clock | 1800 MHz | DRIVER | Dynamic state; re-query each campaign |
| Theoretical DRAM–L2 bandwidth | 1843.2 GB/s | DRIVER | mcProfiler `MAX_Bandwith`; not sustained application bandwidth |
| Inferred FP16 MMA roof | 1916.928 TFLOP/s | INFERRED | Reconstruct before precise use; instruction/clock dependent |
| Inferred physical ridge | 1040 FLOP/B | INFERRED | `1916.928 × 1000 / 1843.2` |

## sc-16g observed slice

| Parameter | Observed value | Interpretation |
|---|---:|---|
| Compute quota | 25% | Scheduling quota, not fixed 26-AP exposure |
| VRAM quota | 16000 MiB | Runtime sees about 15.22 GiB |
| Runtime-visible APs | 104 | Current evidence supports time-sliced access across physical APs |
| Scheduling class | best effort | Do not infer undocumented guarantees |
| Time slice | 10 ms | Current driver observation |
| Mixed read/write sustained HBM | about 1.43–1.46 TB/s | BENCHMARK, idle single-tenant condition |
| Conservative engineering HBM roof | 1400 GB/s | Use for current sc-16g sensitivity/modeling |
| Physical theoretical HBM roof | 1843.2 GB/s | Retain as theoretical comparison |

The 25% compute quota does not imply 25% HBM. The hypothesis `1843.2 × 25% = 460.8 GB/s` was falsified by MXCC, PyTorch, and mx-smi streaming measurements. Keep 460.8 GB/s only as a sensitivity point when discussing unknown contention/QoS.

## Unknowns

- Exact public VL1 capacity/associativity/replacement behavior.
- Complete shared-memory and register allocation rules for this TileLang/MXMACA version.
- Authoritative dtype-specific physical peaks beyond measured/inferred paths.
- HBM QoS and minimum bandwidth under multi-sGPU contention.
- Exact occupancy formulas and limits without compiler/resource evidence.

Use microbenchmarks, resource usage, profiler counters, generated code, and assembly instead of importing CUDA/NVIDIA constants.

## Per-version re-query requirements

Capture physical and sGPU views, clocks, memory, active processes, AP usage, scheduling class/time slice, KMD/MACA/BIOS/mx-smi versions, and synchronized HBM samples. A previous idle snapshot cannot certify the current run.
