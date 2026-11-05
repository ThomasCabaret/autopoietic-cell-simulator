"""Post-hoc stock/horizon audit of MX1, using existing events and checkpoints.

No simulation, fitting, observer feedback or new trajectory. Typed stocks are
reconstructed from conserved elementary IDs; windows are descriptive, not a
retroactive replacement of the frozen MX1 gate.
"""
import argparse,json,sys
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.campaign_io import read,write
from scripts.campaign import validate,status,digest


def material_inventory(scenario,assembly):
    cfg=scenario['chemistry'];g=cfg['genetics'];n=len(assembly['rungs'])
    families=[g['seed_family']]*len(g['sequence'])+[0]*g['free_units']+[1]*g['function_units']
    if len(families)!=n or 'bond_turnover' in g:raise ValueError('Require irreversible actual support inventory')
    types=['P_G' if f==0 else 'P_F' for f in families]+[f'R{b}' for b in assembly['atom_bits']]
    types+=['H']*cfg['food_units']+['T']*cfg['food_units']
    initial=set(assembly['initial_supports']);initial_atoms=initial|{n+s for s in initial}
    boundary=cfg.get('initial_boundary')
    if boundary is not None:
        start=len(types);count=boundary['units']
        types+=['H']*count+['T']*count;initial_atoms.update(range(start,start+2*count))
    return n,families,types,initial_atoms


def stock_at(scenario,assembly,lipid_births,time):
    n,families,types,occupied=material_inventory(scenario,assembly)
    made=[e for e in assembly['events'] if e['time']<=time]
    for e in made:occupied.update((e['support'],e['recognizer']))
    for e in lipid_births:
        if e['time']<=time:occupied.update((e['head'],e['tail']))
    out=Counter(types[i] for i in range(len(types)) if i not in occupied)
    return {k:int(out[k]) for k in ('P_G','P_F','R0','R1','H','T')}


def history_at(history,time):
    eligible=[r for r in history if r['time']<=time+1e-9]
    if not eligible:raise ValueError('Missing initial observation')
    return eligible[-1]


def weighted(history,key,start,end):
    total=0.
    for a,b in zip(history,history[1:]):
        span=max(0.,min(end,b['time'])-max(start,a['time']))
        total+=span*a[key]
    return total/(end-start)


def row(folder,task,state,manifest):
    p=folder/state['result'];r=read(p);cfg=task['scenario'];m=r['metrics'];g=m['genetics'];a=g['assembly_state']
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    if r['scenario']!=cfg or r['source_sha256']!=hashes or r['error'] or not r['completed']:raise ValueError('Evidence mismatch')
    checkpoint=p.parent/'checkpoint.npz'
    with np.load(checkpoint,allow_pickle=False) as data:
        meta=json.loads(str(data['metadata']));pos=data['positions'].copy()
    if meta['source_sha256']!=hashes or meta['step']!=round(cfg['duration']/cfg['engine']['dt']):raise ValueError('Incomplete/different checkpoint')
    n,families,types,initial=material_inventory(cfg,a);horizon=cfg['duration'];area=float(np.prod(cfg['chemistry']['box']))
    expected={s:n+s for s in a['initial_supports']}
    for e in a['events']:
        if e['support'] in expected:raise ValueError('Repeated irreversible support birth')
        expected[e['support']]=e['recognizer']
    if expected!={i:int(v[1]) for i,v in enumerate(a['rungs']) if v[1]>=0}:raise ValueError('Reconstructed axial identity mismatch')
    counts={0.:dict(PR=0,L=0,G=0,F=0)};windows=[]
    last_counts=counts[0.]
    for time in [horizon*q/4 for q in range(5)]:
        hist=history_at(g['history'],time)
        current=dict(PR=sum(e['time']<=time for e in a['events']),L=sum(e['time']<=time for e in m['births']),
            G=hist['detached_ever'],F=hist['translated_detached_ever'])
        stocks=stock_at(cfg,a,m['births'],time)
        windows.append(dict(time=time,unassembled=stocks,concentrations_2D={k:v/area for k,v in stocks.items()},
            cumulative=current,increment={k:current[k]-last_counts[k] for k in current}))
        last_counts=current
    host=meta['chemistry']['host'];cap=meta['chemistry']['capture'];captured=Counter(types[q] for q in cap['site_bound'] if q>=0)
    examples=[]
    for i,j in host['edges']:
        x,y=cap['site_bound'][i],cap['site_bound'][j]
        if x<0 or y<0:continue
        kinds={types[x],types[y]}
        valid=(kinds=={'H','T'} or (any(k in kinds for k in ('P_G','P_F')) and any(k.startswith('R') for k in kinds)))
        examples.append(dict(sites=[i,j],atoms=[x,y],types=[types[x],types[y]],compatible=valid,
            distance=float(np.linalg.norm(pos[x]-pos[y])),within_formation_radius=bool(np.linalg.norm(pos[x]-pos[y])<=cfg['chemistry']['rung_capture_radius'])))
    degree=Counter(q for edge in host['edges'] for q in edge);paired=host['pairing'];free_composite=Counter()
    for s,recognizer in expected.items():
        if not degree[s] and paired[s]<0:free_composite[f'{"G" if families[s]==0 else "F"}{a["atom_bits"][recognizer-n]}']+=1
    gamma=cfg['mechanics']['damping'];mass=cfg['mechanics']['mass'];temperature=cfg['chemistry']['temperature']
    D=temperature/(mass*gamma)
    return dict(label=task['label'],seed=cfg['seed'],area=area,atoms=len(pos),windows=windows,
        captured_final=dict(captured),unpaired_unlinked_composites_final=dict(free_composite),final_double_motifs=examples,
        time_weighted_occupancy={key:weighted(m['history'],key,0.,horizon) for key in
            ('genetic_ligands','lipid_ligands','wrong_double_edges','double_occupied_edges')},
        last_PR=max((e['time'] for e in a['events']),default=None),last_L=max((e['time'] for e in m['births']),default=None),
        ideal_free_particle=dict(velocity_relaxation=1/gamma,D_asymptotic=D,
            box_slowest_density_mode=max(cfg['chemistry']['box'])**2/(np.pi**2*D) if D else None,
            caution='Ideal isolated-particle asymptotic estimate from this integrator. Not a measured mixing/contact time in a reactive aggregate bath.'),
        external_cycles=horizon/cfg['chemistry']['genetics']['period'],
        result_sha256=digest(p),checkpoint_sha256=digest(checkpoint),
        caveat='Unassembled stocks include temporarily captured atoms; they are not all immediately available. '
            'Final geometry is one snapshot. Occupancy left-held between irregular samples, not exact reaction exposure. '
            'Windows selected for diagnosis after MX1, no steady-state or asymptotic-failure inference.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--campaign',type=Path);args=p.parse_args()
    if args.campaign:folder=args.campaign
    else:folder=Path(read(Path(read(ROOT/'research/BATCH_41_RECIPES.json')['job'])/'job.json')['campaigns'][0])
    manifest=validate(folder);snap=status(folder)
    if snap['controller_active'] or snap['counts']['complete']!=len(manifest['tasks']):raise ValueError('Require complete inactive cohort')
    rows=[row(folder,t,s,manifest) for t,s in zip(manifest['tasks'],snap['tasks'])]
    dest=ROOT/'outputs/diagnostics'/('MX1_calibration_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));dest.mkdir(parents=True)
    write(dest/'report.json',dict(manifest_sha256=digest(folder/'manifest.json'),rows=rows))
    (ROOT/'outputs/diagnostics/latest_mixed_calibration.txt').write_text(str(dest.resolve()))
    for r in rows:
        if '_mixed_' in r['label'] or '_uncaptured_' in r['label']:
            print(json.dumps(dict(label=r['label'],remaining=r['windows'][-1]['unassembled'],last_quarter=r['windows'][-1]['increment'],
                occupancy=r['time_weighted_occupancy'],last_PR=r['last_PR'],last_L=r['last_L']),ensure_ascii=True))
    print(dest)


if __name__=='__main__':main()
