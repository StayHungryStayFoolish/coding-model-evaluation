# Evaluation methodology

- The evaluation measures executable coding outcomes across 33 custom business scenarios, with separate direct API, controlled engineering and Antigravity results.
- Within each track, models receive the same task requirements and acceptance criteria. Compilers, tests and instruction checks determine scores.
- Repeated runs measure consistency on the same scenarios; they do not increase the number of distinct business scenarios.

[中文](methodology.zh-CN.md) · [Report](../reports/report.html) · [Data dictionary](data-dictionary.md)

## Dataset and business coverage

The dataset is a custom collection of task specifications, initial code and acceptance checks organized around development work. It is not a random sample of customer production traffic. The [bilingual catalog](../data/scenarios.json) lists each scenario and its requirement.

| Category | Scenarios | Examples of tested outcomes |
|---|---:|---|
| Business modules and systems | 9 | Log normalization, dependency scheduling, cache expiry and limits, matching, protocol parsing, rules and WebAssembly generation |
| Evolving requirements | 6 | Five sequential requirement turns for telemetry, reactive state, transaction storage, service recovery, query engines and language tooling |
| Maintenance and quality | 6 | Long-code repair, scoped patches, generated unit tests, security fixes, language migration and SQL |
| Frontend/backend and cross-module engineering | 6 | UI interactions, backend concurrency, approval interfaces, data/page state, cross-module changes and refactoring |
| Upgrades, delivery and operations | 6 | Dependency compatibility, build repair, data migration, CI gates, startup health checks and log-driven repairs |

Frontend checks include browser behavior and input security. Backend checks exercise service logic, transaction behavior and concurrent quota enforcement. Full-stack checks cover approval interfaces, database operations and page state. The report describes these tested components explicitly; it does not relabel service-level checks as production deployment tests.

## Three separate execution tracks

| Track | Tasks and runs | Generation and feedback | Configuration |
|---|---|---|---|
| Direct API | 21 scenarios × 3 runs × 4 models; 540 generations | Single-turn tasks generate once. Six projects evolve over five turns, with conversation history. No compiler/test feedback is supplied during generation. Submitted code is then evaluated. | Argon `HIGH`; Claude `adaptive` + `high`; output limit 64,000 tokens |
| Controlled engineering | 12 tasks × 3 runs × 4 models; 144 sessions | Separate workspaces, shared tool interfaces and public-check feedback. Models can inspect, edit, test and repair; final scoring uses hidden checks and instruction constraints. At most six model responses and fifteen minutes per session. | Argon `HIGH`; Claude `adaptive` + `high`; output limit 32,000 tokens |
| Antigravity | The same 21 scenarios, with one archived result per participating model | Tool-based generation is evaluated separately. The reported compliant set contains no shell/compiler/test execution during generation. Four Sonnet projects were retested for rule compliance. Haiku was not tested. | Underlying settings are tool-managed; internal configuration is not published |

The 21 API scenarios comprise 9 single-turn modules, 6 five-turn projects and 6 maintenance tasks: 9 + 30 + 6 = 45 generations per model/run. Thus 45 × 3 × 4 = 540 generations, while full-scenario success uses 21 × 3 = 63 outcomes per model. Engineering success uses 12 × 3 = 36 sessions per model. The public scenario-run file contains 252 API rows plus 144 engineering rows, or 396 total.

The shared direct API and engineering generation fields are:

```json
{"generationConfig":{"maxOutputTokens":64000,"thinkingConfig":{"thinkingLevel":"HIGH"}}}
```

```json
{"max_tokens":64000,"thinking":{"type":"adaptive"},"output_config":{"effort":"high"}}
```

Engineering changes the output limit to 32,000. These are the relevant generation fields, not full API request examples. Equal names such as high do not establish equal internal compute budgets. Sampling settings otherwise use service defaults; lower or maximum effort settings are not evaluated here.

## Scoring and judge roles

**No model acts as a primary or secondary judge.** Scores are obtained by executing code against expected behavior and checking explicit constraints. GPT-6 Astra (reasoning level high) assisted data review and report analysis, not answer scoring. The report makes no independent-certification claim about this assistance or the origin of the test suite.

| Measure | Definition |
|---|---|
| API unique functional checks | 361 unambiguous checks per model/run; each distinct check is counted once |
| Historical regressions | 180 checks per model/run, covering earlier behavior in the five-turn projects; counted separately from unique functional checks |
| API full-scenario success | Every applicable functional and historical regression check passes across the whole scenario |
| Engineering functional checks | 10 hidden checks per task, 120 per model/run |
| Engineering instruction checks | 4 per task, 48 per model/run: required interfaces, allowed file edits, prohibited changes/dependencies, and required delivery/test claims |
| Engineering full success | All functional and instruction checks pass in the final delivered workspace |
| First-edit success | The first completed edit satisfies final acceptance, distinct from success after repair feedback |

Missing outputs, compilation errors and budget exhaustion remain in the denominator. Assertions from the same scenario and repeated runs are related observations, not additional independent business scenarios.

One language-scoping check had a prompt/test ambiguity. The report consistently excludes it from unique functional scoring, giving 361 rather than 362 checks per run. Engineering instruction checks were also corrected consistently where comments or initial build artifacts caused false violations. The public engineering rows retain original and corrected instruction/full-success values so readers can see the scoring effect.

Final-archive checksums can establish file integrity, but do not prove that every check was frozen before generation. The reviewed pre-run manifests have gaps for some check files and differences in frontend dependency files. The report therefore does not claim fully verified pre-run freezing or independent third-party certification.

## Cost and time

Costs are calculated from measured usage using the prices stated in the report, including billable reasoning output, cache reads and feedback-repair calls. They exclude human work, infrastructure, unperformed repairs and failed transport attempts without usable billing records. They are not invoice reconciliation.

`cost per success = total calculated call cost across the task set / number of complete successes`

The denominator includes successes, while the numerator also includes measured unsuccessful task attempts. This metric does not quote the cost of repairing every remaining failure until all tasks pass.

The report uses Global API pricing verified on October 14, 2026: Argon's promotional effective input/output price is $2/$10 per million tokens through November 30, 2026, with cache reads at $0.10. Opus uses $4/$20/$0.20, Sonnet $2/$10/$0.10 and Haiku $0.10/$0.50/$0.01 for the tested input sizes below 100K. The report also identifies Argon's subsequent $4/$20 standard input/output price; promotional savings must not be carried forward unchanged. Sources: [Google Cloud pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) and [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing).

API timing is measured per model request; engineering timing covers the complete session. These medians and P90s are not interchangeable. Antigravity cost and timing are left blank because comparable records are unavailable.

## Interpretation and reproducibility

The report compares observed code behavior and business implications, not just aggregate pass counts. Small average differences are not described as stable superiority; a nonsignificant difference is not proof of equivalence. Additional tokens or attempts may help, but the report does not assign unmeasured repair costs to a model or treat failure within a budget as permanent incapability.

The [public script](../tools/recompute_results.py) validates and recomputes aggregate results from the published numerical rows. It does not call models or execute original tests. Original prompts, submissions, hidden tests and traces are not distributed in this release. See [release scope](release-scope.md).
