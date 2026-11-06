"""CC1 short first-dynamics gates; component cycles are not vesicle certificates."""
from pathlib import Path
from collections import Counter
from scripts.campaign import validate,status,digest
from simulator.campaign_io import read,write
from simulator.checkpoint import load
from simulator.observations import components
from simulator.observations import area
from simulator.membrane_bath import polygon_simple
from experiments.mixed_calibration import weighted
import numpy as np


def decide(rows):
    if len(rows)!=6:raise ValueError('Require six CC1 cases')
    groups={k:[r for r in rows if r['variant']==k] for k in ('integrated','assembly')}
    if any(len(g)!=3 or {r['seed'] for r in g}!={0,1,2} for g in groups.values()):raise ValueError('Require three seeds per variant')
    conditions=dict(final_ports=all(r['final_ports_valid'] for r in rows),
        integrated_invariants=all(r['invariant_failures']==0 for r in groups['integrated']),
        temperature=all(r['late_temperature']<=.12 for r in rows),
        integrated_closure=all(r['valid_fraction_late']>=.8 for r in groups['integrated']),
        isolated_association=all(r['largest_component']>=4 and r['lateral_contacts']>0 for r in groups['assembly']))
    return dict(screen_passed=all(conditions.values()),conditions=conditions,run_transfer=False,
        scope='First300-time dynamics, constructed integrated frontier and isolated-L association. No closed vesicle, late insertion, numerical convergence, renewal or homeostasis implied. Report then interpret; no long followup automatically.')


def collect(folder,require_complete=True,expected_tasks=6,decision_fn=decide):
    folder=Path(folder);manifest=validate(folder);s=status(folder);rows=[]
    if require_complete and (s['controller_active'] or s['counts']['complete']!=expected_tasks):raise ValueError('Require inactive complete competitive panel')
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    for task,state in zip(manifest['tasks'],s['tasks']):
        if state['phase']!='complete':continue
        p=folder/state['result'];r=read(p);m=r['metrics']
        if r['error'] or not r['completed'] or r['scenario']!=task['scenario'] or r['source_sha256']!=hashes:raise ValueError('CC1 provenance mismatch')
        sim,_=load(folder/state['checkpoint']);c=sim.chemistry;heads,_,links=c.lipids.layout();n=len(heads)
        graph={(a,b) for a,b,_,_ in links};parts=list(components(n,graph));sizes=Counter(len(q[0]) for q in parts)
        contours=[]
        for comp,order,cycle in parts:
            if cycle and len(order)==len(comp):
                points=c.pos[[heads[i] for i in order]]
                if polygon_simple(points):contours.append(dict(units=len(comp),area=float(area(points))))
        faces=[(a,x) for a,b,x,y in links]+[(b,y) for a,b,x,y in links]
        valid=len(faces)==len(set(faces)) and len(set(c.lipids.rungs.values()))==n and bool(np.isfinite(c.pos).all())
        duration=task['scenario']['duration']
        history=read(folder/state['motion_audit'])['history'];temp=[q['kinetic_temperature'] for q in history if q['time']>=.75*duration]
        variant=task['label'].split('_')[1];boundary=m.get('boundary',{}).get('history',[])
        g=m.get('genetics',{})
        rows.append(dict(label=task['label'],seed=task['scenario']['seed'],variant=variant,atoms=len(c.pos),
            final_ports_valid=bool(valid),invariant_failures=m.get('atom_port_invariant_failures') if variant=='integrated' else None,
            late_temperature=sum(temp)/len(temp),valid_fraction_late=weighted(boundary,'valid',.5*duration,duration) if boundary else None,
            L=n,L_new=m['lipids_formed'],lateral_contacts=len(links),largest_component=max(sizes,default=0),size_distribution=dict(sizes),
            graph_cycles=sum(bool(q[2]) for q in parts),simple_contours=contours,
            G_new=g.get('detached_copy_sets_ever'),F_new=g.get('translated_detached_ever'),
            contact_update_stats=m['contact_update_stats'],elapsed_seconds=r['elapsed_seconds'],result_sha256=digest(p)))
    report=dict(rows=rows,counts=s['counts'],controller_active=s['controller_active'],decision=decision_fn(rows) if len(rows)==expected_tasks else None)
    write(folder/'competitive_panel_review.json',report);return report
