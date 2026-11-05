# C500-OPT workflow foundations

C500-OPT organizes the project's accumulated C500/MXMACA/TileLang optimization methods into one reproducible workflow. Use this reference for the shared method and toolchain; use the track-specific contracts for artifact paths and promotion rules.

## Optimization loop

- Resolve the workspace, machine, kernel, reference, inputs, benchmark, and constraints before acting.
- Present the resolved plan before executing an optimization run.
- Establish a correct, measured baseline with exact source and benchmark identities.
- Follow the profile → hypothesis → modify → benchmark → interpret → archive → commit loop.
- State predicted metric changes and a falsifying result before changing the kernel.
- Treat every named iteration as an atomic reproducible state and preserve failed but informative experiments.
- Reassess the bottleneck and mechanism families after three stagnant iterations.
- Restore and fully verify the exact best measured code when stopping.
- Preserve benchmark semantics, complete output initialization, and the full scored execution path.

## C500 toolchain

| Purpose | Tools and evidence |
|---|---|
| Machine and sGPU identity | MetaX C500 and read-only `mx-smi` inspection |
| Stage timing and launch gaps | mcTracer timeline |
| Bottleneck diagnosis | mcProfiler counters, synchronized mx-smi samples, and compiler/resource evidence |
| Correctness and scored latency | Project-native correctness and official/OJ benchmark entrypoints |
| Compiler verification | TileLang lowering, generated device code, MXMACA assembly, and resource usage |
| Performance ceilings | Physical theoretical roof and the measured engineering roof for the current GPU/sGPU configuration |
| Reproducibility | Exact source hashes, commands, environment snapshots, track-specific artifacts, and Git history |

Use the measured paired-run noise band to assess significance. Apply any additional promotion floor only to the track and machine that define it; the active sc-16g MoE restart requires at least 1.2% improvement. NSA uses its own artifact layout and competition requirements.

Continue from the user-approved experiment branch. Create additional branches only for the conditions in [git-protocol.md](git-protocol.md).

Do not run `ncu` or `nvidia-smi` as availability probes. They are not part of the C500 target stack.
