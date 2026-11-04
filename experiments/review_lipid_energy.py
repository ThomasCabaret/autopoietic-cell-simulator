"""Collect the fixed L2 cohort, including the explicitly reused frozen L1 case."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.prepare_lipid_energy import VARIANTS


def row(folder,task,state,manifest,label=None):
    path=folder/state['result'];r=read(path);hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    if r['source_sha256']!=hashes or r['scenario']!=task['scenario'] or r['error'] or not r['completed']:raise ValueError('Evidence mismatch')
    g=r['metrics'];h=read(folder/state['motion_audit'])['history'];late=[x['kinetic_temperature'] for x in h if x['time']>=75.]
    after=[x['kinetic_temperature'] for x in h if x['time']>=5.];births=g['births']
    return dict(label=label or task['label'],seed=task['scenario']['seed'],lipids=g['lipids_formed'],
        catalyzed=g['catalyzed_lipids'],max_products_per_site_pair=g['max_products_per_site_pair'],
        final_lateral_contacts=g['history'][-1]['lateral_contacts'],
        first_lipid=dict(event=bool(births),time=births[0]['time'] if births else task['scenario']['duration']),
        mean_T_late=float(np.mean(late)),p95_T_after5=float(np.quantile(after,.95)),max_T=max(x['kinetic_temperature'] for x in h),
        transition_stats=g.get('transition_stats'),elapsed_seconds=r['elapsed_seconds'],
        result_sha256=digest(path),source_manifest_sha256=digest(folder/'manifest.json'),reused=label is not None)


def decide(rows):
    if len(rows)!=21:raise ValueError('Require21 cases including one reused reference')
    groups={}
    for v in VARIANTS:
        groups[v]=[r for r in rows if r['label'].startswith(f'L2_{v}_s')]
        if len(groups[v])!=3 or {r['seed'] for r in groups[v]}!={0,1,2}:raise ValueError('Need three unique seeds per condition')
    c=groups['combined'];med=float(np.median([r['lipids'] for r in c]))
    conditions=dict(useful_products_two_seeds=sum(r['lipids']>=4 and r['max_products_per_site_pair']>=2 for r in c)>=2,
        lateral_contacts_two_seeds=sum(r['final_lateral_contacts']>=1 for r in c)>=2,
        exceeds_control_medians=all(med>np.median([r['lipids'] for r in groups[v]]) for v in ('split','no_boost','no_tool')),
        no_false_catalytic_attribution=all(r['catalyzed']==0 for v in ('split','no_tool') for r in groups[v]),
        late_temperature_all=all(.04<=r['mean_T_late']<=.12 for r in c),
        transient_temperature_all=all(r['p95_T_after5']<=.24 for r in c))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        interpretation='Finite descriptive mechanism screen, not a thermodynamic certificate; stop for interpretation regardless of outcome.')


def collect(folder,require_complete=True):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=20):raise ValueError('Require all20 new cases complete')
    rows=[row(folder,t,st,m) for t,st in zip(m['tasks'],s['tasks']) if st['phase']=='complete']
    reuse=read(folder/'plan.json')['reused_reference'];ref=Path(reuse['campaign']);rm=validate(ref);rs=status(ref)
    if digest(ref/'manifest.json')!=reuse['manifest_sha256'] or rs['controller_active'] or rs['counts']['complete']!=1:
        raise ValueError('Reused reference differs or incomplete')
    rows.append(row(ref,rm['tasks'][0],rs['tasks'][0],rm,'L2_reference_s0'))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,
        decision=decide(rows) if len(rows)==21 else None,
        scope='20 new short trials plus one frozen L1 reference, no P/R or expression. '
            'No-event times censored100; kinetic temperatures measured, not assumed equal to thermostat. '
            'Product counts are finite stocks, not steady useful rates or homeostasis.')
    write(folder/'lipid_energy_review.json',report);return report
