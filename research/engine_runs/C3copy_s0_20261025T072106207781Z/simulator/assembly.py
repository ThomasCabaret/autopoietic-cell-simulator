"""Persistent precursor beads and locally saturated, constructible P--R bonds.

Support identity is an elementary kind; the symbol is carried by the actual
recognition bead. No requested sequence, aggregate or future-partner lookup in
the reaction. Prepared seeds/stock are initial conditions only.
"""
import numpy as np


class RungAssembly:
    def __init__(self,c,rng):
        self.atom_bits=c.bits.copy()
        self.events=[]
        length=len(c.config['sequence'])
        self.initial_supports=set(range(c.n if c.config['assembled_stock'] else length))
        if c.config['assembled_stock']:return
        c.rungs[length:,1]=-1
        c.bits[length:]=-1
        # Independent dispersed R atoms, initially outside every capture sphere.
        # No correspondence between support index and free R chemical identity.
        for r in range(c.n+length,2*c.n):
            for _ in range(20000):
                p=rng.uniform([.6,.6],c.box-.6)
                if np.min(np.linalg.norm(c.pos[:c.n]-p,axis=1))>max(.65,c.config['rung_capture_radius']):break
            else:raise RuntimeError('Cannot disperse precursor recognizers outside capture radius')
            c.pos[r]=p

    def react(self,c,time,dt,neighbors):
        occupied=set(int(r) for r in c.rungs[:,1] if r>=0)
        pairs=neighbors.pairs(c.pos,c.config['rung_capture_radius'],'rung_assembly')
        candidates=pairs[(pairs[:,0]<c.n)&(pairs[:,1]>=c.n)]
        c.rng.shuffle(candidates)
        probability=-np.expm1(-c.config['rung_formation_rate']*dt*5)
        for s,r in candidates:
            if c.rungs[s,1]>=0 or int(r) in occupied:continue
            if c.rng.random()>=probability:continue
            c.rungs[s,1]=r
            c.bits[s]=self.atom_bits[r-c.n]
            c.capacities[s]=1 if c.bits[s]==c.config['caps_symbol'] else 2
            occupied.add(int(r))
            self.events.append(dict(time=float(time),support=int(s),recognizer=int(r),symbol=int(c.bits[s])))

    def export(self,c):
        return dict(rungs=c.rungs.tolist(),bits=c.bits.tolist(),events=self.events)

    def restore(self,c,state):
        c.rungs=np.array(state['rungs'],dtype=np.int64)
        c.bits=np.array(state['bits'],dtype=np.int64)
        c.capacities=np.where(c.bits==c.config['caps_symbol'],1,2)
        self.events=list(state['events'])
