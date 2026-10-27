"""One physical bath for existing L and constructible P/R chemistries.

Species partition chemical reactivity, never biological aggregates. All forces
share one position array and scheduler. Only the local P--R bond state changes
cross-contact permeability; observer contours are not available to reactions.
"""
import numpy as np
from .copy import CopyChemistry
from .membrane_bath import MembraneBathChemistry, MembraneBathObserver, barrier_force, in_polygon
from .observations import CopyObserver, components, area

DEFAULTS=dict(temperature=.08,membrane={},genetics={},include_membrane=True,
              packet_offset=[27.5,0.],bound_contact=.55,bound_barrier_stiffness=80.)


class ScopedNeighbors:
    """Separate spatial caches for subsets of the shared physical positions."""
    def __init__(self,parent,prefix):self.parent,self.prefix=parent,prefix
    def pairs(self,points,radius,key='default'):
        return self.parent.pairs(points,radius,self.prefix+key)


def membrane_config(config):
    from .config import resolve
    raw=dict(config['membrane'],temperature=config['temperature'],retained_probes=0,permeable_probes=0)
    return resolve(dict(schema_version=1,model='membrane_bath',chemistry=raw))['chemistry']


def genetics_config(config):
    from .config import resolve
    raw=dict(config['genetics'],temperature=config['temperature'])
    return resolve(dict(schema_version=1,model='copy',chemistry=raw))['chemistry']


def shifted(array,offset,columns):
    result=array.copy()
    if len(result):result[:,:columns]+=offset
    return result


class CoupledBathChemistry:
    def __init__(self,config,rng):
        self.config,self.rng=config,rng
        self.membrane=MembraneBathChemistry(membrane_config(config),rng)
        self.genetics=CopyChemistry(genetics_config(config),rng)
        self.box=self.membrane.box.copy()
        # The native genetic box constructs a packet; it is not an inner wall.
        self.genetics.pos+=self.box/2-self.genetics.box/2+np.asarray(config['packet_offset'])
        if np.any(self.genetics.pos<0) or np.any(self.genetics.pos>self.box):
            raise ValueError('Genetic initial packet leaves the global box')
        self.genetics.box=self.box
        self.offset=len(self.membrane.pos) if config['include_membrane'] else 0
        self.pos=np.concatenate((self.membrane.pos[:self.offset],self.genetics.pos))
        self.mobility=np.concatenate((np.full(self.offset,.4),np.full(len(self.genetics.pos),.25)))[:,None]
        # 0=L,1=free P,2=free R,3=bound P,4=bound R: mechanical
        # classes only, not new elementary kinds or whole-molecule identities.
        self.contact=np.zeros((5,5))
        for i in range(1,5):
            for j in range(1,5):
                self.contact[i,j]=.70 if i%2 and j%2 else (.28 if i%2!=j%2 else 0.)
        self.contact[0,0]=.4
        self.contact[0,3:]=self.contact[3:,0]=config['bound_contact']
        self.springs=np.empty((0,4));self.angles=np.empty((0,5))
        self._views();self._mechanics()

    def _views(self):
        if self.offset:self.membrane.pos=self.pos[:self.offset]
        self.genetics.pos=self.pos[self.offset:]

    def bound_atoms(self):
        g=self.genetics
        ids=g.rungs[g.rungs[:,1]>=0].reshape(-1)
        bound=np.zeros(len(g.pos),dtype=bool);bound[ids]=True
        return bound

    def _mechanics(self):
        g=self.genetics;bound=self.bound_atoms()
        kinds=np.concatenate((np.ones(g.n,dtype=np.int64),np.full(g.n,2,dtype=np.int64)))
        kinds[bound]+=2
        self.kinds=np.concatenate((np.zeros(self.offset,dtype=np.int64),kinds))
        ms=self.membrane.springs if self.offset else np.empty((0,4))
        ma=self.membrane.angles if self.offset else np.empty((0,5))
        self.springs=np.concatenate((ms,shifted(g.springs,self.offset,2)))
        self.angles=np.concatenate((ma,shifted(g.angles,self.offset,3)))

    def react(self,time,dt,neighbors):
        self._views()
        if self.offset:self.membrane.react(time,dt,ScopedNeighbors(neighbors,'L:'))
        events=self.genetics.react(time,dt,ScopedNeighbors(neighbors,'PR:'))
        self._mechanics()
        return events

    def extra_forces(self,neighbors):
        self._views();force=np.zeros_like(self.pos)
        if self.offset:force[:self.offset]+=self.membrane.extra_forces(ScopedNeighbors(neighbors,'L:'))
        force[self.offset:]+=self.genetics.extra_forces(ScopedNeighbors(neighbors,'PR:'))
        ids=self.offset+np.flatnonzero(self.bound_atoms())
        if self.offset and len(ids) and self.membrane.edges[0] and self.config['bound_contact']>0:
            edges=np.array(sorted(self.membrane.edges[0]),dtype=np.int64)
            midpoint=(self.pos[edges[:,0]]+self.pos[edges[:,1]])/2
            half=.5*np.linalg.norm(self.pos[edges[:,1]]-self.pos[edges[:,0]],axis=1).max()
            points=np.concatenate((midpoint,self.pos[ids]));ne=len(edges)
            pairs=neighbors.pairs(points,half+self.config['bound_contact'],'PR:segment')
            pairs=pairs[(pairs[:,0]<ne)&(pairs[:,1]>=ne)].copy();pairs[:,1]-=ne
            force+=barrier_force(self.pos,edges,ids,pairs,self.config['bound_contact'],self.config['bound_barrier_stiffness'])[0]
        return force

    def observe(self,callback,time,events):
        self._views();callback(time,self,events)

    def export(self):
        return dict(membrane=self.membrane.export(),genetics=self.genetics.export())

    def restore(self,state):
        # Checkpoint.load has already restored the combined mechanical arrays.
        gs=self.springs[self.springs[:,0]>=self.offset].copy()
        ga=self.angles[self.angles[:,0]>=self.offset].copy()
        if len(gs):gs[:,:2]-=self.offset
        if len(ga):ga[:,:3]-=self.offset
        self._views();self.membrane.restore(state['membrane']);self.genetics.restore(state['genetics'])
        self.membrane._face_mechanics()
        self.genetics.springs,self.genetics.angles=gs,ga
        self._mechanics()

    def bonds(self):
        result=self.membrane.bonds() if self.offset else {}
        result={k:list(v) for k,v in result.items()}
        for key,pairs in self.genetics.bonds().items():
            result.setdefault(key,[]).extend([[a+self.offset,b+self.offset] for a,b in pairs])
        return result

    def colors(self):
        return (self.membrane.colors() if self.offset else [])+self.genetics.colors()


class CoupledBathObserver:
    """Nested observers are saved as plain state dictionaries for exact resume."""
    def __init__(self,config):
        self.config=config
        self.genetic_state=None;self.membrane_state=None
        self.times=[];self.frames=[];self.edges_frames=[];self.history=[]
        self.contact_samples=0;self.bound_contact_samples=0;self.free_contact_samples=0
        self.contact_atom_time={'free':0.,'bound':0.};self.first_contact=None
        self.last_inside={};self.last_bound={};self.crossings={'free':0,'bound':0,'state_changed':0}
        self.inside_counts={};self.valid_samples=0

    def __call__(self,time,c,events):
        g=CopyObserver(genetics_config(self.config));g.record_trajectory=False
        if self.genetic_state is not None:g.__dict__.update(self.genetic_state)
        c.genetics.observe(g,time,events);self.genetic_state=g.__dict__
        self.times.append(float(time))
        envelope=None
        if c.offset:
            m=MembraneBathObserver(membrane_config(self.config));m.record_trajectory=False
            if self.membrane_state is not None:m.__dict__.update(self.membrane_state)
            c.membrane.observe(m,time,[]);self.membrane_state=m.__dict__
            if m.history[-1]['envelope_valid']:
                choices=[]
                for comp,order,cycle in components(c.membrane.n,c.membrane.edges[0]):
                    if len(comp & set(range(m.ring)))<.8*m.ring or len(order)<3:continue
                    p=c.membrane.pos[order]
                    if not cycle and np.linalg.norm(p[-1]-p[0])>2.5:continue
                    from .membrane_bath import polygon_simple
                    if area(p)<.5*m.initial_area or not polygon_simple(p):continue
                    choices.append((area(p),p))
                if choices:envelope=max(choices,key=lambda x:x[0])[1]
            # Pure diagnostic distance to actual local membrane beads.
            from scipy.spatial import cKDTree
            distances=cKDTree(c.membrane.pos).query(c.genetics.pos)[0]
            bound=c.bound_atoms();near=distances<.8
            self.contact_samples+=int(near.sum())
            self.bound_contact_samples+=int(np.count_nonzero(near&bound))
            self.free_contact_samples+=int(np.count_nonzero(near&~bound))
            span=self.times[-1]-self.times[-2] if len(self.times)>1 else 0.
            self.contact_atom_time['free']+=span*int(np.count_nonzero(near&~bound))
            self.contact_atom_time['bound']+=span*int(np.count_nonzero(near&bound))
            if np.any(near) and self.first_contact is None:self.first_contact=float(time)
        if envelope is not None:
            self.valid_samples+=1;inside=in_polygon(c.genetics.pos,envelope);bound=c.bound_atoms()
            counts={name:int(np.count_nonzero(inside&mask)) for name,mask in [('free',~bound),('bound',bound)]}
            self.inside_counts=counts
            for atom,value in enumerate(inside):
                if atom in self.last_inside and self.last_inside[atom]!=bool(value):
                    label=('bound' if bound[atom] else 'free') if self.last_bound[atom]==bool(bound[atom]) else 'state_changed'
                    self.crossings[label]+=1
            self.last_inside={i:bool(x) for i,x in enumerate(inside)}
            self.last_bound={i:bool(x) for i,x in enumerate(bound)}
        else:
            # Do not bridge an interval with unclassifiable topology.
            self.last_inside={};self.last_bound={}
        self.history.append(dict(time=float(time),envelope_valid=envelope is not None,
                                 inside=dict(self.inside_counts) if envelope is not None else None))
        if getattr(self,'record_trajectory',True):self.frames.append(c.pos.copy())

    def summary(self):
        g=CopyObserver(genetics_config(self.config));g.__dict__.update(self.genetic_state)
        gm=g.summary()
        membrane=None
        if self.membrane_state is not None:
            m=MembraneBathObserver(membrane_config(self.config));m.__dict__.update(self.membrane_state)
            membrane=m.summary()
        return dict(genetics=gm,membrane=membrane,history=self.history,
                    valid_transport_fraction=self.valid_samples/max(len(self.times),1),
                    near_membrane_atom_samples=self.contact_samples,
                    near_membrane_free_atom_samples=self.free_contact_samples,
                    near_membrane_bound_atom_samples=self.bound_contact_samples,
                    near_membrane_atom_time=self.contact_atom_time,first_membrane_contact=self.first_contact,
                    sampled_crossings=self.crossings,final_inside_counts=self.inside_counts,
                    limitations='Sampled diagnostic envelope, no crossing inference across unknown samples; state may change between samples; crossings are not flux or proof of seal. No membrane synthesis or shared minimal alphabet demonstrated.')
