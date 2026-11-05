# TileLang code-generation workflow

## Artifact chain

Capture the exact chain for both baseline and candidate:

```text
custom_fusedmoe.py
→ TileLang/TIR lowering
→ generated MXMACA device C/C++ or CUDA-like source
→ backend assembly/ISA output
→ compiler resource report
```

Name the real artifact format reported by the toolchain; do not call MXMACA assembly “SASS”.

## What to inspect

### Lowering

- grid/block dimensions and linearized CTA mapping;
- loop bounds, unrolling, pipelining, predicates, tail guards;
- buffer scopes, layouts, vectorization, alignment, shared allocation;
- barriers, synchronization, and producer/consumer ordering;
- whether an intended TileLang transformation survived canonicalization.

### Generated device code

- target MMA/MFMA intrinsics and dtype;
- global load/store width and address direction;
- shared-to-local/fragment loads such as `ldmatrix_b` paths;
- repeated address arithmetic, branches, masks, and conversions;
- barrier placement and pipeline order;
- explicit spill or unexpected local-memory access if visible.
- forbidden asynchronous-copy materialization, headers, helper calls, waits, or pipeline tokens;
- user-injected C/C++/CUDA-like/LLVM fragments or foreign-call escape hatches.

### Assembly and resources

- MMA/load/store/barrier instruction mix and ordering;
- vector width and transaction issue pattern;
- register counts, shared memory, maximum waves/occupancy estimate;
- instruction count changes that explain or contradict the hypothesis;
- spills or resource-limit changes.
- async-copy instructions/tokens/waits that were not permitted by the TileLang-only contract.

## Comparison rules

- Diff artifacts from the exact baseline and candidate hashes.
- Normalize timestamps, generated symbol suffixes, and unrelated metadata before structural comparison.
- Do not infer speedup from source aesthetics.
- If source changes but generated code/resources do not, mark the mechanism `not materialized`.
- If generated code changes but the targeted counter does not, re-evaluate the causal model.
- Archive the extraction script and exact command in `restart-scripts/<id>/`.
- Reject the candidate if any official shape uses async copy or injected/foreign code. Missing codegen for a selected shape is `inconclusive`, not evidence of compliance.

Tool/API details vary with TileLang/MXMACA versions. Discover available dump APIs and compiler flags from the checked-out repository and installed compiler instead of hard-coding an old private interface.
