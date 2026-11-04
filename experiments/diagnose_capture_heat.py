"""Selected L2 no-boost first-capture microscope; bounded2 simulated units."""
import json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
RUNTIME=ROOT/'research/campaign_recipes/L2_20261104T122737643199Z/runtime'
if '--archived' in sys.argv:sys.path.insert(0,str(RUNTIME))
from simulator.engine import Simulation
from simulator.campaign_io import read,write
from simulator.checkpoint import source_hashes
from experiments.diagnose_lipid_heat import energy


def elastic(c):
    h=c.host;pos=h.pos;spring=angle=0.
    for i,j,k,l in h.springs:
        spring+=.5*k*(float(np.linalg.norm(pos[int(i)]-pos[int(j)]))-l)**2
    for i,j,k,strength,target in h.angles:
        a=pos[int(i)]-pos[int(j)];b=pos[int(k)]-pos[int(j)]
        cosine=float(np.dot(a,b)/max(np.linalg.norm(a)*np.linalg.norm(b),1e-16))
        angle+=.5*strength*(cosine-target)**2
    return dict(springs=float(spring),angles=float(angle))


def main():
    recipe=ROOT/'research/campaign_recipes/L2_20261104T122737643199Z';m=read(recipe/'manifest.json')
    if source_hashes()!={k:v for k,v in m['source_sha256'].items() if k.startswith('simulator/')}:
        if '--archived' in sys.argv:raise ValueError('Archived L2 sources differ')
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'--archived'],cwd=RUNTIME,check=True);return
    cfg=next(t['scenario'] for t in m['tasks'] if t['label']=='L2_no_boost_s0')
    sim=Simulation(cfg);plain=Simulation(cfg);c=sim.chemistry;target=[];initial=[];original=c.capture.react
    def watched(world,dt,neighbors):
        if not initial:initial.append(elastic(c))
        if target:return original(world,dt,neighbors)
        old=c.capture.site_bound.copy();before=energy(c);p=c.pos.copy()
        original(world,dt,neighbors)
        sites=np.flatnonzero((old<0)&(c.capture.site_bound>=0))
        if len(sites):
            after=energy(c);ids={int(c.capture.site_bound[s]) for s in sites}
            for s in sites:ids.update(map(int,c.rungs[s]))
            target.append(dict(time=sim.time,before=before,after=after,delta={k:after[k]-v for k,v in before.items()},
                positions_unchanged=bool(np.array_equal(p,c.pos)),local_atom_ids=sorted(ids),
                local_positions=c.pos[sorted(ids)].tolist(),site_atom_pairs=[(int(s),int(c.capture.site_bound[s])) for s in sites]))
    c.capture.react=watched;steps=round(2./sim.dt);sim.advance(steps);plain.advance(steps)
    np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos)
    np.testing.assert_array_equal(sim.motion.velocities,plain.motion.velocities)
    if sim.rng.bit_generator.state!=plain.rng.bit_generator.state or c.export()!=plain.chemistry.export():raise ValueError('Microscope is not passive')
    if len(target)!=1:raise ValueError('First capture absent in frozen budget')
    result=dict(initial_F_elastic=initial[0],first_capture=target[0],total_capture_jump=sum(target[0]['delta'].values()),
        physical_replay_exact_through=2.,scope='Selected seed0 no_boost; first capture batch only, all64 atoms in energy, local positions bounded. No full heat balance.')
    out=ROOT/'outputs/diagnostics'/('L2_capture_heat_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));out.mkdir()
    write(out/'summary.json',result);print(json.dumps(result,indent=2))
    (ROOT/'outputs/diagnostics/L2_capture_heat_latest.txt').write_text(str(out.resolve()))


if __name__=='__main__':main()
