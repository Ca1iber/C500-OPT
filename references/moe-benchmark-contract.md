# MoE benchmark contract

## Authoritative interfaces

Use the repository versions of:

```text
race_tests/moe/fusedmoe_benchmark.py
race_tests/moe/oj_benchmark.py
race_tests/moe/custom_fusedmoe.py
```

For every verified global-SOTA promotion, the final authority is also:

```text
race_tests/moe/restart-submission/<id>/submission.py
```

Discover the exact CLI and correctness path from the checked-out files. Do not hard-code old shapes or flags into the Skill. Record SHA-256 hashes for the kernel and both benchmark files in every version manifest.

## Integrity rules

- Do not modify benchmark logic while judging a kernel candidate.
- Keep random/input construction, dtype, tolerance, warmup/repeat, synchronization, and timing method unchanged.
- If diagnostic instrumentation requires a benchmark wrapper, archive it and label the run `diagnostic`, not official/OJ verdict.
- Do not replace OJ token/expert distributions with random local distributions.
- Keep `16g`, `sc-16g`, and `64g` results separate.
- Never use a profiler-instrumented run as the clean latency verdict.
- Run `validate_oj_submission.py` before compiling or timing a candidate intended for OJ.
- Development-only profiler and diagnostic scripts may use standard-library/tool imports, but the exact source submitted to OJ may use only the import forms in [oj-submission-contract.md](oj-submission-contract.md).
- A development kernel that is faster but cannot be expressed in a compliant `submission.py` is not an accepted OJ optimization.
- Resolve the incumbent from `restart-submission/SOTA.json` before testing a candidate. Do not substitute the latest version, direct parent, or latest locally fast version.

## Gates

1. Static OJ import validation passes for the exact candidate/submission source.
2. Import/compile succeeds.
3. Functional/correctness path passes the repository tolerance.
4. Official benchmark runs in its authoritative mode.
5. OJ benchmark runs all exact cases in its authoritative mode.
6. Paired/repeated candidate-versus-best measurements exceed the observed noise before acceptance.
7. The exact candidate SHA-256 receives external OJ results for every official case.
8. Compared with the incumbent OJ-verified SOTA under the same metric, no case regresses and at least one case strictly improves.
9. The promoted result is reproduced from `restart-submission/<id>/submission.py`, not only from `custom_fusedmoe.py`.

Use a fast screen only if the repository already exposes one or the user authorizes a diagnostic wrapper. Every accepted/final version must receive a full clean verdict. Missing or pending external OJ scores make the promotion verdict `inconclusive`; correctness-only OJ success is insufficient. Follow [sota-promotion-contract.md](sota-promotion-contract.md).

## Required report fields

- benchmark hashes and commands;
- shape, dtype, expert count, top-k, token distribution, padded rows/blocks;
- warmup/repeat, timing method, synchronization;
- correctness result and tolerances;
- raw per-run values, mean/median/min/max or available statistics;
- comparison against `v000`, previous version, and the incumbent OJ-verified SOTA;
- exact incumbent and candidate OJ score vectors, metric direction, and submission hashes;
- machine and software identity;
- explicit `screen` or `verdict` label.
- candidate staging path and SHA-256; for a promoted SOTA, submission path, import-validator command/output, and confirmation that OJ-tested code is byte-identical to the archived submission.
