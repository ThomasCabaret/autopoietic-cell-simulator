"""EL1 selected EN1 replay: passive fixed-position L-contact energy ledger."""
import argparse,hashlib,json,os,shutil,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8');tmp.replace(p)


def potential(c,pos,links,heads):
    from simulator.docking import free_faces,docking_force,bound_port_force
    from simulator.membrane_bath import barrier_force
    from simulator.spatial import Neighborhood
    n=len(heads);cfg=c.config;neighbors=Neighborhood('brute',0.)
    partners=np.full((n,2),-1,dtype=np.int64)
    for i,j,a,b in links:partners[i,a]=j;partners[j,b]=i
    pairs=neighbors.pairs(pos[:n],1.+4*cfg['dock_width'],'EL1_ports')
    ports=docking_force(pos,pairs,free_faces(n,links),1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'],partners)[1]
    ports+=bound_port_force(pos,np.asarray(links,dtype=np.int64).reshape(-1,4),1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width'])[1]
    ids=c.host.rungs[c.host.rungs[:,1]>=0].reshape(-1);barrier=0.
    if len(ids) and links and cfg['bound_barrier_radius']>0:
        edges=np.asarray([(heads[i],heads[j]) for i,j,_,_ in links],dtype=np.int64)
        # Observation only; small selected bath, all segment/atom pairs with
        # the exact finite-range barrier kernel. No simulator cache is touched.
        pairs=np.asarray([(a,b) for a in range(len(edges)) for b in range(len(ids))],dtype=np.int64).reshape(-1,2)
        barrier=barrier_force(c.pos,edges,ids,pairs,cfg['bound_barrier_radius'],cfg['bound_barrier_stiffness'])[1]
    return float(ports),float(barrier)


class Ledger:
    def __init__(self):self.events=[];self.totals={};self.largest=None;self.kinetics=[];self.dropped=0

    def change(self,c,t,pos,before,after,phase,reported=None):
        removed=sorted(set(map(tuple,before))-set(map(tuple,after)));formed=sorted(set(map(tuple,after))-set(map(tuple,before)))
        if not removed and not formed:return
        heads,ids,_=c.lipids.layout();a,b=potential(c,pos,before,heads),potential(c,pos,after,heads)
        delta=[b[i]-a[i] for i in range(2)];total=sum(delta)
        row=dict(time=float(t),phase=phase,ports=delta[0],barrier=delta[1],delta_U=total,
            removed=[[heads[i],heads[j],x,y] for i,j,x,y in removed],formed=[[heads[i],heads[j],x,y] for i,j,x,y in formed])
        if reported is not None:row['reported_delta_error']=total-reported
        stats=self.totals.setdefault(phase,dict(changes=0,positive=0.,negative=0.,ports=0.,barrier=0.,max_reported_delta_error=0.))
        stats['changes']+=1;stats['positive']+=max(total,0.);stats['negative']+=min(total,0.);stats['ports']+=delta[0];stats['barrier']+=delta[1]
        if reported is not None:stats['max_reported_delta_error']=max(stats['max_reported_delta_error'],abs(total-reported))
        if len(self.events)<2000:self.events.append(row)
        else:self.dropped+=1
        if self.largest is None or total>self.largest['delta_U']:
            units=sorted({q for edge in removed+formed for q in edge[:2]});atoms=sorted([heads[q] for q in units]+[c.lipids.rungs[heads[q]] for q in units])
            self.largest=dict(row,atom_ids=atoms,positions=c.pos[atoms].tolist())

    def sample(self,sim):
        c=sim.chemistry;groups={'PR':np.arange(c.prefix),
            'food_HT':np.arange(c.prefix,c.prefix+2*c.config['food_units']),
            'prepared_L':np.arange(c.prefix+2*c.config['food_units'],len(c.pos))}
        row=dict(time=sim.time)
        mass=sim.config.get('mechanics',{}).get('mass',1.)
        for key,ids in groups.items():row[key]=float(.5*mass*np.sum(sim.motion.velocities[ids]**2)/len(ids))
        self.kinetics.append(row)


def prepare():
    from datetime import datetime,timezone
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=ROOT/'outputs/diagnostics'/('EL1_'+stamp);out.mkdir(parents=True)
    job=Path(read(ROOT/'research/BATCH_47_EN1_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0])
    manifest=read(folder/'manifest.json');task=next(t for t in manifest['tasks'] if t['scenario']['seed']==2)
    state=read(folder/'tasks'/task['id']/'state.json');result=folder/state['result']
    src=out/'contact_heat_probe.py';shutil.copyfile(Path(__file__),src)
    cfg=dict(campaign=str(folder),manifest_sha256=digest(folder/'manifest.json'),task=task['id'],result_sha256=digest(result),
        source_sha256=digest(src),start=2100.,end=2200.,max_wall_seconds=2700,
        scope='Selected late heating window; fixed-position port and PR segment changes only, not total-world energy.')
    write(out/'recipe.json',cfg);write(out/'status.json',dict(phase='ready',pid=None,time=0.,target=2200.))
    recipe=ROOT/'research/diagnostic_recipes'/('EL1_'+stamp);recipe.mkdir(parents=True)
    shutil.copyfile(src,recipe/src.name);shutil.copyfile(out/'recipe.json',recipe/'recipe.json')
    write(ROOT/'research/BATCH_48_EL1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),recipe_sha256=digest(recipe/'recipe.json'),source_sha256=digest(src)))
    (ROOT/'outputs/diagnostics/EL1_latest.txt').write_text(str(out),encoding='utf-8');return out


def run(out):
    cfg=read(out/'recipe.json');folder=Path(cfg['campaign']);manifest=read(folder/'manifest.json');started=time.monotonic()
    if digest(Path(__file__))!=cfg['source_sha256'] or digest(folder/'manifest.json')!=cfg['manifest_sha256']:raise ValueError('Source/manifest changed')
    for p,h in manifest['source_sha256'].items():
        if digest(folder/'runtime'/p)!=h:raise ValueError('Frozen source changed')
    write(out/'status.json',dict(phase='initializing',pid=os.getpid(),time=0.,target=cfg['end']))
    sys.path.insert(0,str(folder/'runtime'))
    from simulator.engine import Simulation
    from simulator.runner import make_observer
    from simulator import checkpoint
    import simulator.linked_lipids as module
    task=next(t for t in manifest['tasks'] if t['id']==cfg['task']);state=read(folder/'tasks'/task['id']/'state.json')
    result=folder/state['result']
    if digest(result)!=cfg['result_sha256']:raise ValueError('Historical result changed')
    saved=read(out/'resume.json') if (out/'resume.json').exists() else None
    if saved:
        sim,obs=checkpoint.load(out/saved['checkpoint'],make_observer);ledger=Ledger();ledger.__dict__.update(saved['ledger'])
        if sim.step_index!=saved['step']:raise ValueError('Checkpoint mismatch')
    else:
        sim=Simulation(task['scenario']);obs=make_observer(sim.config,False);obs.record_trajectory=False;sim.listeners.append(obs);ledger=Ledger()
    def save(phase):
        name=f'checkpoint_{sim.step_index}.npz';checkpoint.save(out/name,sim,obs)
        write(out/'resume.json',dict(checkpoint=name,step=sim.step_index,ledger=ledger.__dict__))
        write(out/'status.json',dict(phase=phase,time=sim.time,target=cfg['end'],pid=os.getpid(),updated=time.time()))
    def advance_to(target,chunk):
        last=time.monotonic()
        while sim.time<target-1e-9:
            sim.advance(min(round(chunk/sim.dt),round((target-sim.time)/sim.dt)))
            if sim.time>cfg['start']:ledger.sample(sim)
            stop=(out/'STOP').exists() or time.monotonic()-started>=cfg['max_wall_seconds']
            if stop or time.monotonic()-last>30:save('paused' if stop else 'running');last=time.monotonic()
            if stop:return False
        return True
    if sim.time<cfg['start']:
        if not advance_to(cfg['start'],25.):return
        checkpoint.save(out/'plain_start.npz',sim,obs);save('running')
    elif not (out/'plain_start.npz').exists():checkpoint.save(out/'plain_start.npz',sim,obs)
    old_update,old_exchange=module.update_faces,module.exchange_faces
    def update(pos,links,*args,**kwargs):
        after,broken=old_update(pos,links,*args,**kwargs);ledger.change(sim.chemistry,sim.time,pos,links,after,'face_update');return after,broken
    def exchange(pos,links,*args,**kwargs):
        after,events=old_exchange(pos,links,*args,**kwargs)
        ledger.change(sim.chemistry,sim.time,pos,links,after,'exchange',sum(e.get('delta_U',0.) for e in events));return after,events
    module.update_faces,module.exchange_faces=update,exchange
    try:
        if not advance_to(cfg['end'],.1):return
    finally:module.update_faces,module.exchange_faces=old_update,old_exchange
    save('checking')
    plain,plain_obs=checkpoint.load(out/'plain_start.npz',make_observer);plain.advance(sim.step_index-plain.step_index)
    np.testing.assert_array_equal(sim.chemistry.pos,plain.chemistry.pos);np.testing.assert_array_equal(sim.motion.velocities,plain.motion.velocities)
    if sim.rng.bit_generator.state!=plain.rng.bit_generator.state or sim.chemistry.export()!=plain.chemistry.export() or obs.summary()!=plain_obs.summary():raise ValueError('Probe changed trajectory')
    old=read(result)['metrics'];current=json.loads(json.dumps(obs.summary()))
    for section,key in (('metrics','history'),('metrics','births'),('genetics','history'),('genetics','events'),('boundary','history')):
        a=old if section=='metrics' else old[section];b=current if section=='metrics' else current[section]
        if [e for e in a[key] if e['time']<=sim.time+1e-9]!=b[key]:raise ValueError('Historical observed prefix changed')
    write(out/'ledger.json',ledger.__dict__)
    write(out/'report.json',dict(plain_state_rng_observer_exact=True,historical_observed_prefix_exact=True,
        start=cfg['start'],end=cfg['end'],totals=ledger.totals,largest=ledger.largest,events=len(ledger.events),
        dropped=ledger.dropped,kinetic_samples=len(ledger.kinetics),scope=cfg['scope']))
    write(out/'status.json',dict(phase='complete',time=sim.time,target=cfg['end'],pid=os.getpid(),updated=time.time()))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path);a=p.parse_args()
    if a.run:
        try:run(a.run)
        except Exception:
            import traceback
            write(a.run/'status.json',dict(phase='failed',pid=os.getpid(),error=traceback.format_exc()));raise
    else:print(prepare())
