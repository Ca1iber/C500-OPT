#!/usr/bin/env python3
"""Initialize the four evidence directories for one restart iteration."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


VERSION_RE = re.compile(r"^v\d{3}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
MACHINES = ("16g", "sc-16g", "64g", "16g-64g", "sc-16g-64g")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="MoE root, usually race_tests/moe")
    parser.add_argument("--version", required=True, help="Zero-padded version, for example v001")
    parser.add_argument("--slug", required=True, help="Lowercase snake_case optimization direction")
    parser.add_argument("--machine", required=True, choices=MACHINES)
    return parser.parse_args()


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    if not VERSION_RE.fullmatch(args.version):
        raise SystemExit("--version must match vNNN, for example v001")
    if not SLUG_RE.fullmatch(args.slug):
        raise SystemExit("--slug must be lowercase snake_case")

    root = args.root.resolve()
    iteration_id = f"{args.version}_{args.slug}_{args.machine}"
    dirs = {
        "roofline": root / "moe-roofline" / iteration_id,
        "experiment": root / "restart-experiments" / iteration_id,
        "report": root / "restart-rep" / iteration_id,
        "scripts": root / "restart-scripts" / iteration_id,
    }
    collisions = [str(path) for path in dirs.values() if path.exists()]
    if collisions:
        raise SystemExit("Refusing to overwrite existing iteration directories:\n" + "\n".join(collisions))

    created: list[Path] = []
    try:
        for path in dirs.values():
            path.mkdir(parents=True, exist_ok=False)
            created.append(path)

        for relative in (
            "native",
        ):
            (dirs["roofline"] / relative).mkdir(parents=True)
        for relative in (
            "correctness",
            "benchmark",
            "profiler/mcprofiler/raw",
            "profiler/mctracer",
            "profiler/mxsmi",
            "codegen",
        ):
            (dirs["report"] / relative).mkdir(parents=True)

        created_at = datetime.now(timezone.utc).isoformat()
        base_manifest = {
            "iteration_id": iteration_id,
            "version": args.version,
            "slug": args.slug,
            "machine": args.machine,
            "status": "initialized",
            "created_at_utc": created_at,
            "baseline_id": None,
            "parent_id": None,
            "current_sota_id": None,
            "current_sota_submission_sha256": None,
            "current_sota_oj_scores": None,
        }
        write_text(
            dirs["roofline"] / f"{iteration_id}_manifest.json",
            json.dumps({**base_manifest, "kind": "roofline"}, indent=2, ensure_ascii=False) + "\n",
        )
        write_text(
            dirs["report"] / f"{iteration_id}_manifest.json",
            json.dumps({**base_manifest, "kind": "evidence"}, indent=2, ensure_ascii=False) + "\n",
        )
        write_text(
            dirs["experiment"] / f"{iteration_id}_experiment.md",
            f"""# {iteration_id} 实验记录

## 身份

- 状态：initialized
- 机器：{args.machine}
- 基线版本：待填写
- 父版本：待填写
- 当前 OJ SOTA（ID / submission SHA-256 / 各 case 分数）：待填写
- Kernel 路径及 SHA-256：待填写

## 假设卡（改代码前填写）

- Observed evidence / 已观测证据：
- Verified bottleneck / 已验证瓶颈：
- Current hypothesis / 当前假设：
- Proposed mechanism / 拟采用机制：
- Predicted metric changes / 预测指标变化：
- Falsifying result / 证伪条件：
- Correctness and resource risks / 正确性与资源风险：

## 实施经过

- 实际改动：
- 相对计划的偏离：
- Source snapshot：`{iteration_id}_custom_fusedmoe.py`
- Patch：`{iteration_id}.patch`
- Candidate submission：先放在 `candidate_submission.py` 或 `/tmp`，记录 SHA-256；OJ SOTA 门禁通过前禁止创建 `restart-submission/{iteration_id}/`

## 结果

- 结论：待填写（accepted 仅表示全局 OJ SOTA 晋升；否则 rejected / failed / inconclusive）
- 证据报告：`../../restart-rep/{iteration_id}/{iteration_id}_report.md`
""",
        )
        write_text(
            dirs["report"] / f"{iteration_id}_report.md",
            f"""# {iteration_id} 证据报告

## Verdict

- 运行类型：待填写（screen / verdict）
- 结论：initialized
- 一句话因果结论：待填写

## Identity

- Machine：{args.machine}
- Git branch / commit / status：待填写
- Kernel / benchmark hashes：待填写
- Incumbent OJ SOTA ID / SHA-256 / per-case scores：待填写
- Candidate path / SHA-256 / import validation：待填写
- Promoted submission path：仅全局 OJ SOTA 晋升版填写
- KMD / MACA / TileLang / PyTorch / mcProfiler：待填写

## Correctness

- 命令、容差、结果：待填写

## Benchmark

- 官方 benchmark：待填写
- OJ benchmark：待填写
- 与 v000 / 上一版 / incumbent OJ SOTA 比较：待填写
- 外部 OJ incumbent / candidate 各 case 分数及 metric direction：待填写
- SOTA gate（所有 case 不退化且至少一个严格提升）：待填写
- 原始样本及统计：见 `benchmark/`

## Profile

- mcTracer（Step1 / Step2 / launch gap）：待填写
- mcProfiler（仅列出与假设相关的计数器）：待填写
- mx-smi 同步采样：待填写
- Roofline（native 与 re-normalized）：待填写

## Lowering and code generation

- TileLang lowering：待填写
- Generated device code：待填写
- Assembly / resource usage：待填写

## Causal interpretation

- 预测指标是否按方向变化：待填写
- 端到端与分阶段时间是否一致：待填写
- 生成代码是否实际变化：待填写
- 是否超出 paired-run 噪声带：待填写
- 瓶颈是否迁移：待填写
""",
        )

        skill_root = Path(__file__).resolve().parent.parent
        template_root = skill_root / "assets" / "restart-scripts"
        for source in sorted(template_root.iterdir()):
            if source.name == "scripts.md.template":
                target = dirs["scripts"] / f"{iteration_id}_scripts.md"
                content = source.read_text(encoding="utf-8").replace("{{ITERATION_ID}}", iteration_id)
                write_text(target, content)
            else:
                shutil.copy2(source, dirs["scripts"] / source.name)
        shutil.copy2(skill_root / "scripts" / "render_roofline.py", dirs["scripts"] / "render_roofline.py")
        shutil.copy2(
            skill_root / "scripts" / "validate_oj_submission.py",
            dirs["scripts"] / "validate_oj_submission.py",
        )
    except Exception:
        for path in reversed(created):
            shutil.rmtree(path, ignore_errors=True)
        raise

    print(iteration_id)
    for label, path in dirs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
