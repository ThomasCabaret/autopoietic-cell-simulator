"""RX1 bounded passive replay of historical RV1 protection/recycling failures."""
import argparse,copy,hashlib,json,os,shutil,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8');tmp.replace(p)


class Exposure:
    """Observe pre-loss states and reconstruct the actual intra-call rung gate.

    Journal labels never enter a predicate or consume randomness. Intensities
    are conditional rate*time sums, not independent Poisson event estimates.
    """
    def __init__(self,initial_polymer=()):
        self.polymer=set(map(int,initial_polymer));self.cursor=0;self.windows={}

    def export(self):return dict(polymer=sorted(self.polymer),cursor=self.cursor,windows=self.windows)

    @classmethod
    def restore(cls,state):
        obj=cls(state['polymer']);obj.cursor=state['cursor'];obj.windows=state['windows'];return obj

    def before(self,c):
        for e in c.turnover.events[self.cursor:]:
            if e['kind']=='backbone_form':self.polymer.update((int(e['a']),int(e['b'])))
        self.cursor=len(c.turnover.events)
        occupied=c.pairing>=0;cat=c.assembly.catalyst
        capture=np.zeros(c.n,dtype=bool) if cat is None else cat.site_bound>=0
        degree=np.zeros(c.n,dtype=np.int64)
        for a,b in c.edges:degree[a]+=1;degree[b]+=1
        return dict(active=(c.rungs[:,1]>=0).copy(),paired=occupied.copy(),capture=capture.copy(),
            degree=degree,edges=list(c.edges),families=c.families.copy())

    def after(self,c,t,dt,before):
        span=dt*5;events=c.turnover.events[self.cursor:];degree=before['degree'].copy()
        for e in events:
            if e['kind']=='backbone_break':degree[e['a']]-=1;degree[e['b']]-=1
        key=str(int((t+1e-9)//50)*50)
        window=self.windows.setdefault(key,dict(calls=0,time=0.,site_time={},rung_gate_time={},
            rung_intensity={},backbone_time={},backbone_intensity={},events={}))
        window['calls']+=1;window['time']+=span
        def add(section,label,amount):
            values=window[section];values[label]=values.get(label,0.)+float(amount)
        for s in np.flatnonzero(before['active']):
            family='G' if before['families'][s]==0 else 'F';origin='polymer_seen' if int(s) in self.polymer else 'other'
            label=f'{family}:{origin}:degree{min(int(before["degree"][s]),2)}:pair{int(before["paired"][s])}:capture{int(before["capture"][s])}'
            add('site_time',label,span)
            gate=('linked' if degree[s]>0 else 'paired' if before['paired'][s] else
                'captured' if before['capture'][s] else 'eligible')
            add('rung_gate_time',f'{family}:{origin}:{gate}',span)
            if gate=='eligible':add('rung_intensity',f'{family}:{origin}',c.turnover.settings['rung_'+family.lower()]*span)
        occupied=before['paired']|before['capture']
        for a,b in before['edges']:
            family='G' if before['families'][a]==0 else 'F';protected=bool(occupied[a] or occupied[b])
            label=f'{family}:'+('occupied' if protected else 'exposed')
            add('backbone_time',label,span)
            rate=c.turnover.settings['backbone_'+family.lower()]*(c.turnover.settings['protection'] if protected else 1.)
            add('backbone_intensity',label,rate*span)
        for e in events:
            origin='polymer_seen' if e.get('support',-1) in self.polymer else 'other'
            label=e['kind']+((':'+origin) if e['kind']=='rung_break' else '')
            add('events',label,1.)
        self.cursor=len(c.turnover.events)

    def summary(self):
        totals={k:{} for k in ('site_time','rung_gate_time','rung_intensity','backbone_time','backbone_intensity','events')}
        for w in self.windows.values():
            for section,values in totals.items():
                for k,v in w[section].items():values[k]=values.get(k,0.)+v
        return dict(totals=totals,windows=self.windows,
            scope='Pre-backbone state exposure; rung eligibility reconstructed after actual backbone breaks in the same call. '
                'polymer_seen is a passive journal label. Gate categories prioritized linked/paired/captured/eligible; '
                'site_time retains overlapping occupations. Conditional intensities, no independence or homeostasis claim.')


def prepare():
    from datetime import datetime,timezone
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=ROOT/'outputs/diagnostics'/('RX1_'+stamp);out.mkdir(parents=True)
    job=Path(read(ROOT/'research/BATCH_31_RECIPES.json')['job']);folder=Path(read(job/'job.json')['campaigns'][0])
    manifest=read(folder/'manifest.json');cases=[]
    for label in ('RV1_full_s0','RV1_protected_s0'):
        task=next(t for t in manifest['tasks'] if t['label']==label);state=read(folder/'tasks'/task['id']/'state.json')
        if state['status']!='complete':raise ValueError('Require completed historical reference')
        result=folder/state['result'];ck=folder/state['checkpoint']
        cases.append(dict(task=task['id'],label=label,result=str(result),result_sha256=digest(result),
            checkpoint=str(ck),checkpoint_sha256=digest(ck)))
    src=out/'turnover_probe.py';shutil.copyfile(Path(__file__),src)
    cfg=dict(campaign=str(folder),manifest_sha256=digest(folder/'manifest.json'),cases=cases,
        source_sha256=digest(src),max_wall_seconds=1800,checkpoint_simulated_interval=50.,after='Report then stop; no tuning or transfer')
    write(out/'recipe.json',cfg);write(out/'status.json',dict(phase='ready',case=0,time=0.,pid=None))
    recipe=ROOT/'research/diagnostic_recipes'/('RX1_'+stamp);recipe.mkdir(parents=True)
    shutil.copyfile(src,recipe/src.name);shutil.copyfile(out/'recipe.json',recipe/'recipe.json')
    write(ROOT/'research/BATCH_47_RX1.json',dict(output=str(out),recipe=recipe.relative_to(ROOT).as_posix(),
        recipe_sha256=digest(recipe/'recipe.json'),source_sha256=digest(src)))
    (ROOT/'outputs/diagnostics/RX1_latest.txt').write_text(str(out),encoding='utf-8');return out


def run(out):
    cfg=read(out/'recipe.json');folder=Path(cfg['campaign']);manifest=read(folder/'manifest.json')
    if digest(Path(__file__))!=cfg['source_sha256'] or digest(folder/'manifest.json')!=cfg['manifest_sha256']:raise ValueError('Recipe/source changed')
    for p,h in manifest['source_sha256'].items():
        if digest(folder/'runtime'/p)!=h:raise ValueError('Frozen source changed')
    sys.path.insert(0,str(folder/'runtime'))
    from simulator.engine import Simulation
    from simulator.runner import make_observer
    from simulator import checkpoint
    state=read(out/'status.json');started=time.monotonic();reports=[]
    for index,case in enumerate(cfg['cases']):
        dest=out/case['label'];dest.mkdir(exist_ok=True)
        if (dest/'report.json').exists():reports.append(read(dest/'report.json'));continue
        if digest(case['result'])!=case['result_sha256'] or digest(case['checkpoint'])!=case['checkpoint_sha256']:raise ValueError('Reference changed')
        task=next(t for t in manifest['tasks'] if t['id']==case['task'])
        saved=read(dest/'resume.json') if (dest/'resume.json').exists() else None
        if saved:
            sim,obs=checkpoint.load(dest/saved['checkpoint'],make_observer);audit=Exposure.restore(saved['audit'])
            if sim.step_index!=saved['step']:raise ValueError('Checkpoint/audit mismatch')
        else:
            sim=Simulation(task['scenario']);obs=make_observer(sim.config,False);obs.record_trajectory=False
            sim.listeners.append(obs);audit=Exposure(q for q in obs.polymer_atoms if q<sim.chemistry.n)
        original=sim.chemistry.turnover.react
        def observed(c,t,dt):
            before=audit.before(c);original(c,t,dt);audit.after(c,t,dt,before)
        sim.chemistry.turnover.react=observed
        def save(phase):
            name=f'checkpoint_{sim.step_index}.npz';checkpoint.save(dest/name,sim,obs)
            write(dest/'resume.json',dict(checkpoint=name,step=sim.step_index,audit=audit.export()))
            write(out/'status.json',dict(phase=phase,case=index,label=case['label'],time=sim.time,
                target=sim.config['duration'],pid=os.getpid(),updated=time.time(),wall_seconds=time.monotonic()-started))
        while not sim.done:
            sim.advance(min(round(cfg['checkpoint_simulated_interval']/sim.dt),sim.target_step-sim.step_index))
            stop=(out/'STOP').exists() or time.monotonic()-started>=cfg['max_wall_seconds']
            save('paused' if stop else 'running')
            if stop:return
        reference,reference_obs=checkpoint.load(case['checkpoint'],make_observer)
        np.testing.assert_array_equal(sim.chemistry.pos,reference.chemistry.pos)
        if sim.motion is not None:np.testing.assert_array_equal(sim.motion.velocities,reference.motion.velocities)
        if sim.rng.bit_generator.state!=reference.rng.bit_generator.state or sim.chemistry.export()!=reference.chemistry.export() or obs.summary()!=reference_obs.summary():raise ValueError('Replay changed historical state/RNG/observer')
        report=dict(label=case['label'],historical_state_rng_observer_exact=True,reference_result_sha256=case['result_sha256'],
            exposure=audit.summary(),metrics=obs.summary()['final'],wall_seconds=time.monotonic()-started)
        write(dest/'report.json',report);reports.append(report)
    write(out/'report.json',dict(cases=reports,scope='Two selected historical RV1 replays. No chemical changes, new cohort, causal intervention or transfer to EG1.'))
    write(out/'status.json',dict(phase='complete',case=len(reports),pid=os.getpid(),updated=time.time()))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path);a=p.parse_args()
    if a.run:
        try:run(a.run)
        except Exception:
            import traceback
            write(a.run/'status.json',dict(phase='failed',pid=os.getpid(),error=traceback.format_exc()));raise
    else:print(prepare())
