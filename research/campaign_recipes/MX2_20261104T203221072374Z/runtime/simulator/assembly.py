"""Persistent precursor beads and locally saturated, constructible P--R bonds.

Support identity is an elementary kind; the symbol is carried by the actual
recognition bead. No requested sequence, aggregate or future-partner lookup in
the reaction. Prepared seeds/stock are initial conditions only.
"""
import numpy as np
from .precursors import PrecursorCapture


class RungAssembly:
    def __init__(self,c,rng):
        self.atom_bits=c.bits.copy()
        self.events=[]
        length=len(c.config['sequence'])
        self.initial_supports=set(range(c.n if c.config['assembled_stock'] else length))
        self.initial_supports.update(q for g in c.initial_groups for q in g['units'])
        self.catalyst=PrecursorCapture(c) if c.config.get('rung_catalysis',False) else None
        if c.config['assembled_stock']:return
        free=np.array([i for i in range(length,c.n) if i not in self.initial_supports],dtype=np.int64)
        c.rungs[free,1]=-1
        c.bits[free]=-1
        # Independent dispersed R atoms, initially outside every capture sphere.
        # No correspondence between support index and free R chemical identity.
        for r in c.n+free:
            for _ in range(20000):
                p=rng.uniform([.6,.6],c.box-.6)
                if np.min(np.linalg.norm(c.pos[:c.n]-p,axis=1))>max(.65,c.config['rung_capture_radius']):break
            else:raise RuntimeError('Cannot disperse precursor recognizers outside capture radius')
            c.pos[r]=p
        if self.catalyst is not None:self.catalyst.refresh(c)

    def react(self,c,time,dt,neighbors):
        if self.catalyst is not None:self.catalyst.react(c,dt,neighbors)
        if np.all(c.rungs[:,1]>=0):return
        occupied=set(int(r) for r in c.rungs[:,1] if r>=0)
        pairs=neighbors.pairs(c.pos,c.config['rung_capture_radius'],'rung_assembly')
        candidates=pairs[(pairs[:,0]<c.n)&(pairs[:,1]>=c.n)]
        c.rng.shuffle(candidates)
        probability=-np.expm1(-c.config['rung_formation_rate']*dt*5)
        for s,r in candidates:
            if c.rungs[s,1]>=0 or int(r) in occupied:continue
            support=(-1,-1);catalyzed=False
            if self.catalyst is not None:
                support=self.catalyst.support(s,r)
                catalyzed=all(i>=0 for i in support) and tuple(sorted(support)) in c.edges
            p=-np.expm1(-c.config['rung_catalytic_rate']*dt*5) if catalyzed else probability
            if c.rng.random()>=p:continue
            c.rungs[s,1]=r
            c.bits[s]=self.atom_bits[r-c.n]
            c.capacities[s]=1 if c.bits[s]==c.config['caps_symbol'] else 2
            occupied.add(int(r))
            event=dict(time=float(time),support=int(s),recognizer=int(r),symbol=int(c.bits[s]))
            if self.catalyst is not None:
                event.update(catalytic_support=list(support),catalyzed=bool(catalyzed))
                self.catalyst.release(s);self.catalyst.release(r)
            self.events.append(event)
        if self.catalyst is not None:self.catalyst.refresh(c)

    def export(self,c):
        state=dict(rungs=c.rungs.tolist(),bits=c.bits.tolist(),events=self.events)
        if self.catalyst is not None:state['capture']=self.catalyst.export()
        return state

    def restore(self,c,state):
        c.rungs=np.array(state['rungs'],dtype=np.int64)
        c.bits=np.array(state['bits'],dtype=np.int64)
        c.capacities=np.where(c.bits==c.config['caps_symbol'],1,2)
        self.events=list(state['events'])
        if self.catalyst is not None:self.catalyst.restore(c,state['capture'])
