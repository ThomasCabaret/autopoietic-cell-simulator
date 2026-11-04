"""One motivated passive microscope: energy jump at the first L1 H--T birth."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation
from simulator.precursors import precursor_force
from simulator.spatial import Neighborhood
from simulator.checkpoint import source_hashes
from simulator.campaign_io import read,write
from scripts.campaign import validate


def energy(c):
    pos=c.pos;kind=c.kinds.copy()
    for h,t in c.lipids.rungs.items():kind[[h,t]]=3
    i,j=np.triu_indices(len(pos),1);distance=np.linalg.norm(pos[j]-pos[i],axis=1)
    core=float(40*np.sum(np.maximum(c.contact[kind[i],kind[j]]-distance,0.)**2))
    axial=sum(90*(float(np.linalg.norm(pos[h]-pos[t]))-.65)**2 for h,t in c.lipids.rungs.items())
    capture=sum(17.5*float(np.sum((pos[c.rungs[s,1]]-pos[a])**2)) for s,a in enumerate(c.capture.site_bound) if a>=0)
    cap=c.capture;cfg=c.config;pairs=Neighborhood('brute',0.).pairs(pos,3*cfg['food_ligand_width'])
    attractive=precursor_force(pos,pairs,cap.owners,cap.categories,c.bits,c.pairing,
        cap.site_bound,cap.atom_bound,cap.activity,cfg['food_ligand_energy'],cfg['food_ligand_width'])[1]
    ports=c.lipids.forces(pos,cfg,Neighborhood('brute',0.))[1]
    return dict(core=core,HT_axial=axial,capture_springs=capture,free_capture_potential=float(attractive),ports=ports)


def main():
    folder=Path((ROOT/'outputs/lipid_pilots/latest.txt').read_text().strip());manifest=validate(folder)
    hashes={k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
    if hashes!=source_hashes():raise ValueError('Use exact pilot sources')
    cfg=manifest['tasks'][0]['scenario'];sim=Simulation(cfg);plain=Simulation(cfg);c=sim.chemistry;capture=[]
    original=c.form_lipids
    def watched(time,interval,neighbors):
        if capture:return original(time,interval,neighbors)
        before=energy(c);count=len(c.births);p=c.pos.copy()
        original(time,interval,neighbors)
        if len(c.births)>count:
            after=energy(c);events=c.births[count:]
            ids=set(q for e in events for q in (e['head'],e['tail']))
            for e in events:
                for s in e['sites']:
                    if s>=0:ids.update(map(int,c.rungs[s]))
            capture.append(dict(time=float(time),events=events,before=before,after=after,
                delta={k:after[k]-v for k,v in before.items()},positions_unchanged=bool(np.array_equal(p,c.pos)),
                local_atom_ids=sorted(ids),local_positions=c.pos[sorted(ids)].tolist()))
    c.form_lipids=watched
    # Fixed first-unit replay budget; one transition, at most six recorded beads
    # in the observed pilot. Energy includes all64 atoms to retain outside context.
    steps=round(1./sim.dt);sim.advance(steps);plain.advance(steps)
    np.testing.assert_array_equal(c.pos,plain.chemistry.pos)
    np.testing.assert_array_equal(sim.motion.velocities,plain.motion.velocities)
    if sim.rng.bit_generator.state!=plain.rng.bit_generator.state or c.export()!=plain.chemistry.export():
        raise ValueError('Microscope changed dynamics')
    if len(capture)!=1:raise ValueError('First-birth target absent within fixed budget')
    record=capture[0];record['total_potential_jump']=sum(record['delta'].values())
    record['scope']=('Single selected first birth, six local atoms; all64 atoms included in energies. '
        'No F-internal or wall-energy change at identical positions. Not a trajectory-integrated heat balance. '
        'Replay and uninstrumented control physically exact through1.0; no feedback.')
    write(folder/'heat_microscope.json',record)
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
