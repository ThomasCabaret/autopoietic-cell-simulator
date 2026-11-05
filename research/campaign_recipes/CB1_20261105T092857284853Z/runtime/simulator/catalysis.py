"""Exploratory sequence -> cleft geometry -> repeated generic food ligation.

Three prepared F beads form one chain. The middle symbol chooses a local angle;
no whole sequence or enzyme identity is tested by forces or reaction eligibility.
Food has an activated, irreversible ligation opportunity everywhere in the bath.
"""
import numpy as np

DEFAULTS=dict(sequence='001',food_pairs=8,box=[10.,10.],temperature=.2,
              assembled=True,ligand_energy=2.,ligand_width=.6,binding_radius=.25,
              binding_rate=20.,unbinding_rate=.1,reaction_radius=.25,reaction_rate=.2,
              angle_strength=100.,native_cosines={'0':.98,'1':-.5})


class CatalysisChemistry:
    def __init__(self,config,rng):
        self.config,self.rng=config,rng
        if len(config['sequence'])!=3 or set(config['sequence'])-set('01'):
            raise ValueError('The current C1 screen uses three binary F units')
        if not isinstance(config['food_pairs'],int) or config['food_pairs']<1:
            raise ValueError('food_pairs must be a positive integer')
        if any(config[k]<=0 for k in ('ligand_width','binding_radius','reaction_radius')):
            raise ValueError('Contact widths must be positive')
        if any(config[k]<0 for k in ('ligand_energy','binding_rate','unbinding_rate','reaction_rate','angle_strength')):
            raise ValueError('Rates and strengths must be nonnegative')
        if any(not np.isfinite(v) or not -1<=v<=1 for v in config['native_cosines'].values()):
            raise ValueError('Native angle cosines must lie in [-1,1]')
        self.n=3+2*config['food_pairs']
        self.bits=np.array([int(b) for b in config['sequence']]+[i%2 for i in range(self.n-3)])
        self.family=np.array([0]*3+[1]*(self.n-3))
        self.kinds=self.family.copy()
        self.contact=np.array([[.12,0.],[0.,.15]])
        self.box=np.array(config['box']); self.mobility=.4
        self.pos=rng.uniform([.5,.5],self.box-.5,(self.n,2))
        if config['assembled']:
            self.pos[:3]=np.array([[-.8,0.],[0.,0.],[.8,0.]])+self.box/2
        self.scaffold={(0,1),(1,2)} if config['assembled'] else set()
        self.products=set(); self.binding=np.full(self.n,-1,dtype=np.int64)
        self.springs=np.empty((0,4)); self.angles=np.empty((0,5))

    def react(self,time,dt,neighbors):
        c,rng=self.config,self.rng; interval=dt*5; events=[]
        used={i for edge in self.products for i in edge}
        for i in np.flatnonzero(self.family==0):
            j=int(self.binding[i])
            if j>=0 and rng.random() < -np.expm1(-c['unbinding_rate']*interval):
                self.binding[i]=self.binding[j]=-1
        pairs=neighbors.pairs(self.pos,c['binding_radius'],'capture').copy(); rng.shuffle(pairs)
        for i,j in pairs:
            if self.family[i]==self.family[j] or self.bits[i]!=self.bits[j]: continue
            if self.binding[i]>=0 or self.binding[j]>=0 or int(i) in used or int(j) in used: continue
            if rng.random() < -np.expm1(-c['binding_rate']*interval): self.binding[i]=j; self.binding[j]=i
        candidates=neighbors.pairs(self.pos,c['reaction_radius'],'ligation').copy(); rng.shuffle(candidates)
        for i,j in candidates:
            if self.family[i]!=1 or self.family[j]!=1 or self.bits[i]==self.bits[j]: continue
            if int(i) in used or int(j) in used: continue
            if rng.random() < -np.expm1(-c['reaction_rate']*interval):
                support=(int(self.binding[i]),int(self.binding[j]))
                self.products.add((int(i),int(j))); used.update((int(i),int(j)))
                events.append({'formed':(int(i),int(j)),'support':support})
                # Local bond occupancy changes substrate affinity; product is released.
                for q in (i,j):
                    partner=int(self.binding[q])
                    if partner>=0: self.binding[partner]=-1; self.binding[q]=-1
        springs=[(i,j,160.,.8) for i,j in sorted(self.scaffold)]
        springs.extend((i,j,80.,.18) for i,j in sorted(self.products))
        springs.extend((int(i),int(j),35.,0.) for i,j in enumerate(self.binding) if j>i)
        self.springs=np.asarray(springs,dtype=float).reshape(-1,4)
        self.angles=np.array([[0,1,2,c['angle_strength'],c['native_cosines'][str(self.bits[1])]]]) if self.scaffold else np.empty((0,5))
        return events

    def extra_forces(self,neighbors):
        c=self.config; force=np.zeros_like(self.pos)
        used={i for edge in self.products for i in edge}
        pairs=neighbors.pairs(self.pos,3*c['ligand_width'],'ligand_force')
        for i,j in pairs:
            if self.family[i]==self.family[j] or self.bits[i]!=self.bits[j]: continue
            if self.binding[i]>=0 or self.binding[j]>=0 or int(i) in used or int(j) in used: continue
            d=self.pos[j]-self.pos[i]; r2=np.dot(d,d)
            f=c['ligand_energy']/c['ligand_width']**2*np.exp(-r2/(2*c['ligand_width']**2))*d
            force[i]+=f; force[j]-=f
        return force

    def observe(self,callback,time,events): callback(time,self.pos,self.bonds(),self.bits,events)
    def bonds(self):
        return {'scaffold':sorted(self.scaffold),'backbone':sorted(self.products),
                'pairing':[(i,int(j)) for i,j in enumerate(self.binding) if j>i]}
    def colors(self):
        return [('#275f94' if b==0 else '#9a4aa0') if f==0 else ('#148e9c' if b==0 else '#df7947') for b,f in zip(self.bits,self.family)]
    def export(self): return {'products':sorted(self.products),'binding':self.binding.tolist()}
    def restore(self,state):
        self.products={tuple(p) for p in state['products']}; self.binding=np.array(state['binding'],dtype=np.int64)


class CatalysisObserver:
    def __init__(self,config):
        self.frames=[]; self.times=[]; self.edges_frames=[]; self.history=[]
        self.events=[]; self.double_bound=0; self.chain_supported=0
        self.last_cleft=None
    def __call__(self,time,pos,bonds,bits,events):
        self.last_cleft=float(np.linalg.norm(pos[0]-pos[2]))
        for e in events:
            self.events.append({'time':time,**e})
            # Count co-binding even in the unconnected-site control.
            if all(i>=0 for i in e['support']):
                self.double_bound+=1
                if bonds['scaffold']: self.chain_supported+=1
        if not self.times or time-self.times[-1]>=.49:
            self.times.append(time)
            if getattr(self,'record_trajectory',True):
                self.frames.append(pos.copy())
                mat=np.zeros((len(pos),len(pos)),dtype=np.uint8)
                for i,j in bonds['scaffold']+bonds['backbone']+bonds['pairing']: mat[i,j]=mat[j,i]=1
                self.edges_frames.append(mat)
            self.history.append({'time':time,'products':len(bonds['backbone']),
                                 'double_bound_ligations':self.double_bound,
                                 'cleft_distance':float(np.linalg.norm(pos[0]-pos[2]))})
    def summary(self):
        return {'products':len(self.events),'double_bound_ligations':self.double_bound,
                'chain_supported_ligations':self.chain_supported,
                'final_cleft_distance':self.last_cleft,
                'history':self.history,'events':self.events}
