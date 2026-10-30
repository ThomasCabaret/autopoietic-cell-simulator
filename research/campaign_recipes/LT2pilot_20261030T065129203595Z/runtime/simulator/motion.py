"""Experimental inertial mechanics, with cache invalidation owned by the engine.

No component, molecule label or target is read. Pair OU impulses are reciprocal;
all conservative interactions use the same finite-range forces as the old path.
"""
import numpy as np
from numba import njit
from .physics import force_kernel


@njit(cache=True)
def pair_ou(pos,vel,pairs,noise,dt,mass,gamma,temperature,cutoff,reverse=False):
    for q in range(len(pairs)):
        k=len(pairs)-1-q if reverse else q
        i,j=pairs[k,0],pairs[k,1]
        x,y=pos[i,0]-pos[j,0],pos[i,1]-pos[j,1]
        distance=np.sqrt(x*x+y*y)
        if distance<=1e-12 or distance>=cutoff:continue
        x/=distance;y/=distance
        weight=1-distance/cutoff
        decay=np.exp(-2*gamma*weight*weight*dt/mass)
        u=(vel[i,0]-vel[j,0])*x+(vel[i,1]-vel[j,1])*y
        new=decay*u+np.sqrt(2*temperature/mass*(1-decay*decay))*noise[k]
        impulse=.5*(new-u)
        vel[i,0]+=impulse*x;vel[i,1]+=impulse*y
        vel[j,0]-=impulse*x;vel[j,1]-=impulse*y


class InertialMotion:
    def __init__(self,c,rng,settings=None):
        cfg=c.config if settings is None else settings;self.kind=cfg['motion'];self.mass=cfg['mass']
        self.gamma=cfg['damping'];self.cutoff=cfg['dpd_cutoff']
        self.velocities=rng.normal(size=c.pos.shape)*np.sqrt(c.config['temperature']/self.mass)
        self.force=None;self.steps=0;self.force_evaluations=0;self.pair_visits=0;self.max_displacement=0.

    def conservative(self,c,neighbors):
        pairs=neighbors.pairs(c.pos,float(c.contact.max()),'core')
        force=force_kernel(c.pos,pairs,c.kinds,c.contact,c.springs,c.angles)
        force+=c.extra_forces(neighbors)
        if c.box is not None:force+=100*(np.maximum(-c.pos,0)-np.maximum(c.pos-c.box,0))
        self.force_evaluations+=1
        return force

    def thermostat(self,c,rng,neighbors,dt,reverse=False):
        pairs=neighbors.pairs(c.pos,self.cutoff,'dpd_thermostat')
        noise=rng.normal(size=len(pairs))
        pair_ou(c.pos,self.velocities,pairs,noise,dt,self.mass,self.gamma,
            c.config['temperature'],self.cutoff,reverse)
        self.pair_visits+=len(pairs)

    def step(self,c,rng,dt,neighbors):
        if self.force is None:self.force=self.conservative(c,neighbors)
        old=c.pos.copy();v=self.velocities
        if self.kind=='dpd':self.thermostat(c,rng,neighbors,dt/2)
        v+=self.force*(dt/(2*self.mass))
        if self.kind=='langevin':
            c.pos=c.pos+v*(dt/2)
            decay=np.exp(-self.gamma*dt)
            v*=decay
            v+=np.sqrt(c.config['temperature']/self.mass*(1-decay*decay))*rng.normal(size=v.shape)
            c.pos+=v*(dt/2)
        else:
            c.pos=c.pos+v*dt
        self.force=self.conservative(c,neighbors)
        v+=self.force*(dt/(2*self.mass))
        if self.kind=='dpd':self.thermostat(c,rng,neighbors,dt/2,True)
        displacement=float(np.linalg.norm(c.pos-old,axis=1).max())
        if not np.isfinite(v).all() or not np.isfinite(c.pos).all() or displacement>1.:
            raise FloatingPointError('Inertial integrator unstable; reduce dt, never clip motion')
        self.max_displacement=max(self.max_displacement,displacement);self.steps+=1

    def diagnostics(self,c):
        bonds=c.springs
        error=np.abs(np.linalg.norm(c.pos[bonds[:,0].astype(int)]-c.pos[bonds[:,1].astype(int)],axis=1)-bonds[:,3]) if len(bonds) else np.array([0.])
        return dict(kinetic_temperature=float(self.mass*np.mean(self.velocities**2)),
            momentum=(self.mass*self.velocities.sum(axis=0)).tolist(),
            max_bead_speed=float(np.linalg.norm(self.velocities,axis=1).max()),
            max_step_displacement=self.max_displacement,force_evaluations=self.force_evaluations,
            thermostat_pair_visits=self.pair_visits,steps=self.steps,max_bond_extension=float(error.max()))

    def export(self):
        return dict(velocities=self.velocities.tolist(),force=None if self.force is None else self.force.tolist(),
            steps=self.steps,force_evaluations=self.force_evaluations,pair_visits=self.pair_visits,
            max_displacement=self.max_displacement)

    def restore(self,state):
        self.velocities=np.array(state['velocities'],dtype=float)
        self.force=None if state['force'] is None else np.array(state['force'],dtype=float)
        self.steps=state['steps'];self.force_evaluations=state['force_evaluations']
        self.pair_visits=state['pair_visits'];self.max_displacement=state['max_displacement']


class MotionAudit:
    """Passive thermal/readout companion for reactive hooks; no engine feedback."""
    def __init__(self,sim,state=None,interval=.5):
        self.sim=sim;self.interval=interval
        self.state=state if state is not None else dict(history=[],next_sample=0.)

    def __call__(self,time,*args):
        if time<self.state['next_sample']-1e-8 and not self.sim.done:return
        row=dict(time=float(time),**self.sim.motion.diagnostics(self.sim.chemistry))
        self.state['history'].append(row)
        self.state['next_sample']=(int((time+1e-8)/self.interval)+1)*self.interval

    def summary(self):
        return dict(target_temperature=self.sim.chemistry.config['temperature'],
            history=self.state['history'],interval=self.interval,
            scope='All-bead kinetic temperature and bond/readout samples, observation only. Reaction potential changes and external release may heat the bath; no global rescaling.')
