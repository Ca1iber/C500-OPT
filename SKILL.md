---
name: c500-opt
description: "Drive an evidence-first, OJ-compliant optimization loop for TileLang GPU kernels on MetaX C500/MXMACA. Use when Codex needs to optimize, benchmark, profile, diagnose, package, or iterate a C500 kernel—especially Fused MoE GEMM—using the OJ import allowlist, submission-ready sources, project-native benchmarks, mcTracer, mcProfiler, mx-smi, Roofline analysis, TileLang lowering, generated device code, backend assembly, per-version experiment artifacts, and bilingual Git commits."
---

# C500-OPT

C500-OPT captures the project's accumulated C500/MXMACA/TileLang optimization practice as a reproducible, evidence-driven workflow.

## Track-specific archive roots

The measurement and evidence workflow is shared across C500 kernels; archive paths and promotion rules are track-specific. For MoE restart work, use the `race_tests/moe/restart-*` roots and MoE SOTA rules. For NSA, use `race_tests/nsa/experiments/<id>/`, `hack/<id>/`, `rep/<id>/`, and `submission/<id>/`; never use a `restart-` prefix anywhere under `race_tests/nsa/`. Reference shared root inputs by repository path, commit, and hash; do not copy `official_case.json`, `reference.py`, the shared test runner, or an already archived submission into `experiments/<id>/`. MoE restart branches, the MoE SOTA ledger, and the MoE-specific promotion floor do not apply to NSA unless the NSA competition defines an equivalent rule. See [artifact-layout.md](references/artifact-layout.md).

Run a measurement-first loop: establish an exact baseline, identify the limiting stage with independent evidence, state a falsifiable hypothesis, change one coherent mechanism, then close the version with correctness, benchmarks, profiles, code-generation artifacts, reports, and Git history.

## Hard rules

1. Treat correctness as a gate. Never claim performance for an incorrect result.
2. Optimize end-to-end official/OJ latency, not a single attractive counter. A faster kernel may report lower raw GB/s after eliminating traffic.
3. Do not tune before establishing the current machine, code, benchmark, and profiler identity.
4. Separate facts, hypotheses, predictions, and conclusions. Write the falsifier before editing the kernel.
5. Use only project-native benchmark logic. Do not introduce KernelBench, `--no-ref`, altered shapes, reduced correctness, or timing shortcuts unless the existing benchmark explicitly exposes and the user authorizes them.
6. Use mcTracer, mcProfiler, mx-smi, TileLang lowering, generated device code, assembly, and resource reports as complementary evidence. Do not pretend any one tool is an NCU-equivalent source of all metrics.
7. Never infer that a 25% compute slice has 25% HBM, L2, clocks, or AP visibility. Read [c500-hardware-and-sgpu.md](references/c500-hardware-and-sgpu.md).
8. Archive every named version before starting the next one. A labeled failed run is still closed and committed with its failure evidence; incidental syntax/debug attempts do not receive version numbers.
9. Preserve user changes and unrelated dirty files. Stage only the kernel and artifacts belonging to the current version.
10. Never store SSH passwords, private keys, tokens, or temporary credentials in the Skill or experiment artifacts.
11. Treat OJ import compliance as a correctness gate. Submission source may import only the `torch`, `tilelang`, and `math` roots; TileLang imports must use one of the exact forms in [oj-submission-contract.md](references/oj-submission-contract.md). `tvm`, `tir`, `typing`, and every other root package are forbidden in submitted source.
12. Treat `race_tests/moe/restart-submission/` as a monotonic global-SOTA promotion ledger, not a collection of locally improved or merely OJ-valid candidates. A candidate must beat the current OJ-verified SOTA, not only its direct parent. Across every official OJ case, no score may regress and at least one score must strictly improve. Missing/pending OJ scores, correctness-only OJ results, local-only wins, and improvements over a non-SOTA parent cannot create a `restart-submission/<id>/` directory or use `accepted`/`opt(moe)`. Read [sota-promotion-contract.md](references/sota-promotion-contract.md).
13. Never accept an optimization that exists only in a development kernel. Every SOTA promotion must have a self-contained `race_tests/moe/restart-submission/<id>/submission.py`, pass `validate_oj_submission.py`, and pass correctness plus official/OJ benchmarks from that exact file and SHA-256.
14. Never use asynchronous copy in a development kernel, candidate, or submission. Reject MACA/MXMACA async-copy builtins, headers, pipeline-copy helpers, waits/tokens, and any TileLang construct whose lowering materializes asynchronous copy. `T.Pipelined` or `T.copy` is allowed only when lowering, generated device code, and ISA prove that the selected configuration remains synchronous.
15. Never inject C/C++, CUDA-like device source, LLVM, or other foreign code. Reject `T.import_source`, `call_extern`, `call_packed`, `call_cpacked`, embedded headers/device functions, and equivalent escape hatches even when the injected code is textually self-contained or OJ imports otherwise pass.
16. Express the complete kernel data movement, synchronization, and computation with OJ-allowed TileLang primitives. Python helpers may organize or expand TileLang IR, and the host wrapper may allocate/cache tensors with `torch`, but neither may replace kernel work with injected code, external calls, or Torch computation.
17. For the active sc-16g MoE restart, enforce a **1.2% minimum promotion floor** versus the incumbent under the formal paired benchmark. A candidate below 1.2%, inside the measured noise band, regressing any official case, failing correctness, or lacking complete evidence is not an optimization or version and must not advance `dorm`, create a branch, or enter `restart-submission/`.
18. Archive explored, rejected, regressing, failed, or inconclusive MoE directions only in `race_tests/moe/restart-deped-trials/`. Each archive report must preserve the starting commit, exact source/configuration, correctness/import results, benchmark/profile evidence, hypothesis, and stop reason. Do not leave temporary wrappers, generated kernels, profiler dumps, or scratch files in the submission tree.
19. Weight preprocessing for Gate, Up, or Down is allowed only when its complete cost is inside every scored `run_kernel` call. Perform all preprocessing computation with submitted TileLang kernels, fully overwrite the consumed preprocessed contents on every call, and consume them only within that same call. Never perform preprocessing only during warmup, reuse or cache preprocessed results across calls, or omit preprocessing kernels from the official/OJ timing path. Caching an allocation is not permission to cache its contents.
20. Do not manually invoke, wrap, spell, or otherwise access general MXMACA compiler built-in functions such as `__builtin_mxc_*` from submission logic, including preprocessing. Use OJ-allowed TileLang primitives only. Backend-generated built-ins produced by normal lowering of an allowed TileLang primitive are compiler implementation details, not authorization to call those built-ins directly; verify the submitted source rather than treating generated spelling as a source-level API.

## Resolve the run before acting

Inspect the workspace and present a concise resolved plan containing:

- workspace and active Git branch;
- kernel path and source hash;
- correctness command;
- official benchmark path/command;
- OJ benchmark path/command;
- target machine (`16g`, `sc-16g`, `64g`, or an explicit cross-machine scope);
- current version ID and track-specific artifact directories; for MoE, also the incumbent OJ-verified SOTA ID/hash/score vector;
- candidate staging path and applicable submission validator; for MoE, do not create `restart-submission/<id>/` before SOTA promotion, and for NSA use `race_tests/nsa/submission/<id>/` without a `restart-` prefix;
- profiler/codegen commands that are confirmed available;
- user constraints and unresolved uncertainties.

Stop for clarification only when a role or command cannot be discovered safely. Do not install dependencies, change benchmark logic, or mutate GPU/sGPU settings without explicit authority.

## Establish `v000` baseline

Use `v000_minibs_baseline_sc-16g` for the current restart baseline unless the user specifies another ID. Read [artifact-layout.md](references/artifact-layout.md), then initialize all four matching directories with:

```bash
python <skill>/scripts/init_iteration.py \
  --root race_tests/moe \
  --version v000 \
  --slug minibs_baseline \
  --machine sc-16g
```

Record before profiling:

- Git branch, commit, status, kernel hash, benchmark hashes;
- mx-smi/KMD/MACA/BIOS/TileLang/PyTorch/mcProfiler identity;
- physical and sGPU views, clocks, memory, AP usage, scheduling class and time slice;
- exact shapes, dtype, warmup/repeat, random/input construction, and timing method;
- clean correctness, official benchmark, and exact OJ benchmark results.

Then collect for each relevant OJ case and each Step1/Step2 kernel:

1. mcTracer timeline and stage/launch-gap summary;
2. mcProfiler raw output and only the counters required by the hypothesis;
3. native and re-normalized Roofline points;
4. synchronized mx-smi HBM/AP samples;
5. TileLang lowering, generated device code, assembly, and resource usage.

Read [profiling-workflow.md](references/profiling-workflow.md), [tilelang-codegen-workflow.md](references/tilelang-codegen-workflow.md), and [roofline-method.md](references/roofline-method.md) before interpreting these artifacts.

## Iteration protocol

For each `vNNN_<direction>_<machine>` version, perform this sequence without starting the next code change early:

### 1. Select the target

- Compare the incumbent OJ-verified SOTA against `v000` and the immediately previous experiment. Never infer that the direct parent or latest commit is the SOTA.
- Use mcTracer to select the stage that materially affects end-to-end time.
- Use mcProfiler, mx-smi, Roofline, and generated code to classify it as memory-, compute-, latency/grid-, synchronization-, resource-, or launch-bound.
- Read [optimization-decision-tree.md](references/optimization-decision-tree.md) for candidate families.

### 2. Write the hypothesis card

Create the experiment document before editing. State:

```text
Observed evidence:
Verified bottleneck:
Current hypothesis:
Proposed mechanism:
Predicted metric changes:
Falsifying result:
Correctness and resource risks:
```

Historical experiments are observations, not permanent bans. Revisit a prior direction only when current evidence predicts why this configuration or combination should behave differently.

### 3. Make one coherent change

- Change one mechanism or a tightly coupled set required to express that mechanism.
- Preserve the official and OJ benchmark semantics.
- Capture a source snapshot and patch.
- Inspect lowering/codegen before benchmarking when the intended change may be optimized away.

### 4. Run the evidence bundle

Run, in order:

1. build/import and correctness;
2. static OJ import validation of the exact candidate source;
   this gate also rejects async copy, foreign-code injection, and non-TileLang kernel escape hatches;
3. official benchmark;
4. exact OJ benchmark;
5. mcTracer;
6. targeted mcProfiler plus Roofline;
7. synchronized mx-smi sampling;
8. lowering, generated code, assembly, and resource capture.

Use full required benchmark settings for a version verdict. A fast screen is allowed only through modes already exposed by the project and must be labeled `screen`, never `verdict`.

### 5. Interpret causally

Answer:

- Did the predicted metric move in the predicted direction?
- Did Step1/Step2 time and end-to-end latency agree?
- Did HBM traffic fall, bandwidth utilization rise, cache behavior change, MMA utilization change, or resource pressure migrate?
- Did the generated code actually change?
- Is the result outside the paired-run noise band?
- Did the bottleneck migrate?

Use `accepted`, `rejected`, `failed`, or `inconclusive`. Here `accepted` means a verified global SOTA promotion under [sota-promotion-contract.md](references/sota-promotion-contract.md), never merely a local win. Never call a noisy single run a win.

### 6. Close the version

- Put visual Roofline artifacts in `moe-roofline/<id>/`.
- Put hypothesis, strategy, source snapshot, and patch in `restart-experiments/<id>/`.
- Put correctness, benchmark, profiler, tracer, mx-smi, codegen, and report artifacts in `restart-rep/<id>/`.
- Put the exact scripts used plus their short Markdown description in `restart-scripts/<id>/`.
- Stage an OJ-ready candidate under `/tmp` or `restart-experiments/<id>/`; validate, benchmark, and submit that exact SHA-256 without creating `restart-submission/<id>/` yet.
- Only after the candidate passes the monotonic OJ SOTA gate, create `restart-submission/<id>/submission.py`, record the incumbent/candidate OJ score vector and hashes in `sota_gate`, and update `restart-submission/SOTA.json` in the same commit. Do not merely copy a development file that depends on forbidden imports or repository-private helpers.
- If any OJ case regresses, scores are unavailable/pending, or the candidate only beats a non-SOTA parent, close it in the four evidence directories as `rejected` or `inconclusive`; no same-ID submission directory is permitted.
- Run `summarize_iteration.py` and `validate_iteration.py`.
- Commit before editing the next version. Follow [git-protocol.md](references/git-protocol.md).

If compilation or correctness fails, archive logs, mark unavailable profile/Roofline outputs explicitly, close the version, and do not make performance claims.

## Stall and stop rules

After three consecutive versions fail to beat the incumbent OJ SOTA outside the measured noise band or improve the targeted causal metric:

1. re-profile the incumbent OJ SOTA under a fresh environment snapshot;
2. review all attempted mechanism families;
3. check whether the roof, stage dominance, or generated code has changed;
4. select a genuinely different evidence-supported direction.

For the active sc-16g MoE restart, do not promote a candidate below the user-specified 1.2% relative improvement floor. Repeated measurements and causal evidence are required, but they do not waive that floor. Candidates below 1.2% remain diagnostic trials and belong in `race_tests/moe/restart-deped-trials/` only.

Stop only when one of these holds:

- the user-specified iteration cap is reached;
- reproducible measurements show a physical/timer/launch floor;
- at least three distinct viable mechanism families have been falsified and no evidence-supported direction remains.

On stop, restore the best measured kernel from its exact commit, retain every artifact directory, rerun full correctness plus official/OJ benchmarks, and create a final bilingual commit.

## Reference routing

- C500-OPT workflow foundations and toolchain: [workflow-foundations.md](references/workflow-foundations.md)
- Restart epistemology and evidence hierarchy: [restart-principles.md](references/restart-principles.md)
- C500, sc-16g, 25% sGPU, AP/L2/HBM facts: [c500-hardware-and-sgpu.md](references/c500-hardware-and-sgpu.md)
- Evidence labels and conflict handling: [c500-evidence-rules.md](references/c500-evidence-rules.md)
- mcTracer/mcProfiler/mx-smi collection and interpretation: [profiling-workflow.md](references/profiling-workflow.md)
- TileLang lowering/generated code/assembly workflow: [tilelang-codegen-workflow.md](references/tilelang-codegen-workflow.md)
- Dual-roof formulas and point schema: [roofline-method.md](references/roofline-method.md)
- Official/OJ correctness and benchmark integrity: [moe-benchmark-contract.md](references/moe-benchmark-contract.md)
- OJ import allowlist and accepted-version submission packaging: [oj-submission-contract.md](references/oj-submission-contract.md)
- Global SOTA identity, per-case monotonic promotion, staging, and manifest schema: [sota-promotion-contract.md](references/sota-promotion-contract.md)
- Four-directory naming and required artifacts: [artifact-layout.md](references/artifact-layout.md)
- Branch, commit, final restore, and bilingual body rules: [git-protocol.md](references/git-protocol.md)
- Bottleneck-to-experiment mapping: [optimization-decision-tree.md](references/optimization-decision-tree.md)

This specialized restart layout overrides the general `rep-workflow` location for runs governed by this Skill. Do not move new restart artifacts into `race_tests/experiment/`; leave historical files untouched.
