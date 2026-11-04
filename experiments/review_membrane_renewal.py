"""Source-checked material transfer and membrane coexistence, without feedback."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.review_renewal import renewal
from experiments.tool_product_flux import routes,inventory
from scripts.demo_motion_report import metrics_summary


def decide(rows):
    if len(rows)!=12:raise ValueError('Require all12 MIN1M trials')
    groups={}
    for v in ('active','noL','split','nogene'):
        groups[v]=[r for r in rows if r['label'].startswith(f'MIN1M_{v}_s')]
        if len(groups[v])!=3 or {r['seed'] for r in groups[v]}!={0,1,2}:raise ValueError('Need three unique seeds per condition')
    a=groups['active'];n=groups['nogene']
    conditions=dict(whole_new_active_F_two_seeds=sum(r['renewal']['active_wholly_constructed_F']>0 for r in a)>=2,
        membrane_closed_70pct_two_seeds=sum(r['physical']['regular_parent_closed_fraction']>=.7 for r in a)>=2,
        simultaneous_material_and_membrane_two_seeds=sum(r['renewal']['active_wholly_constructed_F']>0 and
            r['physical']['regular_parent_closed_fraction']>=.7 for r in a)>=2,
        nogene_negative=all(r['F_new']==0 and r['renewal']['active_wholly_constructed_F']==0 for r in n))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        interpretation='Screen only. Stop after this cohort regardless of outcome; no auto promotion, tuning, '
            'maintenance/half-renewal claim, or independent validation of a selected preparation.')


def collect(folder,require_complete=True):
    folder=Path(folder);manifest=validate(folder);snap=status(folder)
    if require_complete and (snap['controller_active'] or snap['counts']['complete']!=12):
        raise ValueError('Require complete inactive cohort')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(manifest['tasks'],snap['tasks']):
        if state['phase']!='complete':continue
        p=folder/state['result'];r=read(p)
        if r['scenario']!=task['scenario'] or r['source_sha256']!=hashes or not r['completed'] or r['error']:
            raise ValueError('Completion/provenance mismatch')
        g=r['metrics']['genetics'];flux=routes(r);new=renewal(g);first=new['first_operation_by_wholly_constructed_F']
        audit=read(folder/state['genetic_audit'])
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G_new=g['detached_copy_sets_ever'],
            F_new=g['translated_detached_ever'],renewal=new,physical=metrics_summary(r['metrics'],task['scenario']),
            first_new_active_F=dict(event=first is not None,time=first if first is not None else task['scenario']['duration']),
            formed=flux['formed'],incorporated=flux['incorporated'],inventory=inventory(task['scenario']),
            exposure=audit['exposure'],elapsed_seconds=r['elapsed_seconds'],result_sha256=digest(p)))
    report=dict(counts=snap['counts'],controller_active=snap['controller_active'],rows=rows,
        manifest_sha256=digest(folder/'manifest.json'),decision=decide(rows) if len(rows)==12 else None,
        scope='New complete food-derived F active after expression/detachment. Initial enzymes retained. '
            'Membrane closure sampled on the regular grid; no sealed-boundary or homeostasis proof. '
            'No-event first passages right-censored at1200; noL matches initial PR positions/types, not Langevin velocities or post-initialization RNG.')
    write(folder/'membrane_renewal_review.json',report);return report


if __name__=='__main__':
    from scripts.membrane_renewal_followup import latest
    job=latest();folder=Path(read(job/'job.json')['campaigns'][0])
    print(json.dumps(collect(folder,False),indent=2))
