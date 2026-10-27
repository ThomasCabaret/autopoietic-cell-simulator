"""Read-only six-bead geometry at exact exchange events in frozen B0 laws."""
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=ROOT/'outputs/campaigns/campaign_20261026T165544113247Z'
sys.path.insert(0,str(PREVIOUS/'runtime'))
from simulator.engine import Simulation
from simulator.runner import make_observer,create_output,save_result
from simulator.docking import port_geometry,free_faces
import simulator.membrane_bath as bath


if __name__=='__main__':
    manifest=json.loads((PREVIOUS/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['source_sha256'].items():
        assert hashlib.sha256((PREVIOUS/'runtime'/name).read_bytes()).hexdigest()==digest
    cfg=manifest['tasks'][1]['scenario'];cfg=json.loads(json.dumps(cfg));cfg['duration']=800.
    cfg['name']='M1B0_exchange_geometry';cfg['branch']='M1G'
    sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
    out=create_output(sim.config,ROOT/'outputs/batch12/traces')
    source=Path(__file__).read_bytes();(out/'trace_exchange_geometry.py').write_bytes(source)
    original=bath.exchange_faces;events=[];current_time=[0.]
    react=sim.chemistry.react
    def clocked(time,dt,neighbors):
        current_time[0]=time;return react(time,dt,neighbors)
    sim.chemistry.react=clocked
    def checked(pos,links,config,rng,neighbors,interval):
        result,changes=original(pos,links,config,rng,neighbors,interval)
        if not changes:return result,changes
        n=len(pos)//2;head,tail,_,_=port_geometry(pos,n,1.,config['short_length']);current=list(links)
        for e in changes:
            removed=tuple(e['removed']);formed=tuple(e['formed']);common=set(removed[:2])&set(formed[:2])
            assert len(common)==1;i=next(iter(common));j=next(iter(set(removed[:2])-{i}));k=next(iter(set(formed[:2])-{i}))
            jface=removed[2+removed[:2].index(j)];kface=formed[2+formed[:2].index(k)]
            free=free_faces(n,current);other=1-kface
            q=float(np.sum((head[j,jface]-head[k,other])**2)+np.sum((tail[j,jface]-tail[k,other])**2))
            cutoff=16*config['dock_width']**2
            events.append(dict(time=float(current_time[0]),**e,shared=i,displaced=j,incoming=k,
                incoming_other_face_free=bool(free[k,other]),remaining_port_mismatch=q,
                existing_attraction_cutoff_squared=cutoff,shadow_gate=bool(free[k,other] and q<cutoff),
                motif_coordinates={str(x):[pos[x].tolist(),pos[n+x].tolist()] for x in (i,j,k)}))
            current.remove(removed);current.append(formed)
        assert sorted(current)==result
        return result,changes
    bath.exchange_faces=checked
    import time
    start=time.perf_counter()
    while not sim.done:sim.advance(1000)
    evidence=save_result(out,sim,obs,time.perf_counter()-start)
    state=json.loads((PREVIOUS/'tasks/task0001/state.json').read_text())
    reference=json.loads((PREVIOUS/state['result']).read_text())
    assert evidence['metrics']['history']==[h for h in reference['metrics']['history'] if h['time']<=800.]
    assert evidence['metrics']['exchange_events']==[e for e in reference['metrics']['exchange_events'] if e['time']<=800.]
    result=dict(duration=800.,driver_sha256=hashlib.sha256(source).hexdigest(),
        all_prefix_observations_equal=True,events=events)
    (out/'geometry_trace.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(folder=str(out),**result),ensure_ascii=False))
