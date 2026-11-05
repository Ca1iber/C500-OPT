# C500-OPT

面向沐曦 C500 / MXMACA / TileLang 的 GPU 内核优化技能，将项目实践沉淀为可复现、可解释、可提交的实验流程。适用于 Fused MoE GEMM、Native Sparse Attention（NSA）等 C500 算子任务。

## 工作流程

1. **确认实验身份**：记录机器与 sGPU 配置、Git 版本、源码哈希和测试入口。
2. **建立正确基线**：通过正确性检查，运行项目原生的官方与 OJ benchmark。
3. **定位性能瓶颈**：结合 mcTracer、mcProfiler、mx-smi、Roofline 和编译生成代码判断限制因素。
4. **提出可证伪假设**：先写证据、预期指标变化和证伪条件，再修改一个明确机制。
5. **验证候选版本**：检查正确性、OJ 合规和端到端性能，用测量证据解释收益。
6. **归档并提交**：保存源码、补丁、命令、结果与结论，再进入下一轮。

MoE 与 NSA 分别使用各自的归档路径和验收规则。当前 sc-16g MoE 的逐 case 不退步要求及 1.2% 晋升门槛，不自动适用于 NSA。

## 安装与调用

将仓库克隆到本机的技能目录；以下示例适用于默认的 `~/.codex/skills` 位置：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Ca1iber/C500-OPT.git ~/.codex/skills/c500-opt
```

若技能已经存在，请在现有目录之外检查更新，避免覆盖本地修改。使用自定义 `CODEX_HOME` 时，将安装位置调整为其下的 `skills/c500-opt`。

显示名称为 **C500-OPT**，技能 ID 为 `c500-opt`。安装后在下一轮对话中调用：

```text
使用 $c500-opt，先确认目标机器、待优化内核和官方测试入口，再建立基线并定位瓶颈。
```

该仓库提供优化流程、验证工具和脚本模板。实际编译、正确性测试、benchmark 和 profiling 需要目标项目与 C500 算力环境；执行时遵守项目的 `AGENTS.md` 和用户约束。

## 文件结构

```text
SKILL.md                 技能入口、实验闭环与关键约束
agents/openai.yaml       显示名称与默认调用提示
references/              硬件、测量、提交、归档和 Git 规则
scripts/                 迭代初始化、验证、汇总与 Roofline 工具
assets/restart-scripts/  环境采集、测试、profiling 与代码生成模板
LICENSE                  MIT 许可证及保留的版权声明
```

详细规则从 [SKILL.md](SKILL.md) 开始，完整流程概述见 [workflow-foundations.md](references/workflow-foundations.md)。

## 许可证

本仓库保留 [MIT 许可证及版权声明](LICENSE)。
