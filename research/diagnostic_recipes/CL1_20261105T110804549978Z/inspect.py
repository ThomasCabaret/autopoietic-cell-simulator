"""CL1 bounded six-bead microscope on the first CB1 exchange, frozen physics."""
import argparse,hashlib,json,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def prepare():
    from datetime import datetime,timezone
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=ROOT/'outputs/diagnostics'/('CL1_'+stamp);out.mkdir(parents=True)
    job=Path(read(ROOT/'research/BATCH_44_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0])
    manifest=read(folder/'manifest.json');task=next(t for t in manifest['tasks'] if t['label']=='CB1_active_s0')
    state=read(folder/'tasks'/task['id']/'state.json');result=folder/state['result']
    import numpy as np
    with np.load(result.parent/'checkpoint.npz',allow_pickle=False) as z:meta=json.loads(str(z['metadata']))
    event=meta['chemistry']['exchanges'][0];rungs=dict(meta['chemistry']['lipids']['rungs'])
    heads=sorted(set(event['removed'][:2]+event['formed'][:2]));ids=sorted(heads+[rungs[h] for h in heads])
    config=dict(campaign=str(folder),manifest_sha256=digest(folder/'manifest.json'),task=task['id'],
        result_sha256=digest(result),target_event=event,atom_ids=ids,heads=heads,start=event['time']-.5,
        end=event['time']+6.,max_frames=700,max_wall_seconds=1800)
    src=out/'inspect.py';shutil.copyfile(Path(__file__),src);config['diagnostic_source_sha256']=digest(src)
    write(out/'recipe.json',config);write(out/'status.json',dict(phase='ready',time=0.,target=config['end']))
    recipe=ROOT/'research/diagnostic_recipes'/('CL1_'+stamp);recipe.mkdir(parents=True)
    shutil.copyfile(src,recipe/'inspect.py');shutil.copyfile(out/'recipe.json',recipe/'recipe.json')
    write(ROOT/'research/BATCH_45_LOUPE.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),
        recipe_sha256=digest(recipe/'recipe.json'),source_sha256=digest(src)))
    return out


def run(out):
    cfg=read(out/'recipe.json');folder=Path(cfg['campaign']);manifest=read(folder/'manifest.json')
    if digest(folder/'manifest.json')!=cfg['manifest_sha256']:raise ValueError('Manifest changed')
    for p,h in manifest['source_sha256'].items():
        if digest(folder/'runtime'/p)!=h:raise ValueError('Frozen source changed')
    sys.path.insert(0,str(folder/'runtime'))
    import numpy as np
    from simulator.engine import Simulation
    from simulator.runner import make_observer
    from simulator import checkpoint
    from simulator.spatial import Neighborhood
    from simulator.docking import docking_force,bound_port_force,free_faces
    from simulator.membrane_bath import barrier_force
    import simulator.linked_lipids as module
    task=next(t for t in manifest['tasks'] if t['id']==cfg['task']);sim=Simulation(task['scenario'])
    obs=make_observer(sim.config,False);sim.listeners.append(obs);started=time.monotonic();last=started
    def advance_to(target):
        nonlocal last
        step=round(target/sim.dt)
        while sim.step_index<step:
            sim.advance(min(250,step-sim.step_index));now=time.monotonic()
            if now-last>=10:
                write(out/'status.json',dict(phase='replay',time=sim.time,target=cfg['end'],wall_seconds=now-started));last=now
            if now-started>cfg['max_wall_seconds']:
                checkpoint.save(out/'budget_checkpoint.npz',sim,obs)
                write(out/'status.json',dict(phase='budget_stopped',time=sim.time,target=cfg['end']));raise TimeoutError('CL1 fixed budget')
    advance_to(cfg['start']);checkpoint.save(out/'before_window.npz',sim,obs)
    plain,plain_obs=checkpoint.load(out/'before_window.npz',make_observer)
    c=sim.chemistry;events=[];frames=[];original=module.exchange_faces
    def port_energy(pos,links):
        n=len(pos)//2;partners=np.full((n,2),-1,dtype=np.int64)
        for i,j,a,b in links:partners[i,a]=j;partners[j,b]=i
        pairs=Neighborhood('brute',0.).pairs(pos[:n],1+4*c.config['dock_width'])
        return docking_force(pos,pairs,free_faces(n,links),1.,c.config['short_length'],c.config['dock_energy'],c.config['dock_width'],partners)[1]+bound_port_force(pos,np.asarray(links,dtype=np.int64).reshape(-1,4),1.,c.config['short_length'],c.config['dock_energy'],c.config['dock_width'])[1]
    def barrier_energy(edge):
        edges=np.asarray([edge],dtype=np.int64);ids=c.host.rungs[c.host.rungs[:,1]>=0].reshape(-1)
        pairs=np.array([[0,i] for i in range(len(ids))],dtype=np.int64).reshape(-1,2)
        return float(barrier_force(c.pos,edges,ids,pairs,c.config['bound_barrier_radius'],c.config['bound_barrier_stiffness'])[1])
    def watched(pos,links,config,rng,neighbors,interval):
        before=list(links);after,new=original(pos,links,config,rng,neighbors,interval)
        heads=sorted(c.lipids.rungs)
        for e in new:
            removed=[heads[e['removed'][0]],heads[e['removed'][1]],*e['removed'][2:]]
            formed=[heads[e['formed'][0]],heads[e['formed'][1]],*e['formed'][2:]]
            events.append(dict(time=sim.time,removed=removed,formed=formed,
                L_port_potential_delta=float(port_energy(pos,after)-port_energy(pos,before)),
                segment_barrier_delta=barrier_energy(formed[:2])-barrier_energy(removed[:2])))
        return after,new
    module.exchange_faces=watched
    def capture(time,c,events_):
        if cfg['start']-1e-8<=time<=cfg['end']+1e-8 and len(frames)<cfg['max_frames']:
            frames.append(dict(time=float(time),positions=c.pos[cfg['atom_ids']].tolist(),
                velocities=sim.motion.velocities[cfg['atom_ids']].tolist(),
                local_links=[list(e) for e in c.lipids.links if e[0] in cfg['heads'] or e[1] in cfg['heads']]))
    original_react=c.react
    def react(time,dt,neighbors):
        result=original_react(time,dt,neighbors);capture(time,c,result);return result
    c.react=react
    try:advance_to(cfg['end'])
    finally:module.exchange_faces=original
    plain.advance(sim.step_index-plain.step_index)
    np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos)
    np.testing.assert_array_equal(sim.motion.velocities,plain.motion.velocities)
    if sim.rng.bit_generator.state!=plain.rng.bit_generator.state or c.export()!=plain.chemistry.export() or obs.summary()!=plain_obs.summary():raise ValueError('Microscope changed state')
    old=read(folder/read(folder/'tasks'/task['id']/'state.json')['result'])['metrics'];current=json.loads(json.dumps(obs.summary()))
    for section,key in (('metrics','history'),('metrics','births'),('genetics','history'),('genetics','events')):
        a=old if section=='metrics' else old['genetics'];b=current if section=='metrics' else current['genetics']
        if [e for e in a[key] if e['time']<=sim.time+1e-9]!=b[key]:raise ValueError('CB1 observed prefix changed: '+key)
    write(out/'frames.json',dict(atom_ids=cfg['atom_ids'],frames=frames))
    report=dict(time=sim.time,events=events,frames=len(frames),atom_ids=cfg['atom_ids'],
        plain_control_exact=True,CB1_observed_prefix_exact=True,wall_seconds=time.monotonic()-started,
        scope='Selected first original-edge displacement, six beads and6.5-time window. '
            'Potential deltas at fixed positions, ports and actual PR segment barrier only; '
            'not a time-integrated heat budget or full-cell survival proof. No feedback.')
    write(out/'report.json',report);write(out/'status.json',dict(phase='complete',time=sim.time,target=cfg['end']));print(json.dumps(report))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--run',type=Path);args=parser.parse_args()
    if args.run:run(args.run)
    else:print(prepare())
