"""Selected400-unit continuations by full recipes; compare the entire L3 prefix."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_lipid_curvature import scenario as previous,REFERENCE as OLD_REFERENCE
from simulator.config import resolve
from simulator.campaign_io import read,write
from scripts.campaign import validate,status,digest

REFERENCE=ROOT/'research/campaign_recipes/L3_20261104T164655147905Z'


def plan(ref):
    tasks=[]
    for seed in range(3):
        cfg=previous(seed,'combined');cfg.update(duration=400.,name=f'L4_tail_s{seed}',branch='L4');tasks.append(dict(scenario=resolve(cfg)))
    return dict(name='L4 selected thermal tails, unchanged chemistry',workers=1,checkpoint_seconds=30.,record_trajectory=False,
        tasks=tasks,reused_reference=dict(campaign=str(ref),manifest_sha256=digest(ref/'manifest.json')),
        comparison_policy='BATCH_39_PLAN:3 selected400-unit runs, exact L3 prefix audit, no independent repetition claim, '
            'no new chemistry or automatic second phase. Closed finite stocks do not demonstrate homeostasis.')


def decide(rows):
    if len(rows)!=3 or {r['seed'] for r in rows}!={0,1,2}:raise ValueError('Need three selected seeds')
    return dict(run_transfer=False,prefixes_exact=all(r['prefix_exact'] for r in rows),
        cool_tail_all=all(.04<=r['T_350_400']<=.12 for r in rows),
        interpretation='Selected thermal follow-up only; keep original L3 screen refused. Stop for interpretation.')


def collect(folder,require_complete=True):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=3):raise ValueError('Require complete inactive three-case cohort')
    reuse=read(folder/'plan.json')['reused_reference'];ref=Path(reuse['campaign']);rm=validate(ref);rs=status(ref)
    if digest(ref/'manifest.json')!=reuse['manifest_sha256'] or rs['controller_active'] or rs['counts']['complete']!=18:raise ValueError('L3 reference changed/incomplete')
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,st in zip(m['tasks'],s['tasks']):
        if st['phase']!='complete':continue
        p=folder/st['result'];r=read(p);seed=task['scenario']['seed']
        if r['source_sha256']!=hashes or r['scenario']!=task['scenario'] or r['error'] or not r['completed']:raise ValueError('L4 evidence differs')
        idx=next(i for i,t in enumerate(rm['tasks']) if t['label']==f'L3_combined_s{seed}');old=read(ref/rs['tasks'][idx]['result'])
        oldhashes={k:v for k,v in rm['source_sha256'].items() if k.startswith('simulator/')}
        if old['source_sha256']!=oldhashes or old['scenario']!=rm['tasks'][idx]['scenario'] or not old['completed'] or old['error']:raise ValueError('L3 evidence differs')
        h=read(folder/st['motion_audit'])['history'];oh=read(ref/rs['tasks'][idx]['motion_audit'])['history'];g=r['metrics'];og=old['metrics']
        exact=([x for x in g['history'] if x['time']<=100.]==og['history'] and
            [x for x in g['births'] if x['time']<=100.]==og['births'] and [x for x in h if x['time']<=100.]==oh)
        if not exact:raise ValueError('Selected follow-up prefix differs')
        def mean(lo,hi):
            values=[x['kinetic_temperature'] for x in h if lo<=x['time']<=hi];return sum(values)/len(values)
        rows.append(dict(label=task['label'],seed=seed,prefix_exact=exact,T_100_200=mean(100,200),T_200_300=mean(200,300),
            T_300_400=mean(300,400),T_350_400=mean(350,400),lipids=g['lipids_formed'],contacts=g['history'][-1]['lateral_contacts'],
            last_birth=max((e['time'] for e in g['births']),default=None),births_after300=sum(e['time']>=300 for e in g['births']),
            result_sha256=digest(p),reference_result_sha256=digest(ref/rs['tasks'][idx]['result'])))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,decision=decide(rows) if len(rows)==3 else None,
        scope='Three selected longer horizons, finite stock and exact observed prefix, no independence or steady-fed-cell claim.')
    write(folder/'thermal_tail_review.json',report);return report
