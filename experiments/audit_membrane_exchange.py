"""Trace the positive archived exchange case without altering its laws or RNG."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
folder=next((ROOT/'research/engine_runs').glob('M1exchange_s2*'))
sys.path.insert(0,str(folder))
from simulator.engine import Simulation
from simulator.runner import make_observer
import simulator.membrane_bath as bath
from simulator.docking import port_geometry


original=bath.exchange_faces;trace=[]


def checked(pos,links,config,rng,neighbors,interval):
    before=pos.copy();result,events=original(pos,links,config,rng,neighbors,interval)
    np.testing.assert_array_equal(pos,before)
    if not events:return result,events
    assert len(links)==len(result)
    current=set(links);n=len(pos)//2
    head,tail,_,_=port_geometry(pos,n,1.,config['short_length'])
    for e in events:
        removed=tuple(e['removed']);formed=tuple(e['formed']);assert removed in current
        common=set(removed[:2])&set(formed[:2]);assert len(common)==1
        shared=next(iter(common));old=set(removed[:2])-{shared};new=set(formed[:2])-{shared}
        assert len(old)==len(new)==1 and not old&new
        current.remove(removed)
        occupied={(i,a) for i,j,a,b in current}|{(j,b) for i,j,a,b in current}
        i,k,a,b=formed;assert (i,a) not in occupied and (k,b) not in occupied
        q=float(np.sum((head[k,b]-head[i,a])**2)+np.sum((tail[k,b]-tail[i,a])**2))
        assert q<config['contact_exchange_capture']**2 and q==e['port_mismatch']
        assert max(abs(np.linalg.norm(pos[k]-pos[i])-1.),
                   abs(np.linalg.norm(pos[n+k]-pos[n+i])-config['short_length']))<=config['break_extension']
        current.add(formed);trace.append(dict(**e,atoms=sorted([*removed[:2],*new]+[n+x for x in set(removed[:2])|new])))
    assert current==set(result)
    return result,events


if __name__=='__main__':
    saved=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    for name,digest in saved['source_sha256'].items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==digest
    bath.exchange_faces=checked
    sim=Simulation(saved['scenario']);obs=make_observer(sim.config);sim.listeners.append(obs)
    sim.advance(sim.target_step)
    assert json.loads(json.dumps(obs.summary()))==saved['metrics']
    with np.load(folder/'trajectory.npz') as data:
        np.testing.assert_array_equal(data['positions'],np.array(obs.frames))
        np.testing.assert_array_equal(data['membrane_face_links'],np.array(obs.face_link_frames))
    assert len(trace)==saved['metrics']['contact_exchanges']==2
    out=ROOT/'outputs/batch9'/('exchange_trace_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    out.mkdir(parents=True,exist_ok=False)
    source=Path(__file__).read_bytes();(out/'audit_membrane_exchange.py').write_bytes(source)
    result=dict(recipe=folder.relative_to(ROOT).as_posix(),checked_events=trace,all_metrics_equal=True,
        positions_and_contacts_equal=True,auditor_sha256=hashlib.sha256(source).hexdigest())
    (out/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))
