# Coding 模型业务场景评测

- 以 33 个业务场景覆盖 Coding 生命周期的主要阶段，从需求开发到维护、升级与交付，对比 Gemini 4 Argon 与 Claude Opus、Sonnet、Haiku 5.5。
- 分数来自可执行检查，不由裁判模型打分；API、受控工程开发与 Antigravity 分别呈现。
- 本仓库公开双语报告、评测方法和脱敏数值结果，提供 Python 脚本重新汇总并校验数据。

[English](README.md) · [双语 HTML 报告](reports/report.html) · [评测方法](docs/methodology.zh-CN.md) · [场景目录](data/scenarios.json)

本报告基于定制 Coding 场景实测整理，**不代表 Google 官方评测数据或结论**。报告日期：2026 年 10 月 14 日；版本：1.6。

## 查看报告

下载 [report.html](reports/report.html)，用浏览器打开。默认英文，可切换中文，支持模型对比、深浅色主题和打印。GitHub 文件页面展示 HTML 源码，不直接呈现网页。

报告说明具体业务差异，包括 Rust/WebAssembly 编译器交付、生成单测的误报、缺陷补丁是否真正生效、事务边界处理和前后端功能实现，同时保留其他模型表现更好的场景。

## 核心结果

完整成功要求通过所有适用的无歧义功能、回归和指令约束检查。

| 模型 | API 完整成功场景 / 63 | API 每成功场景费用 | 工程完整成功会话 / 36 | 工程每成功任务费用 |
|---|---:|---:|---:|---:|
| Gemini 4 Argon | 56 / 63 | $0.3396 | 36 / 36 | $0.1214 |
| Claude Opus 5.5 | 54 / 63 | $0.6120 | 36 / 36 | $0.2537 |
| Claude Sonnet 5.5 | 52 / 63 | $0.2217 | 36 / 36 | $0.0997 |
| Claude Haiku 5.5 | 47 / 63 | $0.0296 | 35 / 36 | $0.0073 |

33 个不同场景＝21 个 API 场景＋12 个工程任务，每模型各运行三次。Antigravity 复用前述 21 个场景，不额外计数；按无歧义口径，Argon 完成 21 个、Opus 完成 20 个、Sonnet 完成 19 个，Haiku 未参加该轨道。

费用由实际用量按 2026-10-14 的价格重新计算，包含计费思考输出、缓存读取和反馈修复调用。Argon 采用截至 2026-11-30 的优惠有效价，输入 / 输出为每百万 Token $2 / $10。它们是计算所得 API 费用，不是客户账单，也不包含人工交付成本，详见[方法说明](docs/methodology.zh-CN.md)。

## 谁负责评分？

**本评测没有 primary / secondary judge model。** 编译器、运行环境、功能测试、回归测试和指令约束检查决定验收结果。GPT-6 Astra（推理档位 high）辅助数据复核与报告分析，不给模型答案打分，也不构成独立第三方认证。

API 与受控工程请求显式设置 Argon `thinkingLevel: HIGH`；Claude 为 `thinking: adaptive`、`effort: high`。相同名称不代表跨厂商计算预算相同。Antigravity 的底层参数由工具管理，内部配置不在本次公开范围内。

## 重新汇总结果

需要 Python 3.10+，只使用标准库，不需要凭据、网络连接或模型调用。

```bash
git clone https://github.com/StayHungryStayFoolish/coding-model-evaluation.git
cd coding-model-evaluation
python3 tools/recompute_results.py
```

脚本校验 33 个场景、396 条场景运行结果、132 条场景模型汇总和 8 条模型轨道汇总，并重新计算成功率、断言总数、单位成功成本和文件校验值。

**本次公开的是报告与结果数据，不是完整评测执行包。** 原始提示词、提交代码、隐藏测试和执行日志没有发布，因此脚本可复核公开数据的算术一致性，不能从原始材料独立复现生成、执行、Token 计费或耗时。文件说明见[英文首页](README.md#files)、[数据字典](docs/data-dictionary.md)和[公开范围](docs/release-scope.md)。
