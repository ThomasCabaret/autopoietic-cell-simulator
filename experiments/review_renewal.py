"""Count actual whole-tool replacement and subsequent activity, excluding seeds."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.tool_product_flux import routes,inventory


def renewal(metrics):
    assembly=metrics['assembly_state'];births={int(e['support']):float(e['time']) for e in assembly['events']}
    active=set();first=None;operations=0
    for e in assembly['catalytic_events']:
        if e['chain_kind']!='expressed' or not e.get('chain'):continue
        chain=tuple(sorted(e['chain']))
        if not all(q in births and births[q]<e['time'] for q in chain):continue
        active.add(chain);operations+=1;first=e['time'] if first is None else min(first,e['time'])
    return dict(wholly_constructed_detached_F=metrics['constructed_detached_F'],
        active_wholly_constructed_F=len(active),operations_by_wholly_constructed_F=operations,
        first_operation_by_wholly_constructed_F=first,
        criterion='A complete F certified expressed and detached before operation; every actual support/rung born from free P/R earlier. No turnover permitted.')


def decide(rows):
    if len(rows)!=9:raise ValueError('Need all9 renewal trials')
    groups={}
    for v in ('active','split','nogene'):
        groups[v]=[r for r in rows if r['label'].startswith(f'MIN1R_{v}_s')]
        if len(groups[v])!=3 or {r['seed'] for r in groups[v]}!={0,1,2}:raise ValueError('Need3 unique seeds per condition')
    a=groups['active'];n=groups['nogene']
    conditions=dict(whole_new_tool_two_seeds=sum(r['renewal']['wholly_constructed_detached_F']>0 for r in a)>=2,
        whole_new_tool_active_two_seeds=sum(r['renewal']['active_wholly_constructed_F']>0 for r in a)>=2,
        nogene_negative=all(r['F_new']==0 and r['renewal']['active_wholly_constructed_F']==0 for r in n))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,
        limitation='Selected small constructed-start renewal test, no integrated membrane or sustained homeostasis; stop for interpretation.')


def review():
    folder=Path((ROOT/'outputs/renewal_campaigns/latest.txt').read_text().strip());m=validate(folder);s=status(folder)
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,st in zip(m['tasks'],s['tasks']):
        if st['phase']!='complete':continue
        path=folder/st['result'];r=read(path)
        if not r['completed'] or r['error'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:
            raise ValueError('Invalid renewal result')
        g=r['metrics'];flux=routes(r)
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G_new=g['detached_copy_sets_ever'],F_new=g['translated_detached_ever'],
            renewal=renewal(g),formed=flux['formed'],incorporated=flux['incorporated'],inventory=inventory(task['scenario']),result_sha256=digest(path)))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,decision=decide(rows) if len(rows)==9 else None)
    write(folder/'renewal_review.json',report);print(json.dumps(report,indent=2));return report


if __name__=='__main__':review()
