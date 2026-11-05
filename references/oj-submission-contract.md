# OJ submission contract

## Import allowlist

Apply this gate to every candidate source intended for OJ and every archived `submission.py`. The only allowed root packages are:

```text
torch
tilelang
math
```

TileLang may be introduced only by these exact statements:

```python
import tilelang
import tilelang.language as T
from tilelang import jit
from tilelang.intrinsics import make_mma_swizzle_layout
from tilelang.layout import make_swizzled_layout
```

Use any needed subset. Do not alias these names differently, combine them with another import, or import another TileLang module or symbol. `make_swizzled_layout` is an OJ-verified exception exposed from `tilelang.layout`; do not generalize that exception to other layout symbols. Continue to reject `tilelang.autotuner`, private emitter modules, and direct compiler-internal imports.

Imports whose root is `torch` or `math` are allowed. Reject every other root, including `tvm`, `tir`, `typing`, `numpy`, `os`, `sys`, and `importlib`. Reject dynamic `__import__` calls. Builtins require no import.

This restriction applies to submitted kernel source, not to benchmark/profile/archive helper scripts. Helper scripts remain outside `submission.py` and may use the standard library or profiling tools.

## TileLang-only kernel contract

Implement all kernel data movement, synchronization, arithmetic, and MMA through OJ-allowed TileLang primitives. Python helpers may expand to TileLang IR, and the host wrapper may use `torch` for workspace allocation or caching, but submitted kernel work must not escape to Torch, injected device code, or external functions.

The following are hard failures in development kernels, staged candidates, and archived submissions:

- any asynchronous copy API or lowering, including MACA/MXMACA async-copy builtins, `maca_async.h`, `memcpy_async`, continuous-pipeline copies, async waits/tokens, and `tl.maca_memcpy_async`;
- any C/C++, CUDA-like, LLVM, or other foreign-source injection, including `T.import_source` and embedded headers or device functions;
- any foreign-call escape hatch, including `T.call_extern`, `T.call_packed`, and `T.call_cpacked`;
- any mechanism whose selected-shape lowering or generated device code materializes one of the above even when its source-level flag appears false.

`T.copy`, `T.sync_threads`, TileLang MMA/intrinsic primitives, layouts, and `T.Pipelined(..., num_stages=1)` are not rejected merely by name. They are legal only when the exact selected configurations lower without asynchronous copy or foreign-code injection. Do not assume `num_stages=1` proves this; inspect all official cases.

## Required validation

Run before the first candidate benchmark and again on the final archived submission:

```bash
python <skill>/scripts/validate_oj_submission.py path/to/submission.py
```

After compiling every official/OJ shape, rerun it with all generated device sources:

```bash
python <skill>/scripts/validate_oj_submission.py path/to/submission.py \
  --generated-code case1_generated_device.cpp \
  --generated-code case2_generated_device.cpp \
  --generated-code case3_generated_device.cpp
```

Also inspect the corresponding ISA for async-copy materialization because backend spelling can vary. Archive the source scan, generated-code scan, and ISA conclusion. Any uncertain or missing selected-shape codegen is `inconclusive`, not compliant.

For a staged candidate, archive the successful stdout in its experiment evidence. After and only after SOTA promotion, copy it to:

```text
race_tests/moe/restart-submission/<id>/oj_import_validation.txt
```

After promotion, record the file hash:

```bash
sha256sum race_tests/moe/restart-submission/<id>/submission.py
```

Static validation does not prove the file is self-contained or that lowering stays synchronous. Also execute it in the same isolated import context used by the OJ wrapper, audit generated code and ISA for all selected shapes, and run all correctness/benchmark gates from this exact file.

## Staging and promoting a SOTA candidate

For a version that is ready for external OJ evaluation:

1. Create `/tmp/<id>_submission.py` or `restart-experiments/<id>/candidate_submission.py`; do not create `restart-submission/<id>/` yet.
2. Use `race_tests/moe/submission.py` only to learn the required `run_kernel` interface and top-level layout.
3. Move or inline every required kernel helper into the candidate without importing forbidden/private modules.
4. Replace development-only compiler-internal operations. A mechanism requiring `tvm`/`tir`, asynchronous copy, injected foreign code, or external calls has not produced an OJ-valid optimization until it is re-expressed using the allowlisted TileLang primitive surface.
5. Run static source validation, all-shape generated-code and ISA validation, functional correctness, official benchmark, exact local OJ benchmark, and paired comparison from the exact candidate SHA-256.
6. Submit those exact bytes to the external OJ and record numeric results for every official case.
7. Compare against the incumbent in `restart-submission/SOTA.json`. Require no case regression and at least one strict improvement under the same metric.
8. Only after that gate passes, create `restart-submission/<id>/`, copy the exact candidate bytes to `submission.py`, save validation output and `submission.sha256`, update `SOTA.json`, and cite the promotion evidence in the report/manifest/commit.

Never call a version accepted based only on development-kernel measurements, OJ correctness, or an improvement over a non-SOTA parent. Missing or pending OJ performance results are `inconclusive`. If packaging changes generated code or performance, the submission results supersede the development results. Follow [sota-promotion-contract.md](sota-promotion-contract.md).
