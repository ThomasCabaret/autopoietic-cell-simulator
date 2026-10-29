"""Copied render data and passive topology events. No toolkit, physics or RNG ownership."""
from dataclasses import dataclass
from collections import deque
import numpy as np


@dataclass
class Frame:
    positions: np.ndarray
    species: np.ndarray
    labels: tuple
    palette: np.ndarray
    bonds: dict
    time: float
    step: int
    done: bool
    box: object=None
    revision: int=0
    bond_positions: object=None


@dataclass(frozen=True)
class Transition:
    kind: str
    group: str
    ids: tuple
    points: tuple
    time: float


def topology(chemistry):
    return {name:np.asarray(sorted({tuple(sorted(map(int,p))) for p in pairs}),dtype=np.int64).reshape(-1,2)
        for name,pairs in chemistry.bonds().items()}


def as_sets(bonds):return {name:{tuple(p) for p in pairs} for name,pairs in bonds.items()}


def bond_coordinates(c,group,pairs):
    points=c.pos[pairs].copy()
    if group=='pairing' and getattr(c,'config',{}).get('dual_faces',False):
        virtual=np.all(pairs<c.n,axis=1)
        points[virtual]=2*c.pos[pairs[virtual]]-c.pos[c.n+pairs[virtual]]
    return points


def differences(before,after,positions,time,project=None):
    result=[]
    for name in sorted(before.keys()|after.keys()):
        for kind,pairs in (('bond_created',after.get(name,set())-before.get(name,set())),
                           ('bond_broken',before.get(name,set())-after.get(name,set()))):
            for a,b in sorted(pairs):
                points=project(name,a,b) if project else (positions[a],positions[b])
                result.append(Transition(kind,name,(int(a),int(b)),
                    tuple(tuple(map(float,q)) for q in points),float(time)))
                if name=='scaffold':
                    for q in (a,b):result.append(Transition('state_changed','bound' if kind=='bond_created' else 'free',
                        (int(q),),(tuple(map(float,positions[q])),),float(time)))
    return result


class EventTap:
    """Read actual topology after each reaction tick, including transient pairings.

    Bounded event storage; overflow is counted, never silently converted to no events.
    The wrapper calls the original exactly once and does not change its return value.
    """
    def __init__(self,c,capacity=4096):
        self.events=deque(maxlen=capacity);self.dropped=0;self.revision=0
        self.before=as_sets(topology(c));original=c.react
        def observed(time,dt,neighbors):
            result=original(time,dt,neighbors)
            after=as_sets(topology(c))
            changes=differences(self.before,after,c.pos,time,
                lambda group,a,b:bond_coordinates(c,group,np.array([[a,b]],dtype=int))[0])
            if changes:self.revision+=1
            for event in changes:
                if len(self.events)==self.events.maxlen:self.dropped+=1
                self.events.append(event)
            self.before=after
            return result
        c.react=observed


def species(c):
    """Chemical families only. No whole-sequence/function recognition in this adapter."""
    labels=[];colors=[];codes=np.empty(len(c.pos),dtype=np.int16)
    def add(label,color):
        labels.append(label);colors.append(color);return len(labels)-1
    def genetics(g,offset):
        support_g=add('Support G','#94b9e8');support_f=add('Support F','#d496e9')
        codes[offset:offset+g.n]=np.where(g.families==0,support_g,support_f)
        bits=g.assembly.atom_bits if g.assembly is not None else g.bits
        for bit,color in ((0,'#45dbc1'),(1,'#ffb865'),(2,'#a493ff')):
            code=add(f'Reconnaissance {bit}',color)
            codes[offset+g.n:offset+2*g.n][bits==bit]=code
        if g.food is not None:
            for bit,color in ((0,'#59c5ed'),(1,'#f1cf77')):
                code=add(f'Précurseur {bit}',color)
                codes[offset+2*g.n+np.arange(g.food.count)[np.arange(g.food.count)%2==bit]]=code
    if hasattr(c,'genetics'):
        if c.offset:
            n=c.membrane.n;codes[:n]=add('Membrane H','#55cfbf');codes[n:2*n]=add('Membrane T','#ecb36c')
        genetics(c.genetics,c.offset)
    elif hasattr(c,'families'):genetics(c,0)
    elif hasattr(c,'rungs') and hasattr(c,'n'):
        n=c.n;codes[:n]=add('Membrane H','#55cfbf');codes[n:2*n]=add('Membrane T','#ecb36c')
        if len(c.pos)>2*n:
            k=c.config.get('retained_probes',0)
            codes[2*n:2*n+k]=add('Sonde retenue','#be9ee8');codes[2*n+k:]=add('Sonde perméable','#eed976')
    else:
        for color in sorted(set(c.colors())):
            code=add(f'Type {len(labels)+1}',color);codes[np.array(c.colors())==color]=code
    rgb=np.array([[int(color[i:i+2],16)/255 for i in (1,3,5)] for color in colors],dtype=np.float32)
    return codes,tuple(labels),rgb


def frame(sim,catalog=None,revision=0):
    codes,labels,palette=catalog or species(sim.chemistry)
    # float32 is a display copy only; simulation state remains float64.
    bonds=topology(sim.chemistry)
    return Frame(sim.chemistry.pos.astype(np.float32,copy=True),codes.copy(),labels,palette.copy(),
        bonds,sim.time,sim.step_index,sim.done,
        None if sim.chemistry.box is None else np.asarray(sim.chemistry.box).copy(),revision,
        {group:bond_coordinates(sim.chemistry,group,pairs).astype('f4') for group,pairs in bonds.items()}
        if sim.chemistry.config.get('dual_faces',False) else None)


class Selection:
    def __init__(self):
        self.anchor=None;self.assembly=True;self.follow=False;self.focus=False;self.partners=True
        self._key=None;self._indices=None

    def indices(self,f):
        if self.anchor is None or not 0<=self.anchor<len(f.positions):return np.empty(0,dtype=int)
        if not self.assembly:return np.array([self.anchor])
        key=(f.revision,self.anchor,len(f.positions))
        if key==self._key:return self._indices
        adjacency={}
        for group,pairs in f.bonds.items():
            if group=='pairing':continue
            for a,b in pairs:
                adjacency.setdefault(a,[]).append(b);adjacency.setdefault(b,[]).append(a)
        found={self.anchor};todo=[self.anchor]
        while todo:
            for q in adjacency.get(todo.pop(),[]):
                if q not in found:found.add(q);todo.append(q)
        self._key=key;self._indices=np.array(sorted(found),dtype=int)
        return self._indices

    def linked_partners(self,f,selected):
        mask=np.zeros(len(f.positions),dtype=bool);mask[selected]=True
        pairs=f.bonds.get('pairing',np.empty((0,2),dtype=int))
        if not len(pairs):return np.empty(0,dtype=int)
        linked=np.unique(pairs[np.any(mask[pairs],axis=1)])
        return linked[~mask[linked]]


def style_arrays(f,opacity,selection):
    rgba=np.ones((len(f.positions),4),dtype=np.float32);rgba[:,:3]=f.palette[f.species]
    rgba[:,3]=np.asarray(opacity)[f.species]
    chosen=selection.indices(f);partners=selection.linked_partners(f,chosen) if selection.partners else np.empty(0,dtype=int)
    if selection.focus and len(chosen):rgba[:,3]*=.08
    rgba[partners,3]=np.maximum(rgba[partners,3],.75)
    rgba[chosen,3]=1.
    emphasis=np.zeros(len(rgba),dtype=np.float32);emphasis[chosen]=1.;emphasis[partners]=.5
    return rgba,emphasis,chosen,partners
