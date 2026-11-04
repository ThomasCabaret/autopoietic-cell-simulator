"""MX1 prospective gate and finite-stock transfer report; observation only."""
import sys
from pathlib import Path
from statistics import median
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from experiments.review_renewal import renewal


def decide(rows):
    if len(rows)!=12:raise ValueError('Require all12 MX1 trials')
    groups={}
    for v in ('mixed','uncaptured','noHT','nogene'):
        g=[r for r in rows if r['label'].startswith(f'MX1_{v}_s')]
        if len(g)!=3 or {r['seed'] for r in g}!={0,1,2}:raise ValueError('Require three unique seeds per condition')
        groups[v]=g
    m,u,n,g=[groups[k] for k in ('mixed','uncaptured','noHT','nogene')]
    active=lambda r:r['renewal']['active_wholly_constructed_F']>0
    conditions=dict(noHT_reference_active_two_seeds=sum(active(r) for r in n)>=2,
        G_median_at_least_half_uncaptured=median(r['G_new'] for r in m)>=.5*median(r['G_new'] for r in u),
        F_median_at_least_half_uncaptured=median(r['F_new'] for r in m)>=.5*median(r['F_new'] for r in u),
        same_seed_material_lipids_and_use_two_seeds=sum(active(r) and r['catalyzed_lipids']>=4 and
            r['max_products_per_site_pair']>=2 and r['new_lipids_later_contacted']>0 for r in m)>=2,
        whole_food_tool_catalyzes_lipid_two_seeds=sum(r['lipids_from_whole_food_F']>0 for r in m)>=2,
        nogene_negative=all(r['F_new']==0 and r['lipids_from_expressed_F']==0 for r in g),
        no_false_catalysis=all(r['catalyzed_lipids']==0 for r in u+n),
        atom_ports_valid=all(r['atom_port_invariant_failures']==0 for r in rows))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='One finite mixed bath, not a cell membrane, loss/renewal maintenance or thermal closure. '
            'Stop for interpretation, no second phase, retry or default promotion.')


def collect(folder,require_complete=True,decision_fn=decide):
    folder=Path(folder);m=validate(folder);s=status(folder)
    if require_complete and (s['controller_active'] or s['counts']['complete']!=12):raise ValueError('Require complete inactive cohort')
    hashes={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')};rows=[]
    for task,state in zip(m['tasks'],s['tasks']):
        if state['phase']!='complete':continue
        p=folder/state['result'];r=read(p)
        if r['error'] or not r['completed'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:raise ValueError('Completion/provenance mismatch')
        stats=r['metrics'];g=stats['genetics'];h=stats['history'];renew=renewal(g)
        temp=read(folder/state['motion_audit'])['history'];horizon=task['scenario']['duration']
        late=[q['kinetic_temperature'] for q in temp if q['time']>=.75*horizon]
        first=next((e['time'] for e in stats['births'] if e['chain_kind']=='expressed' and e['chain'] and
            all(any(b['support']==a and b['time']<e['time'] for b in g['assembly_state']['events']) for a in e['chain'])),None)
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],G_new=g['detached_copy_sets_ever'],
            F_new=g['translated_detached_ever'],renewal=renew,
            **{k:stats[k] for k in ('catalyzed_lipids','lipids_from_expressed_F','lipids_from_whole_food_F',
                'whole_food_F_active_on_lipids','max_products_per_site_pair','new_lipids_later_contacted','atom_port_invariant_failures')},
            lipids=stats['lipids_formed'],final_lateral_contacts=h[-1]['lateral_contacts'],
            first_whole_F_to_L=dict(event=first is not None,time=first if first is not None else horizon),
            mean_T_late=float(np.mean(late)),max_T=max(q['kinetic_temperature'] for q in temp),
            sampled_mean_lipid_occupied_sites=float(np.mean([q['lipid_ligands'] for q in h])),
            sampled_mean_genetic_occupied_sites=float(np.mean([q['genetic_ligands'] for q in h])),
            sampled_wrong_double_edge_time=sum((b['time']-a['time'])*a['wrong_double_edges'] for a,b in zip(h,h[1:])),
            elapsed_seconds=r['elapsed_seconds'],result_sha256=digest(p),motion_sha256=digest(folder/state['motion_audit'])))
    report=dict(counts=s['counts'],controller_active=s['controller_active'],rows=rows,
        decision=decision_fn(rows) if len(rows)==12 else None,manifest_sha256=digest(folder/'manifest.json'),
        scope='Fixed finite stocks. Missing events censored at1200; all initial tools retained. '
            'Occupation is sampled every0.5, not exact integrated reaction exposure. '
            'NoHT initial PR positions match, smaller velocity array changes PRNG; uncaptured is a law ablation.')
    write(folder/'mixed_synthesis_review.json',report);return report
