# Restart principles

## Purpose

Treat `restart` as an epistemic reset. Preserve proven code and historical observations, but rebuild causal explanations from current C500 evidence.

## Evidence states

Use exactly these labels in experiment reasoning:

- `VERIFIED`: reproduced by current correctness, benchmark, profiler, tracer, compiler, or hardware evidence.
- `HISTORICAL`: measured previously but not yet reproduced under the current branch/machine/benchmark/toolchain.
- `HYPOTHESIS`: a causal explanation with a prediction and falsifier.
- `UNKNOWN`: unavailable or not yet measured; never fill by analogy with NVIDIA.

Historical negative results are not permanent bans. Reopen one only when the current profile explains why a different shape, combination, branch, machine, or codegen path can change the outcome.

## Causal experiment contract

Before editing, record:

1. the observed stage and metric;
2. the proposed bottleneck mechanism;
3. the smallest code change that targets it;
4. the expected metric and latency movement;
5. a concrete falsifying result;
6. correctness, register, shared-memory, occupancy, traffic, and launch risks.

After measuring, classify:

- `accepted`: exact OJ-tested submission is correct and non-regressing against the incumbent global SOTA on every official case, strictly improves at least one case, and causal evidence is consistent;
- `rejected`: correct but stable regression/no benefit, with evidence explaining the failure where possible;
- `failed`: compile/import/correctness failure;
- `inconclusive`: noise, incomplete collection, tool failure, or conflicting metrics prevent a verdict.

An improvement relative to the direct parent is not sufficient when that parent is below the incumbent SOTA. Treat local-only wins and OJ-correct candidates without complete external performance scores as `inconclusive` for promotion; treat a candidate with any confirmed OJ case regression as `rejected`. Neither may enter `restart-submission`.

## Measurement hierarchy

1. Correctness decides validity.
2. External OJ per-case performance decides global-SOTA promotion; official/local OJ end-to-end latency screens and explains candidates but cannot override an OJ regression.
3. mcTracer decides stage and launch attribution.
4. mcProfiler/mx-smi/Roofline explain compute, traffic, cache, resource, and hardware behavior.
5. Lowering/generated code/assembly decide whether the intended transformation reached the machine.

Do not reverse this hierarchy by accepting a slower candidate because one utilization counter looks better.
