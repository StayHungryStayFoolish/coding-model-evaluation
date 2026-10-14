# Public data dictionary

- Files contain selected numerical results and customer-facing scenario descriptions.
- Scenario slugs link the catalog and CSVs; model identifiers name the four evaluated models.
- Blank fields mean unavailable or not applicable. They must not be interpreted as measured zero.

All files use UTF-8; CSVs have header rows. USD values retain calculation precision. Displayed report values are rounded.

## `scenarios.json`

There are 33 objects. `scenario` is a descriptive public slug. `track` is `direct_api` or `controlled_engineering`. `category_en`, `category_zh`, `title_en`, `title_zh`, `requirement_en` and `requirement_zh` describe the business work. `runs_per_model` is 3. `requirement_turns` is 5 for the six evolving-requirement projects and 1 for the other tasks; this is not the number of agent tool calls or repair responses.

## `scenario_runs.csv`

396 rows: 21 API scenarios × 4 models × 3 runs, plus 12 engineering tasks × 4 models × 3 runs. The unique key is `(track, scenario, model, run)`.

| Field | Meaning |
|---|---|
| `functional_passed`, `functional_total` | Distinct unambiguous API checks, or hidden engineering checks, passed and evaluated |
| `regression_passed`, `regression_total` | Separate historical compatibility checks for API evolution projects; zero where not applicable |
| `instruction_passed`, `instruction_total` | Corrected engineering instruction checks; zero in the API track |
| `full_success` | 1 if every applicable functional, regression and instruction check passed, otherwise 0 |
| `raw_instruction_passed` | Engineering instruction count before comment/initial-artifact corrections; blank for API |
| `raw_full_success` | Original engineering complete-success flag; blank for API |

API per-model/run denominators are 361 functional and 180 regression checks. Engineering denominators are 120 functional and 48 instruction checks. Checks are not independent samples for statistical inference.

## `scenario_totals.csv`

132 rows: 33 scenarios × 4 models. The unique key is `(track, scenario, model)`. `runs` is 3; `full_successes` sums the corresponding run flags. `total_cost_usd` is the calculated total API cost across all three runs, including measured unsuccessful attempts and feedback repair. It is already recomputed at the report's stated prices; original token-level billing records are not included here.

## `summary.csv`

Eight rows: four models × two tracks.

- `scenario_executions`: 63 for API, 36 for engineering, per model.
- `full_successes`, `full_success_rate_pct`: count and percentage of complete successful executions.
- Functional, regression and instruction count pairs: sums of the matching `scenario_runs.csv` fields.
- `total_cost_usd`: sum of scenario costs.
- `cost_per_success_usd`: total cost divided by full successes.
- `time_unit`: `model_request` for API, `engineering_session` for engineering.
- `median_seconds`, `p90_seconds`: timing statistics from the reviewed results. Request/session traces are not public, so the script checks their format and range but does not reconstruct these statistics.

## `antigravity.csv`

Four rows, one per model. `status` is `measured` or `not_tested`. Counts use 21 scenarios and 361 unambiguous checks per measured model. Sonnet includes compliant retests of four projects. These are historical single-run results, separate from the three-run API data.

`thinking_configuration=tool_managed` describes the disclosure scope, not an asserted numeric effort level. Comparable cost/latency fields are blank for all models. Haiku has no measured scores.

## Checksums

`SHA256SUMS.json` contains hashes of every release file except itself. It is an integrity inventory, not a signature, provenance certification or proof of pre-run test freezing. Changes to data require rerunning arithmetic checks and reviewing the results before the checksum inventory is updated.
