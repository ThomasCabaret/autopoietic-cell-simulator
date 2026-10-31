"""C2D-style capture of actual free precursor atoms on composite F sites.

F0 binds free P, F1 binds free R. Adjoining bound F units accelerate a local
P--R bond; no complete chain, target sequence or aggregate name is read here.
"""
import numpy as np
from numba import njit


@njit(cache=True,nogil=True)
def precursor_force(pos,pairs,owners,categories,bits,pairing,site_bound,atom_bound,activity,energy,width):
    force=np.zeros_like(pos);potential=0.
    for i,j in pairs:
        for site,atom in ((i,j),(j,i)):
            s=owners[site]
            if s<0 or categories[atom]<0 or bits[s]!=categories[atom] or pairing[s]>=0:continue
            if site_bound[s]>=0 or atom_bound[atom]>=0:continue
            d=pos[atom]-pos[site]
            value=activity[s]*energy*np.exp(-np.dot(d,d)/(2*width*width))
            f=value/(width*width)*d
            force[site]+=f;force[atom]-=f;potential-=value
    return force,potential


class PrecursorCapture:
    def __init__(self,c):
        self.site_bound=np.full(c.n,-1,dtype=np.int64)
        self.atom_bound=np.full(2*c.n,-1,dtype=np.int64)
        self.refresh(c)

    def refresh(self,c):
        self.owners=np.full(2*c.n,-1,dtype=np.int64)
        self.categories=np.full(2*c.n,-1,dtype=np.int64)
        active=c.rungs[:,1]>=0
        self.categories[np.flatnonzero(~active)]=0
        self.categories[c.n:]=1
        self.categories[c.rungs[active,1]]=-1
        for s in np.flatnonzero(active & (c.families==1)):
            self.owners[c.rungs[s,1]]=s
        self.activity=np.ones(c.n)
        if c.config.get('food_activation',False):
            self.activity[:]=.1/35.
            for i,j in c.edges:self.activity[i]=self.activity[j]=1.

    def react(self,c,dt,neighbors):
        self.refresh(c);interval=dt*5;cfg=c.config
        for s in np.flatnonzero(self.site_bound>=0):
            atom=int(self.site_bound[s]);rate=cfg['food_unbinding_rate']
            if self.activity[s]<1:rate=max(rate,5.)
            if c.rng.random() < -np.expm1(-rate*interval):self.release(atom)
        pairs=neighbors.pairs(c.pos,cfg['food_binding_radius'],'precursor_capture').copy()
        c.rng.shuffle(pairs)
        for i,j in pairs:
            for site,atom in ((int(i),int(j)),(int(j),int(i))):
                s=int(self.owners[site])
                if s<0 or self.categories[atom]<0 or c.bits[s]!=self.categories[atom]:continue
                if c.pairing[s]>=0 or self.site_bound[s]>=0 or self.atom_bound[atom]>=0:continue
                if c.rng.random() < -np.expm1(-self.activity[s]*cfg['food_binding_rate']*interval):
                    self.site_bound[s]=atom;self.atom_bound[atom]=s

    def support(self,p,r):return (int(self.atom_bound[p]),int(self.atom_bound[r]))

    def release(self,atom):
        s=int(self.atom_bound[atom])
        if s>=0:self.site_bound[s]=-1;self.atom_bound[atom]=-1

    def forces(self,c,neighbors):
        pairs=neighbors.pairs(c.pos,3*c.config['food_ligand_width'],'precursor_force')
        return precursor_force(c.pos,pairs,self.owners,self.categories,c.bits,c.pairing,
            self.site_bound,self.atom_bound,self.activity,c.config['food_ligand_energy'],c.config['food_ligand_width'])[0]

    def springs(self,c):
        return [(int(c.rungs[s,1]),int(p),35.,0.) for s,p in enumerate(self.site_bound) if p>=0]

    def export(self):return dict(site_bound=self.site_bound.tolist(),atom_bound=self.atom_bound.tolist())

    def restore(self,c,state):
        self.site_bound=np.array(state['site_bound'],dtype=np.int64)
        self.atom_bound=np.array(state['atom_bound'],dtype=np.int64)
        self.refresh(c)
