"""Source-checked L3 cohort with unchanged prospective L2 thermal thresholds."""
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.review_lipid_energy import row
from experiments.prepare_lipid_curvature import VARIANTS


def decide(rows):
    if len(rows)!=21:raise ValueError('Need21 cases including three reused references')
    groups={}
    for v in VARIANTS:
        groups[v]=[r for r in rows if r['label'].startswith(f'L3_{v}_s')]
        if len(groups[v])!=3 or {r['seed'] for r in groups[v]}!={0,1,2}:raise ValueError('Require three distinct seeds per condition')
    c=groups['combined'];median=float(np.median([r['lipids'] for r in c]))
    conditions=dict(useful_products_two_seeds=sum(r['lipids']>=4 and r['max_products_per_site_pair']>=2 for r in c)>=2,
        lateral_contacts_two_seeds=sum(r['final_lateral_contacts']>=1 for r in c)>=2,
        exceeds_control_medians=all(median>np.median([r['lipids'] for r in groups[v]]) for v in ('split','no_boost','no_tool')),
        no_false_catalytic_attribution=all(r['catalyzed']==0 for v in ('split','no_tool') for r in groups[v]),
        late_temperature_all=all(.04<=r['mean_T_late']<=.12 for r in c),
        transient_temperature_all=all(r['p95_T_after5']<=.24 for r in c))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        interpretation='Same thresholds as L2; stop after cohort regardless of result. Not a thermodynamic or cell-maintenance certificate.')


def collect(folder,require_complete=True):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=18):raise ValueError('Require all18 new cases complete')
    rows=[row(folder,t,st,m) for t,st in zip(m['tasks'],s['tasks']) if st['phase']=='complete']
    reuse=read(folder/'plan.json')['reused_reference'];ref=Path(reuse['campaign']);rm=validate(ref);rs=status(ref)
    if digest(ref/'manifest.json')!=reuse['manifest_sha256'] or rs['controller_active'] or rs['counts']['complete']!=20:
        raise ValueError('L2 reference cohort changed/incomplete')
    for seed in range(3):
        index=next(i for i,t in enumerate(rm['tasks']) if t['label']==f'L2_combined_s{seed}')
        rows.append(row(ref,rm['tasks'][index],rs['tasks'][index],rm,f'L3_reference_s{seed}'))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,decision=decide(rows) if len(rows)==21 else None,
        scope='18 new t100 trials plus three reused L2 cases. Native tool pose is a constructed start; '
            'does not solve folding energy of newly expressed tools. No P/R competition, membrane insertion or homeostasis.')
    write(folder/'lipid_curvature_review.json',report);return report
