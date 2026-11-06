"""External boundary source/sink for unbound precursors, no cell feedback.

Transport uses the shared mechanics. Source times/poses/velocities use a
separate RNG; losses and observations never affect the next source event.
Array indices may change; atom_ids never change or get reused. No bonds yet.
"""
import copy
import hashlib
import math
import struct
import numpy as np

DEFAULTS = dict(species=['P','R'], initial_counts=[0,0], influx_per_length=[.1,.1],
    source_seed=1701, injection_depth=.3, max_particles=10000, max_samples=256,
    temperature=.08, box=[8.,6.], motion='langevin', mass=1., damping=.1,
    dpd_cutoff=1., core_radius=0.)


def validate(cfg):
    names=cfg['species'];counts=cfg['initial_counts'];rates=cfg['influx_per_length']
    if (not isinstance(names,list) or not names or any(not isinstance(x,str) or not x for x in names)
        or len(set(names))!=len(names)):
        raise ValueError('Open bath requires unique species names')
    if not isinstance(counts,list) or len(counts)!=len(names) or any(type(n) is not int or n<0 for n in counts):
        raise ValueError('Invalid initial precursor counts')
    if not isinstance(rates,list) or len(rates)!=len(names) or any(type(r) not in (int,float) or not math.isfinite(r) or r<0 for r in rates):
        raise ValueError('Invalid boundary flux per species')
    if any(type(cfg[k]) is not int or cfg[k]<1 for k in ('max_particles','max_samples')) or sum(counts)>cfg['max_particles']:
        raise ValueError('Invalid open-bath capacity or sample budget')
    if type(cfg['source_seed']) is not int or cfg['source_seed']<0:raise ValueError('Invalid source seed')
    if cfg['motion']!='langevin' or any(type(cfg[k]) not in (int,float) or not math.isfinite(cfg[k]) or cfg[k]<=0 for k in ('mass','damping','injection_depth','dpd_cutoff')):
        raise ValueError('Open bath requires positive-mass/damping Langevin and injection depth')
    if cfg['injection_depth']>=min(cfg['box'])/2 or cfg['core_radius']<0:
        raise ValueError('Invalid injection geometry or precursor core')


class OpenBathChemistry:
    def __init__(self,config,rng):
        self.config=config;self.box=np.asarray(config['box'],dtype=float)
        self.wall_box=None  # Display/absorption box, never a reflecting wall.
        self.mobility=.25;self.source_rng=np.random.default_rng(config['source_seed'])
        self.initial=np.array(config['initial_counts'],dtype=np.int64)
        self.kinds=np.repeat(np.arange(len(self.initial),dtype=np.int64),self.initial)
        self.pos=rng.uniform([0.,0.],self.box,size=(len(self.kinds),2))
        self.atom_ids=np.arange(len(self.pos),dtype=np.int64)
        self.birth_times=np.zeros(len(self.pos));self.next_id=len(self.pos)
        self.springs=np.empty((0,4));self.angles=np.empty((0,5))
        self.contact=np.full((len(self.initial),len(self.initial)),config['core_radius'])
        self.rates=2*self.box.sum()*np.asarray(config['influx_per_length'])
        self.next_arrivals=np.array([self.source_rng.exponential(1/r) if r>0 else np.inf for r in self.rates])
        self.injected=np.zeros_like(self.initial);self.exported=np.zeros_like(self.initial)
        self.export_age_sum=np.zeros(len(self.initial));self.max_injection_lag=0.
        self.source_digest='00'*32;self.last_boundary_time=0.;self.population_change=None

    def react(self,time,dt,neighbors):
        if time<=self.last_boundary_time:return []
        keep=np.flatnonzero(np.all((self.pos>0)&(self.pos<self.box),axis=1))
        removed=np.flatnonzero(np.any((self.pos<=0)|(self.pos>=self.box),axis=1))
        new_pos=[];new_kinds=[];new_vel=[];digest=self.source_digest
        while True:
            kind=int(np.argmin(self.next_arrivals));scheduled=float(self.next_arrivals[kind])
            if scheduled>time:break
            if len(keep)+len(new_pos)>=self.config['max_particles']:
                raise RuntimeError('Open bath capacity exhausted; trial invalid, no source clipping')
            # Each side is selected proportionally to its physical length.
            side=int(self.source_rng.choice(4,p=np.array([self.box[1],self.box[1],self.box[0],self.box[0]])/(2*self.box.sum())))
            p=self.source_rng.uniform([0.,0.],self.box)
            p[side//2]=self.config['injection_depth'] if side%2==0 else self.box[side//2]-self.config['injection_depth']
            v=self.source_rng.normal(size=2)*np.sqrt(self.config['temperature']/self.config['mass'])
            new_pos.append(p);new_kinds.append(kind);new_vel.append(v)
            digest=hashlib.sha256(bytes.fromhex(digest)+struct.pack('<didddd',scheduled,kind,*p,*v)).hexdigest()
            self.max_injection_lag=max(self.max_injection_lag,time-scheduled)
            self.next_arrivals[kind]=scheduled+self.source_rng.exponential(1/self.rates[kind])
        if len(removed) or new_pos:
            old_count=len(self.pos);born=len(new_pos)
            self.exported+=np.bincount(self.kinds[removed],minlength=len(self.initial))
            self.export_age_sum+=np.bincount(self.kinds[removed],weights=time-self.birth_times[removed],minlength=len(self.initial))
            self.injected+=np.bincount(new_kinds,minlength=len(self.initial)) if born else 0
            self.pos=np.vstack((self.pos[keep],np.asarray(new_pos).reshape(-1,2)))
            self.kinds=np.concatenate((self.kinds[keep],np.asarray(new_kinds,dtype=np.int64)))
            self.atom_ids=np.concatenate((self.atom_ids[keep],np.arange(self.next_id,self.next_id+born,dtype=np.int64)))
            self.birth_times=np.concatenate((self.birth_times[keep],np.full(born,time)))
            self.next_id+=born
            self.population_change=(old_count,np.concatenate((keep,np.full(born,-1,dtype=np.int64))),np.asarray(new_vel).reshape(-1,2))
        self.source_digest=digest;self.last_boundary_time=float(time)
        return []

    def census(self,time):
        count=np.bincount(self.kinds,minlength=len(self.initial))
        balance=self.initial+self.injected-self.exported-count
        interior=np.all((self.pos>self.box*.25)&(self.pos<self.box*.75),axis=1)
        return dict(time=float(time),counts=count.tolist(),injected=self.injected.tolist(),exported=self.exported.tolist(),
            balance_error=balance.tolist(),inside_central_half=np.bincount(self.kinds[interior],minlength=len(self.initial)).tolist(),
            mean_export_age=[float(s/n) if n else None for s,n in zip(self.export_age_sum,self.exported)],
            oldest_censored_age=float(np.max(time-self.birth_times)) if len(self.pos) else 0.,
            outside_pending=int(np.count_nonzero(np.any((self.pos<=0)|(self.pos>=self.box),axis=1))))

    def extra_forces(self,neighbors):return np.zeros_like(self.pos)
    def observe(self,callback,time,events):callback(time,self,events)
    def bonds(self):return {}
    def colors(self):return [('#37b9ca','#e9a65c','#a987d6','#b8cd6d')[int(k)%4] for k in self.kinds]

    def export(self):
        return dict(kinds=self.kinds.tolist(),atom_ids=self.atom_ids.tolist(),birth_times=self.birth_times.tolist(),
            next_id=self.next_id,next_arrivals=[float(t) if np.isfinite(t) else None for t in self.next_arrivals],
            source_rng=copy.deepcopy(self.source_rng.bit_generator.state),source_digest=self.source_digest,
            injected=self.injected.tolist(),exported=self.exported.tolist(),export_age_sum=self.export_age_sum.tolist(),
            last_boundary_time=self.last_boundary_time,max_injection_lag=self.max_injection_lag)

    def restore(self,state):
        for key in ('kinds','atom_ids','injected','exported'):setattr(self,key,np.array(state[key],dtype=np.int64))
        for key in ('birth_times','export_age_sum'):setattr(self,key,np.array(state[key],dtype=float))
        self.next_arrivals=np.array([np.inf if t is None else t for t in state['next_arrivals']])
        for key in ('next_id','source_digest','last_boundary_time','max_injection_lag'):setattr(self,key,state[key])
        self.source_rng.bit_generator.state=state['source_rng'];self.population_change=None
        if len(self.pos)!=len(self.atom_ids) or len(set(self.atom_ids))!=len(self.pos):raise ValueError('Invalid open-bath IDs')


class OpenBathObserver:
    """Bounded passive samples; no variable-size trajectory or event archive."""
    def __init__(self,config):
        self.config=config;self.times=[];self.frames=[];self.history=[];self.observations=0
        self.max_balance_error=0;self.max_population=0

    def __call__(self,time,c,events):
        row=c.census(time);self.observations+=1
        self.max_balance_error=max(self.max_balance_error,max(map(abs,row['balance_error'])))
        self.max_population=max(self.max_population,sum(row['counts']))
        self.history.append(row);self.times.append(float(time))
        del self.history[:-self.config['max_samples']];del self.times[:-self.config['max_samples']]
        self.source_digest=c.source_digest;self.max_injection_lag=c.max_injection_lag

    def summary(self):
        return dict(final=self.history[-1],history=self.history,observations=self.observations,
            max_balance_error=self.max_balance_error,max_population=self.max_population,
            source_digest=self.source_digest,max_injection_lag=self.max_injection_lag,
            scope='Unbound precursor transport only; fixed external Poisson source at interior boundary offset, '
                'sampled absorption, independent source RNG, finite horizon. No G/F/L, cell, chemistry, homeostasis '
                'or variable-size trajectory recording. Current atoms and source/sink counters remain checkpointed.')
