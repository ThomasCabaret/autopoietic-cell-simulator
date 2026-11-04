"""CT1 provenance checks and prospective renewal/cost screen, no dynamics feedback."""
import sys
from pathlib import Path
from statistics import median
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.review_renewal import renewal


def decide(rows):
    if len(rows)!=9:raise ValueError('Require all9 CT1 trials')
    groups={}
    for v in ('legacy','matched','nogene'):
        g=[r for r in rows if r['label'].startswith(f'CT1_{v}_s')]
        if len(g)!=3 or {r['seed'] for r in g}!={0,1,2}:raise ValueError('Need three unique seeds per variant')
        groups[v]=g
    a,b,n=groups['legacy'],groups['matched'],groups['nogene']
    whole=lambda r:r['renewal']['active_wholly_constructed_F']
    conditions=dict(reference_reproduces_renewal=sum(whole(r)>0 for r in a)>=2,
        matched_whole_tool_active_two_seeds=sum(whole(r)>0 for r in b)>=2,
        matched_G_median_at_least_half=median(r['G_new'] for r in b)>=.5*median(r['G_new'] for r in a),
        matched_F_median_at_least_half=median(r['F_new'] for r in b)>=.5*median(r['F_new'] for r in a),
        no_gene_negative=all(r['F_new']==0 and whole(r)==0 for r in n),
        elapsed_median_below_twice_reference=median(r['elapsed_seconds'] for r in b)<=2*median(r['elapsed_seconds'] for r in a))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='Prerequisite screen only. Timing is a coarse alarm under concurrent load, not a benchmark. '
            'Same capture stiffness alone is not common chemistry, mixed-substrate compatibility or maintenance. Stop for interpretation.')


def collect(folder,require_complete=True):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=9):raise ValueError('Require complete inactive cohort')
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(m['tasks'],s['tasks']):
        if state['phase']!='complete':continue
        p=folder/state['result'];r=read(p)
        if not r['completed'] or r['error'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:raise ValueError('Result provenance/completion mismatch')
        g=r['metrics'];new=renewal(g);first=new['first_operation_by_wholly_constructed_F']
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G_new=g['detached_copy_sets_ever'],
            F_new=g['translated_detached_ever'],renewal=new,elapsed_seconds=r['elapsed_seconds'],result_sha256=digest(p),
            first_new_active_F=dict(event=first is not None,time=first if first is not None else task['scenario']['duration'])))
    report=dict(rows=rows,counts=s['counts'],controller_active=s['controller_active'],manifest_sha256=digest(folder/'manifest.json'),
        decision=decide(rows) if len(rows)==9 else None,
        scope='Finite stocks and prepared enzymes, no loss. No-event first passages right-censored at1200. '
            'Current default unchanged; same H/T curvature expression tested on P/R, not simultaneous H/T/P/R.')
    write(folder/'capture_transfer_review.json',report);return report
