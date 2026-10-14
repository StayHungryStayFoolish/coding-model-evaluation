"""Validate public files and recompute summary arithmetic. No network or model calls."""
from collections import defaultdict
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('gemini-4-argon', 'claude-opus-5-5', 'claude-sonnet-5-5', 'claude-haiku-5-5')
TRACKS = {'direct_api': 21, 'controlled_engineering': 12}
FILES = (
    '.gitignore', 'README.md', 'README.zh-CN.md',
    'docs/methodology.md', 'docs/methodology.zh-CN.md',
    'docs/data-dictionary.md', 'docs/release-scope.md',
    'reports/report.html', 'data/scenarios.json',
    'data/scenario_runs.csv', 'data/scenario_totals.csv',
    'data/summary.csv', 'data/antigravity.csv', 'tools/recompute_results.py',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(filename):
    with (ROOT/'data'/filename).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def close(actual, expected, label):
    require(abs(Decimal(str(actual))-Decimal(str(expected))) <= Decimal('0.00000001'),
            f'{label}: {actual} != {expected}')


def main():
    hashes = json.loads((ROOT/'SHA256SUMS.json').read_text(encoding='utf-8'))
    require(set(hashes)==set(FILES), 'Checksum inventory differs from the release allowlist')
    for name in FILES:
        p = ROOT/name
        require(not p.is_symlink(), f'Symlink is not permitted: {name}')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[name], f'Checksum mismatch: {name}')

    catalog = json.loads((ROOT/'data/scenarios.json').read_text(encoding='utf-8'))
    require(len(catalog)==33, 'Expected 33 distinct scenarios')
    scenarios = {r['scenario']: r for r in catalog}
    require(len(scenarios)==33, 'Duplicate scenario slug')
    require(all(r['track'] in TRACKS and r['runs_per_model']==3 for r in catalog), 'Invalid catalog track/run count')
    require(sum(r['requirement_turns']==5 for r in catalog)==6, 'Expected six five-turn projects')
    for track, count in TRACKS.items():
        require(sum(r['track']==track for r in catalog)==count, f'Invalid scenario count: {track}')

    executions = rows('scenario_runs.csv')
    require(len(executions)==396, 'Expected 396 scenario-run rows')
    seen, groups, task_groups = set(), defaultdict(list), defaultdict(list)
    pairs = [('functional_passed','functional_total'), ('regression_passed','regression_total'),
             ('instruction_passed','instruction_total')]
    for r in executions:
        track, model, scenario, run = r['track'], r['model'], r['scenario'], int(r['run'])
        key = track, scenario, model, run
        require(key not in seen, f'Duplicate row: {key}')
        seen.add(key)
        require(model in MODELS and run in (1,2,3), f'Invalid model or run: {key}')
        require(scenario in scenarios and scenarios[scenario]['track']==track, f'Invalid scenario/track: {key}')
        for passed, total in pairs:
            require(0<=int(r[passed])<=int(r[total]), f'Invalid count: {key}, {passed}')
        full = int(all(int(r[p])==int(r[n]) for p,n in pairs))
        require(int(r['full_success'])==full, f'Incorrect full success: {key}')
        if track=='controlled_engineering':
            require(int(r['functional_total'])==10 and int(r['instruction_total'])==4 and int(r['regression_total'])==0,
                    f'Invalid engineering denominators: {key}')
            raw = int(r['raw_instruction_passed'])
            require(0<=raw<=4, f'Invalid original instruction count: {key}')
            require(int(r['raw_full_success'])==int(int(r['functional_passed'])==10 and raw==4),
                    f'Incorrect original full success: {key}')
        else:
            require(int(r['instruction_total'])==0 and r['raw_instruction_passed']==r['raw_full_success']=='',
                    f'Invalid API instruction fields: {key}')
        groups[track, model].append(r)
        task_groups[track, scenario, model].append(r)

    expected_tasks={(s['track'],s['scenario'],m) for s in catalog for m in MODELS}
    require(set(task_groups)==expected_tasks, 'Missing scenario/model group')
    for key, items in task_groups.items():
        require({int(r['run']) for r in items}=={1,2,3}, f'Missing independent run: {key}')

    costs, cost_seen = defaultdict(Decimal), set()
    totals = rows('scenario_totals.csv')
    require(len(totals)==132, 'Expected 132 scenario/model totals')
    for r in totals:
        key = r['track'], r['scenario'], r['model']
        require(key in expected_tasks and key not in cost_seen, f'Invalid total key: {key}')
        cost_seen.add(key)
        require(int(r['runs'])==3, f'Invalid run total: {key}')
        require(int(r['full_successes'])==sum(int(x['full_success']) for x in task_groups[key]),
                f'Scenario total mismatch: {key}')
        value = Decimal(r['total_cost_usd'])
        require(value.is_finite() and value>=0, f'Invalid cost: {key}')
        costs[r['track'],r['model']] += value

    expected_groups={(t,m) for t in TRACKS for m in MODELS}
    summary = rows('summary.csv')
    require(len(summary)==8 and {(r['track'],r['model']) for r in summary}==expected_groups,
            'Expected exactly eight model/track summaries')
    for r in summary:
        key = r['track'], r['model']
        items=groups[key]
        n=TRACKS[r['track']]*3
        successes=sum(int(x['full_success']) for x in items)
        require(len(items)==int(r['scenario_executions'])==n, f'Wrong execution count: {key}')
        require(int(r['full_successes'])==successes, f'Wrong success count: {key}')
        for p,t in pairs:
            for field in (p,t):
                require(int(r[field])==sum(int(x[field]) for x in items), f'Wrong summary {field}: {key}')
        for run in (1,2,3):
            subset=[x for x in items if int(x['run'])==run]
            denominators=tuple(sum(int(x[t]) for x in subset) for _,t in pairs)
            require(denominators==((361,180,0) if r['track']=='direct_api' else (120,0,48)),
                    f'Wrong fixed denominators: {key}, run {run}')
        close(Decimal(successes)*100/n, r['full_success_rate_pct'], f'Success rate {key}')
        close(costs[key], r['total_cost_usd'], f'Total cost {key}')
        require(successes>0, f'Undefined cost per success: {key}')
        close(costs[key]/successes, r['cost_per_success_usd'], f'Cost per success {key}')
        require(r['time_unit']==('model_request' if r['track']=='direct_api' else 'engineering_session'),
                f'Wrong timing unit: {key}')
        require(0<=float(r['median_seconds'])<=float(r['p90_seconds']), f'Invalid timing summary: {key}')
        print(f'{r["track"]:23} {r["model"]:20} {successes:2}/{n}  '
              f'{100*successes/n:6.2f}%  ${costs[key]/successes:.4f} per success')

    ag = rows('antigravity.csv')
    require(len(ag)==4 and {r['model'] for r in ag}==set(MODELS), 'Invalid Antigravity model set')
    for r in ag:
        require(r['comparable_cost_usd']==r['comparable_latency_seconds']=='', 'Unexpected Antigravity cost/time')
        if r['model']=='claude-haiku-5-5':
            require(r['status']=='not_tested', 'Haiku Antigravity status must be not_tested')
            require(all(r[k]=='' for k in ['full_successes','scenario_executions','functional_passed','functional_total','thinking_configuration']),
                    'Untested Haiku must have no scores/configuration')
        else:
            require(r['status']=='measured' and r['thinking_configuration']=='tool_managed', 'Invalid Antigravity status')
            require(int(r['scenario_executions'])==21 and 0<=int(r['full_successes'])<=21, 'Invalid Antigravity scenario counts')
            require(int(r['functional_total'])==361 and 0<=int(r['functional_passed'])<=361, 'Invalid Antigravity functional counts')
    print(f'PASS: {len(FILES)} file hashes; 33 scenarios; 396 run rows; 132 scenario totals; 8 summaries.')
    print('Recomputed arithmetic only. Original generation, test execution, billing traces and timing are not reproduced.')


if __name__=='__main__':
    main()
