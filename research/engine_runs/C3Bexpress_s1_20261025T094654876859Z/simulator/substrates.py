"""Local X/Y capture and uniform ligation on the existing composite F sites."""
import numpy as np
from numba import njit


@njit(cache=True,nogil=True)
def capture_force(pos,pairs,n,families,bits,site_bound,food_bound,used,pairing,energy,width,activity):
    force=np.zeros_like(pos)
    for i,j in pairs:
        if i>=n or j<n: continue
        f=j-n
        if families[i]!=1 or site_bound[i]>=0 or pairing[i]>=0: continue
        if food_bound[f]>=0 or used[f] or bits[i] != f%2: continue
        d=pos[n+j]-pos[n+i]
        factor=activity[i]*energy/(width*width)*np.exp(-np.dot(d,d)/(2*width*width))
        force[n+i]+=factor*d
        force[n+j]-=factor*d
    return force


class Substrates:
    def __init__(self,chemistry,rng):
        c=chemistry; count=2*c.config['food_pairs']
        self.n=c.n; self.count=count
        self.site_bound=np.full(c.n,-1,dtype=np.int64)
        self.food_bound=np.full(count,-1,dtype=np.int64)
        self.used=np.zeros(count,dtype=np.bool_)
        self.products=set()
        self.refresh(c)
        food=rng.uniform([.5,.5],c.box-.5,(count,2))
        c.pos=np.concatenate((c.pos,food))
        c.kinds=np.concatenate((c.kinds,np.full(count,2,dtype=np.int64)))
        c.contact=np.array([[.70,.28,0.],[.28,0.,0.],[0.,0.,.15]])

    def refresh(self,c):
        self.activity=np.ones(c.n)
        if c.config.get('food_activation',False):
            self.activity[:]=.1/35.
            for i,j in c.edges: self.activity[i]=self.activity[j]=1.

    def react(self,c,dt,neighbors):
        cfg,rng=c.config,c.rng; interval=5*dt; events=[]
        self.refresh(c)
        for i in np.flatnonzero(self.site_bound>=0):
            f=int(self.site_bound[i])
            off=max(cfg['food_unbinding_rate'],5.) if self.activity[i]<1 else cfg['food_unbinding_rate']
            if rng.random() < -np.expm1(-off*interval):
                self.site_bound[i]=self.food_bound[f]=-1
        pairs=neighbors.pairs(c.pos[self.n:],cfg['food_binding_radius'],'food_capture').copy()
        rng.shuffle(pairs)
        for i,j in pairs:
            if i>=self.n or j<self.n: continue
            f=int(j-self.n); i=int(i)
            if c.families[i]!=1 or c.pairing[i]>=0 or self.site_bound[i]>=0: continue
            if self.food_bound[f]>=0 or self.used[f] or c.bits[i]!=f%2: continue
            if rng.random() < -np.expm1(-self.activity[i]*cfg['food_binding_rate']*interval):
                self.site_bound[i]=f; self.food_bound[f]=i
        pairs=neighbors.pairs(c.pos[2*self.n:],cfg['food_reaction_radius'],'food_ligation').copy()
        rng.shuffle(pairs)
        for a,b in pairs:
            a,b=int(a),int(b)
            if a%2==b%2 or self.used[a] or self.used[b]: continue
            if rng.random() < -np.expm1(-cfg['food_reaction_rate']*interval):
                support=(int(self.food_bound[a]),int(self.food_bound[b]))
                self.products.add((a,b)); self.used[a]=self.used[b]=True
                events.append(dict(kind='food',formed=(a,b),support=support))
                for f in (a,b):
                    i=int(self.food_bound[f])
                    if i>=0: self.site_bound[i]=-1; self.food_bound[f]=-1
        return events

    def forces(self,c,neighbors):
        pairs=neighbors.pairs(c.pos[self.n:],3*c.config['food_ligand_width'],'food_force')
        return capture_force(c.pos,pairs,self.n,c.families,c.bits,self.site_bound,
                             self.food_bound,self.used,c.pairing,
                             c.config['food_ligand_energy'],c.config['food_ligand_width'],self.activity)

    def springs(self):
        n=self.n
        result=[(2*n+a,2*n+b,80.,.18) for a,b in sorted(self.products)]
        result.extend((n+i,2*n+int(f),35.,0.) for i,f in enumerate(self.site_bound) if f>=0)
        return result

    def export(self):
        return dict(products=sorted(self.products),site_bound=self.site_bound.tolist(),food_bound=self.food_bound.tolist())

    def restore(self,state):
        self.products={tuple(p) for p in state['products']}
        self.site_bound=np.array(state['site_bound'],dtype=np.int64)
        self.food_bound=np.array(state['food_bound'],dtype=np.int64)
        self.used[:]=False
        for a,b in self.products: self.used[a]=self.used[b]=True
