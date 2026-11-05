# Git protocol

## Branches

Use the user-approved restart branch, currently `moe-minibs`, as the main experiment line. Reuse an existing restart branch; create a new branch only under the conditions below.

Create `exp/moe-vNNN-<direction>` from the restart branch only for structural risk, multiple commits, benchmark/profile infrastructure changes, or mutually exclusive design paths.

## Atomic version rule

One named version maps to:

- one coherent kernel state;
- four matching artifact directories;
- one closed verdict;
- one commit.

A verified global-SOTA promotion additionally maps to one compliant `restart-submission/<id>/submission.py` and the corresponding `restart-submission/SOTA.json` update captured in the same commit.

After running a labeled version, complete evidence collection, reports, validation, and commit before editing the next version. A labeled compile/correctness failure is committed with failure evidence. Incidental pre-version syntax/debug attempts are not iterations.

Stage only current-version files. Preserve unrelated dirty worktree changes.

Before external OJ evidence exists, stage the candidate under `/tmp` or `restart-experiments/<id>/candidate_submission.py`; do not create `restart-submission/<id>/`. Before an `opt(moe)` commit, compare that exact SHA-256 with the incumbent recorded in `restart-submission/SOTA.json`. Require complete comparable OJ results, no regression in any official case, and a strict improvement in at least one case. Then archive the exact bytes and update the registry atomically. If this gate fails or remains pending, use `exp(moe)` with `rejected` or `inconclusive`; never commit it as the current OJ best.

## Commit message

The subject may be English:

```text
exp(moe): v001 improve Step1 weight locality
```

The body must contain an English section followed by a complete Chinese translation:

```text
English:
Hypothesis: ...
Correctness: ...
Official benchmark: ...
OJ benchmark: ...
OJ submission: path / SHA-256 / import validation ...
mcProfiler: ...
mcTracer: ...
mx-smi: ...
Codegen: ...
Artifacts: ...
Decision: accepted/rejected/failed/inconclusive.

中文：
假设：……
正确性：……
官方 Benchmark：……
OJ Benchmark：……
OJ 提交稿：路径 / SHA-256 / import 校验……
mcProfiler：……
mcTracer：……
mx-smi：……
代码生成：……
产物：……
结论：接受/拒绝/失败/证据不足。
```

Use `opt(moe)` only for a verified global OJ-SOTA promotion. A version that improves relative to a regressed parent but does not beat the incumbent SOTA is not accepted. Use `exp(moe)` for rejected, failed, inconclusive, OJ-pending, local-only, or exploratory versions. Use `fix`, `test`, `docs`, or `chore` only when that is the actual single-purpose change.

## Final restore

Identify the incumbent from `restart-submission/SOTA.json` and verify it against full external OJ evidence; never select the latest commit or a locally faster candidate. It must have a compliant archived submission. Restore both the development kernel and `restart-submission/<id>/submission.py` verbatim from its commit, retain all later reports, rerun import validation, full correctness, and both benchmarks from the submission artifact, then create a bilingual `final(moe)` commit explaining why that version won.

Tag only stable milestones such as the restart baseline or an OJ-verified SOTA promotion. Do not tag an unpromoted submission candidate as current best.
