"""One bounded passive microscope around a selected persistent membrane opening."""
import argparse
from collections import Counter,deque
from datetime import datetime,timezone
import hashlib,json,math,shutil,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


class MembraneLoupe:
    def __init__(self,sim,window=(40.5,41.5),before=1.,after=5.,interval=.01,max_units=24):
        self.sim=sim;self.window=window;self.before=before;self.after=after;self.interval=interval;self.max_units=max_units
        self.buffer=deque(maxlen=math.ceil(before/interval)+2);self.frames=[];self.events=[]
        self.counts=Counter();self.trigger=None;self.ids=None;self.contact=None

    def __enter__(self):
        import simulator.membrane_bath as module
        self.module=module;self.original=module.update_faces
        def watched(pos,links,cfg,rng,neighbors,interval):
            result,broken=self.original(pos,links,cfg,rng,neighbors,interval)
            lost=sorted(set(links)-set(result));self.counts['reported_broken']+=broken
            n=len(pos)//2;t=self.sim.time
            for link in lost:
                i,j,a,b=link
                stretch=max(abs(float(np.linalg.norm(pos[j]-pos[i]))-1.),abs(float(np.linalg.norm(pos[n+j]-pos[n+i]))-cfg['short_length']))
                cause='extension' if stretch>cfg['break_extension'] else 'random_off'
                self.counts['net_'+cause]+=1
                if self.trigger is None and self.window[0]<=t<=self.window[1]:
                    self.trigger=float(t);self.contact=link
                    d=np.linalg.norm(pos[:n]-(pos[i]+pos[j])/2,axis=1)
                    nearby=[int(q) for q in np.argsort(d) if d[q]<=3.]
                    self.ids=np.array(list(dict.fromkeys([i,j]+nearby))[:self.max_units],dtype=int)
                    for row in self.buffer:
                        if row[0]>=t-self.before:self.frames.append(self.project(*row))
                    self.buffer.clear()
                if self.window[0]-.5<=t<=self.window[1]+1.5 and len(self.events)<64:
                    self.events.append(dict(time=float(t),removed=list(map(int,link)),cause=cause,extension=stretch,
                        threshold=cfg['break_extension'],coordinates=pos[[i,j,n+i,n+j]].tolist()))
            return result,broken
        module.update_faces=watched;return self

    def __exit__(self,*args):self.module.update_faces=self.original

    def project(self,t,pos,vel,partners):
        c=self.sim.chemistry;m=c.membrane;n=m.n
        indices=np.r_[self.ids,n+self.ids];i,j,_,_=self.contact
        return dict(time=float(t),positions=pos[indices].tolist(),velocities=vel[indices].tolist(),
            port_partners=partners[self.ids].tolist(),
            head_gap=float(np.linalg.norm(pos[j]-pos[i])),tail_gap=float(np.linalg.norm(pos[n+j]-pos[n+i])),
            membrane_temperature=float(np.mean(vel**2)))

    def tick(self):
        c=self.sim.chemistry;m=c.membrane;n=m.n
        if self.trigger is not None and self.sim.time>self.trigger+self.after:return
        row=(self.sim.time,c.pos[:2*n].copy(),self.sim.motion.velocities[:2*n].copy(),m.face_partners.copy())
        if self.trigger is None:self.buffer.append(row)
        else:self.frames.append(self.project(*row))

    def summary(self):
        return dict(trigger=self.trigger,units=None if self.ids is None else self.ids.tolist(),contact=self.contact,
            counts=dict(self.counts),events=self.events,frames=self.frames,
            limitations='Selected net loss near the known opening. A break and reformation within one update may be absent from net counts; exchanged partners are a separate mechanism. Only the bounded local capture is retained, no feedback or RNG draws. No claim of representative event frequency.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--campaign',type=Path,default=ROOT/'outputs/demo_motion_campaigns/campaign_20261030T065759494210Z');a=p.parse_args()
    sys.path.insert(0,str(a.campaign/'runtime'))
    from campaign import validate,status
    from simulator.engine import Simulation
    from simulator.runner import make_observer,create_output,save_result
    manifest=validate(a.campaign);task=next(t for t in manifest['tasks'] if t['label']=='LT2_integrated_s0_langevin')
    cfg=json.loads(json.dumps(task['scenario']));cfg.update(name='MD1_selected_loupe',branch='MD1',duration=80.)
    sim=Simulation(cfg);obs=make_observer(sim.config,False);sim.listeners.append(obs)
    out=create_output(sim.config,ROOT/'outputs/membrane_loupes');started=time.perf_counter()
    with MembraneLoupe(sim) as probe:
        while not sim.done:sim.advance(5);probe.tick()
    evidence=save_result(out,sim,obs,time.perf_counter()-started)
    state=next(s for s in status(a.campaign)['tasks'] if s['id']==task['id'])
    old=json.loads((a.campaign/state['result']).read_text())
    for path in (('membrane','history'),('genetics','history'),('genetics','events')):
        value=evidence['metrics'];reference=old['metrics']
        for key in path:value=value[key];reference=reference[key]
        assert value==[r for r in reference if r['time']<=80],path
    report=dict(**probe.summary(),prefix_verified=True,source_result_sha256=hashlib.sha256((a.campaign/state['result']).read_bytes()).hexdigest(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'loupe.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');shutil.copyfile(__file__,out/'driver.py')
    print(json.dumps(dict(folder=str(out),trigger=probe.trigger,counts=dict(probe.counts),frames=len(probe.frames),prefix_verified=True)))


if __name__=='__main__':main()
