"""Shared deterministic scheduler and CPU mechanics; independent of any UI."""
import copy
import numpy as np
from .config import resolve
from .registry import MODELS
from .spatial import Neighborhood
from .physics import force_kernel
from .reference import integrate


class Simulation:
    def __init__(self, config):
        self.config = resolve(config)
        self.rng = np.random.default_rng(self.config['seed'])
        self.chemistry = MODELS[self.config['model']][0](self.config['chemistry'],self.rng)
        self.dt = self.config['engine']['dt']
        self.reaction_every = self.config['engine']['reaction_every']
        self.neighbors = Neighborhood(self.config['engine']['spatial'],self.config['engine']['skin'])
        self.step_index = 0
        self.prepared = False
        self.listeners = []
        self.target_step = round(self.config['duration']/self.dt)

    @property
    def time(self):
        return self.step_index*self.dt

    @property
    def done(self):
        return self.step_index>=self.target_step

    def prepare(self):
        if self.prepared:
            return
        events=[]
        if self.step_index%self.reaction_every==0:
            # Existing hook API uses 5*its dt argument as reaction interval.
            # Preserve the default argument bit-for-bit; mechanics always uses self.dt.
            reaction_dt=self.dt if self.reaction_every==5 else self.dt*self.reaction_every/5
            events=self.chemistry.react(self.time,reaction_dt,self.neighbors)
        if self.step_index%self.config['engine']['sample_every']==0 or events or self.done:
            for callback in self.listeners:
                self.chemistry.observe(callback,self.time,events)
        self.prepared=True

    def advance(self, steps=1):
        if not isinstance(steps,int) or steps<0:
            raise ValueError('steps must be a nonnegative integer')
        self.prepare()
        c=self.chemistry
        for _ in range(min(steps,max(0,self.target_step-self.step_index))):
            pairs=self.neighbors.pairs(c.pos,float(c.contact.max()),'core')
            force=force_kernel(c.pos,pairs,c.kinds,c.contact,c.springs,c.angles)
            force+=c.extra_forces(self.neighbors)
            c.pos=integrate(c.pos,force,self.rng,self.dt,c.mobility,c.config['temperature'],c.box)
            self.step_index+=1
            self.prepared=False
            self.prepare()

    def snapshot(self):
        # Independent values: consumers cannot mutate engine arrays or bonds.
        return {'positions':self.chemistry.pos.copy(), 'bonds':copy.deepcopy(self.chemistry.bonds()),
                'colors':self.chemistry.colors(), 'time':self.time, 'step':self.step_index,
                'done':self.done, 'box':None if self.chemistry.box is None else self.chemistry.box.tolist()}
