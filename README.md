# Coding Model Evaluation

- Compare Gemini 4 Argon with Claude Opus, Sonnet and Haiku 5.5 on 33 business scenarios spanning the main stages of the coding lifecycle, from feature development to maintenance, upgrades and delivery.
- Scores come from executable checks, not a judge model. Direct API, controlled engineering and Antigravity results are reported separately.
- This release includes a bilingual report, methodology and sanitized numerical results. The included Python script validates and recomputes the published aggregates.

[中文说明](README.zh-CN.md) · [Bilingual HTML report](reports/report.html) · [Methodology](docs/methodology.md) · [Scenario catalog](data/scenarios.json)

This is a practitioner evaluation based on a custom task set, **not official Google evaluation data or conclusions**. Report date: October 14, 2026. Report edition: 1.6.

## Read the report

Download [report.html](reports/report.html) and open it in a browser. The report defaults to English and includes a Chinese language selector, interactive comparisons, light/dark themes and print support. GitHub's file view displays the HTML source; it does not render the report as a website.

The report explains concrete differences: compiling and running a Rust/WebAssembly compiler, avoiding false failures in generated unit tests, applying effective defect repairs, handling transaction boundaries, and delivering frontend/backend features. It also retains the tasks where another model performed better.

## Results at a glance

Full success requires all applicable unambiguous functional, regression and instruction checks to pass.

| Model | Direct API: successful scenarios / 63 | API cost per success | Engineering: successful sessions / 36 | Engineering cost per success |
|---|---:|---:|---:|---:|
| Gemini 4 Argon | 56 / 63 | $0.3396 | 36 / 36 | $0.1214 |
| Claude Opus 5.5 | 54 / 63 | $0.6120 | 36 / 36 | $0.2537 |
| Claude Sonnet 5.5 | 52 / 63 | $0.2217 | 36 / 36 | $0.0997 |
| Claude Haiku 5.5 | 47 / 63 | $0.0296 | 35 / 36 | $0.0073 |

The 33 distinct scenarios comprise 21 direct API scenarios and 12 engineering tasks, each run three times per model. Antigravity reuses the 21 API scenarios and does not add new scenarios: Argon completed 21, Opus 20 and Sonnet 19 under the unambiguous scoring rule; Haiku was not tested in that track.

Costs are recalculated from measured usage at the stated October 14, 2026 prices, including billable reasoning, cache reads and feedback repairs. Argon uses a promotional effective input/output price of $2/$10 per million tokens through November 30, 2026. These are calculated API costs, not customer invoices or estimates of human delivery effort. See [pricing and interpretation](docs/methodology.md#cost-and-time).

## Who scores the results?

**There is no primary or secondary judge model.** Compilers, runtimes, functional tests, regression checks and instruction checks determine acceptance. GPT-6 Astra, with reasoning level high, assisted data review and report analysis; it did not assign the benchmark scores. This assistance is not an independent third-party certification.

Direct API and engineering requests explicitly set Argon `thinkingLevel: HIGH` and Claude `thinking: adaptive` with `effort: high`. These settings do not imply equal computation across vendors. Antigravity manages its own underlying settings; internal configuration is not part of this release.

## Verify the numerical results

Python 3.10+ and the standard library are sufficient. No credentials, model calls, network access or paid services are needed.

```bash
git clone https://github.com/StayHungryStayFoolish/coding-model-evaluation.git
cd coding-model-evaluation
python3 tools/recompute_results.py
```

The script checks the 33-scenario catalog, all 396 scenario-run rows, 132 scenario/model totals, fixed denominators and eight model/track summaries. It recomputes success rates, assertion totals and cost per success, and verifies release-file checksums.

**This is a report-and-results release, not the complete benchmark execution package.** Original prompts, submitted code, hidden tests and execution logs are excluded. Consequently, the script can validate published arithmetic but cannot independently reproduce model generations, test execution, token billing or timing from original traces. See [release scope](docs/release-scope.md) and the [data dictionary](docs/data-dictionary.md).

## Files

| Location | Contents |
|---|---|
| `reports/report.html` | English/Chinese customer-facing report |
| `docs/methodology.md`, `docs/methodology.zh-CN.md` | Tasks, configuration, execution, scoring and interpretation |
| `data/scenarios.json` | 33 business scenarios with bilingual names and requirements |
| `data/scenario_runs.csv` | Per-model, per-scenario, per-run numerical acceptance results |
| `data/scenario_totals.csv` | Three-run success counts and calculated API costs |
| `data/summary.csv` | Quality, cost and timing by model and track |
| `data/antigravity.csv` | Separate historical Antigravity results; missing values remain blank |
| `tools/recompute_results.py` | Offline consistency and aggregation checks |
| `SHA256SUMS.json` | Integrity hashes for the release files |

Please keep published results attributed to this specific task set and configuration. Repository contents do not establish official vendor endorsement, universal model equivalence or a guarantee of production success.
