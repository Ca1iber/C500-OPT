# Optimization decision tree

Select mechanisms from evidence, not habit.

## Memory-side kernel

First distinguish excess bytes from insufficient issue rate.

### Excess traffic/cache amplification

Check repeated expert-weight loads across row CTAs, routed-token reloads across output tiles, intermediate `up_logits`, padding/tail blocks, routing/index traffic, L2 working set, and profiler transaction/access deltas.

Candidate families:

- CTA/panel mapping that schedules same-expert blocks for L2 reuse;
- persistent/grouped mapping that reuses weights or activations;
- larger logical reuse tile when register/shared/resource evidence permits;
- fusion or producer-consumer reuse that removes HBM round trips;
- vectorized/aligned copies and coalesced routing/scatter;
- padding-aware specialization supported by actual expert-row distributions.

Expected success may reduce HBM GB/s while reducing bytes and time.

### Low memory-level parallelism/overlap

Check clean HBM samples, memory-pipe counters, barrier/wait evidence, active AP distribution, register/shared limits, and generated load/MMA order.

Candidate families:

- real load-ahead/double buffering that survives lowering;
- copy/MMA ordering and independent outstanding loads;
- resource reduction that permits more resident waves;
- grid mapping that sustains APs without destroying reuse.

Do not repeat `num_stages` mechanically; demonstrate how the new buffer/tile/resource combination differs.

## Compute-side kernel

Check actual MMA/MFMA dtype/instructions, achieved throughput, operand feed, ldmatrix/shared layout, K-loop overhead, masks/tails, conversions/activation, register pressure, and spills.

Candidate families:

- fragment/shared layout and operand-feed restructuring;
- MMA tile/warp mapping changes tied to resource evidence;
- instruction load-ahead or fewer barriers/address instructions;
- padding/tail reduction without losing MMA efficiency;
- stage-specific emitter/lowering path changes.

Do not assume “MMA present” means MMA is saturated.

## Latency/grid/launch-side kernel

Use mcTracer and calculate blocks/waves per expert and stage against 104 physical APs. Current 25% sGPU still enumerates 104 APs.

Candidate families:

- grid linearization/panel/group mapping;
- additional independent tiles for small grids;
- merge tiny work or reduce launch/synchronization overhead;
- load-balance expert rows and avoid empty/tail blocks;
- persistent paths only when combine/reduction costs are modeled.

## Resource/synchronization-side kernel

Use compiler resource usage and assembly to test register/shared occupancy limits, barriers, scoreboard waits, spills, or redundant synchronization.

Candidate families:

- narrower accumulator or stage-specific tile;
- buffer lifetime shortening/reuse;
- barrier removal only with proven dependency safety;
- alternative warp/thread layout that is correctness-compatible;
- split mechanisms only when reduction overhead is modeled.

## Required stage focus for MoE

- Model Step1 gate/up/SwiGLU and Step2 down separately.
- Compute per-expert rows and block count, not only total tokens.
- Compare OJ distributions with official/local distributions without substituting one for another.
- Prioritize a stage by end-to-end time share and plausible headroom, then verify bottleneck migration after every OJ-SOTA promotion.
