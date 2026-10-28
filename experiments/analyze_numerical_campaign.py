"""Source-checked descriptive N1 comparison; no three-seed convergence certificate."""
import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.campaign import validate
from experiments.analyze_constructed_tool import analyze
from simulator.campaign_io import read, write

BASELINE = ROOT/'outputs/campaigns/campaign_20261027T192723206222Z'


def triage(levels):
    """Fixed prospective alerts on cohort medians, with raw per-seed rows retained."""
    medians = {}
    for factor, rows in levels.items():
        if len(rows) != 3 or {r['seed'] for r in rows} != {0, 1, 2}:
            continue
        medians[factor] = dict(
            catalytic_per_initial_tool=statistics.median(r['catalyzed']/16 for r in rows),
            incorporated_per_initial_gene=statistics.median(r['catalyzed_incorporated']/16 for r in rows),
            closed=statistics.median(r['membrane']['regular_grid_closed_fraction'] for r in rows),
            envelope=statistics.median(r['membrane']['regular_grid_envelope_fraction'] for r in rows))
    alerts = []
    for a, b in ((1, 2), (2, 4)):
        if a not in medians or b not in medians:
            continue
        for key, old in medians[a].items():
            new = medians[b][key]
            if key in ('closed', 'envelope'):
                change = abs(new-old)
                limit = .10 if key == 'closed' else .05
                alert = change > limit
            else:
                change = None if old == 0 else abs(new-old)/abs(old)
                limit = .30
                alert = new != 0 if old == 0 else change > limit
            if alert:
                alerts.append(dict(from_factor=a, to_factor=b, metric=key,
                    old=old, new=new, change=change, threshold=limit))
    return dict(medians=medians, alerts=alerts,
        complete_cohorts=set(medians) == {1, 2, 4}, convergence_established=False,
        caveat='Descriptive median alerts, not significance tests. Three seeds and sparse complete '
            'G/F cannot establish chemical convergence, even without alerts. Shared seed labels '
            'are not common Brownian paths. dt and reaction interval are refined jointly.')


def compare(folder, baseline=BASELINE):
    folder, baseline = Path(folder).resolve(), Path(baseline).resolve()
    manifests = [validate(p) for p in (baseline, folder)]
    physical = [{k: v for k, v in m['source_sha256'].items() if k.startswith('simulator/')}
        for m in manifests]
    if physical[0] != physical[1]:
        raise ValueError('Simulator sources differ from the J3 baseline')
    original = {t['scenario']['seed']: t['scenario'] for t in manifests[0]['tasks']
        if t['label'] == 'J3_k16_bath'}
    if set(original) != {0, 1, 2}:
        raise ValueError('Missing J3 K16 baseline')
    seen = set()
    for task in manifests[1]['tasks']:
        cfg = task['scenario']
        factor = int(cfg['name'].removeprefix('N1_dt'))
        if factor not in (2, 4) or (factor, cfg['seed']) in seen:
            raise ValueError('Unexpected or duplicate refinement task')
        seen.add((factor, cfg['seed']))
        ref = original[cfg['seed']]
        if cfg['chemistry'] != ref['chemistry'] or cfg['duration'] != ref['duration']:
            raise ValueError('Changed chemical laws or horizon')
        expected_engine = dict(ref['engine'])
        expected_engine['dt'] /= factor
        expected_engine['sample_every'] *= factor
        if cfg['engine'] != expected_engine:
            raise ValueError('Unexpected numerical control')
    if seen != {(f, s) for f in (2, 4) for s in range(3)}:
        raise ValueError('Incomplete declared design')
    reports = [read(analyze(p)/'report.json') for p in (baseline, folder)]
    levels = {1: [r for r in reports[0]['rows'] if r['case'] == 'J3_k16_bath'], 2: [], 4: []}
    for row in reports[1]['rows']:
        levels[int(row['case'].removeprefix('N1_dt'))].append(row)
    from datetime import datetime, timezone
    out = folder/('numerical_analysis_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir()
    hashes = {}
    for name in ('experiments/analyze_numerical_campaign.py', 'experiments/analyze_constructed_tool.py',
                 'experiments/inventory_audit.py'):
        src = ROOT/name
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(src.read_bytes())
        hashes[name] = hashlib.sha256(src.read_bytes()).hexdigest()
    result = dict(baseline=str(baseline), campaign=str(folder), reused_baseline_tasks=3,
        simulator_sources_identical=True, analysis_source_sha256=hashes,
        levels=levels, triage=triage(levels))
    write(out/'report.json', result)
    print(json.dumps(result['triage']))
    print(out)
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder', type=Path)
    p.add_argument('--baseline', type=Path, default=BASELINE)
    a = p.parse_args()
    compare(a.folder, a.baseline)
