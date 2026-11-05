# C500 artifact layout

## NSA artifact roots: no `restart-` prefix

For Native Sparse Attention, use these four roots under `race_tests/nsa/`:

```text
experiments/<id>/
hack/<id>/
rep/<id>/
submission/<id>/
```

Do not create, name, or reference any `restart-*` directory under `race_tests/nsa/`. Keep one ID across the four roots, for example `v001_s1_fastpath_sc-16g-2`; use the exact machine scope in the ID.

- `experiments/<id>/`: hypothesis, patch, and concise experiment notes. Store a development-source snapshot only when it is needed to reproduce a candidate that is not yet archived in `submission/<id>/`; do not duplicate an accepted submission source here. Reference shared root files such as `official_case.json`, `reference.py`, and the test runner by path, starting commit, and hash instead of copying them. Keep raw profiler and benchmark output in `rep/`.
- `hack/<id>/`: exact scripts and commands used, with a short note describing inputs, outputs, and dependencies.
- `rep/<id>/`: report and manifest plus correctness, benchmark, profiler, tracer, mx-smi, Roofline, and code-generation evidence. Keep Roofline artifacts here rather than creating another top-level root. Mark interrupted or failed evidence explicitly; never fill gaps with estimates.
- `submission/<id>/`: the exact competition-interface source candidate and its hash/validation record. Keep development kernels and scratch files in `experiments/` or `hack/`. Apply only the validation and promotion conditions defined for NSA; the MoE global-SOTA ledger and promotion floor are not NSA requirements unless its competition explicitly says so.

The one-version/one-kernel-state/one-evidence-set/one-commit discipline still applies.

## MoE restart version ID

Use the same directory ID across all four roots:

```text
vNNN_<optimization_direction>_<machine>
```

- `vNNN`: zero-padded restart version beginning at `v000`.
- direction: lowercase English snake_case.
- machine: `16g`, `sc-16g`, `64g`, `16g-64g`, or `sc-16g-64g`.

Examples:

```text
v000_minibs_baseline_sc-16g
v001_step1_weight_locality_sc-16g
v002_step2_load_ahead_sc-16g
```

## MoE restart artifact roots

All live under `race_tests/moe/`:

```text
moe-roofline/<id>/
restart-experiments/<id>/
restart-rep/<id>/
restart-scripts/<id>/
```

Only verified global-SOTA promotions may use the existing repository submission root:

```text
restart-submission/<id>/
```

### `moe-roofline/<id>/`

Store only visualization inputs/outputs and native Roofline images:

```text
<id>_roofline.svg
<id>_roofline.png
<id>_points.csv
<id>_manifest.json
native/
```

### `restart-experiments/<id>/`

Store the hypothesis and implementation trajectory:

```text
<id>_experiment.md
<id>_custom_fusedmoe.py
<id>.patch
```

The experiment document records observed evidence, hypothesis, prediction, falsifier, change, deviations, and one-line outcome linked to the report. Do not duplicate raw profiler dumps here.

### `restart-rep/<id>/`

Store evidence and verdict:

```text
<id>_report.md
<id>_manifest.json
correctness/
benchmark/official.*
benchmark/oj.*
profiler/mcprofiler/raw/
profiler/mcprofiler/summary.*
profiler/mctracer/raw_trace.*
profiler/mctracer/stage_summary.*
profiler/mxsmi/snapshot.*
profiler/mxsmi/hbm_samples.*
profiler/mxsmi/ap_usage.*
codegen/lowering.*
codegen/generated_device.*
codegen/assembly.*
codegen/resource_usage.*
```

### `restart-scripts/<id>/`

Store every script actually used by the version and `<id>_scripts.md`. The Markdown file states purpose, command, inputs, outputs, dependencies, and modifications from the template.

### `restart-submission/<id>/` for verified SOTA promotions

Stage candidate submissions under `/tmp` or `restart-experiments/<id>/candidate_submission.py`. Create this directory only after the exact candidate passes the external OJ per-case monotonic promotion gate in [sota-promotion-contract.md](sota-promotion-contract.md). Store:

```text
submission.py
oj_import_validation.txt
submission.sha256
```

`submission.py` must be self-contained, expose the repository-required submission interface, pass the import allowlist, and be byte-identical to the OJ-tested candidate. Use `race_tests/moe/submission.py` only as a format/interface reference; do not inherit forbidden imports from it. Rejected, failed, inconclusive, local-only, OJ-pending, and merely parent-improving versions must not have a same-ID submission directory.

Maintain the current incumbent in:

```text
restart-submission/SOTA.json
```

Record the promoted iteration ID, submission SHA-256, OJ metric and direction, exact per-case score vector, and evidence source. Update this registry atomically with the new submission directory and four evidence directories.

## Failure handling

Create all four evidence directories for every named version. When an artifact cannot exist because of compile/correctness/tool failure, add `UNAVAILABLE.md` in its expected directory with the command, failure, and next required action. Never synthesize missing numbers. Do not mark a version accepted when its required submission artifact is unavailable.

## Manifest identity

Record iteration ID, status, parent/baseline/current-SOTA IDs, machine, timestamps, branch/commit, source and benchmark hashes, tool versions, commands, artifact inventory/hashes, and conclusion. A status of `accepted`, `final`, or `accepted-final` requires a machine-checkable `sota_gate` containing the incumbent/candidate hashes and full OJ score vectors. Those statuses mean global SOTA promotion, not local acceptance.
