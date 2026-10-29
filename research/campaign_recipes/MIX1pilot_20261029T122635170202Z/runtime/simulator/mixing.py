"""Mechanics-only diagnostic: the shared integrator, fixed molecules, no reactions."""
import numpy as np
from scipy.spatial import cKDTree

DEFAULTS = dict(molecules=200, beads_per_molecule=2, steric=True,
    temperature=.08, box=[24.,18.], initial_half=True,
    record_interval=10., contact_interval=.05)


class MixingChemistry:
    def __init__(self, config, rng):
        self.config=config;self.n=config['molecules'];self.size=config['beads_per_molecule']
        self.box=np.array(config['box'],dtype=float);self.mobility=.25
        centers=[]
        for _ in range(self.n):
            high=self.box-[.5,.5]
            if config['initial_half']:high[0]=self.box[0]/2-.5
            for attempt in range(100000):
                p=rng.uniform([.5,.5],high)
                if not centers or np.linalg.norm(np.asarray(centers)-p,axis=1).min()>.6:break
            else:raise ValueError('Initial half-box is too dense')
            centers.append(p)
        centers=np.asarray(centers)
        self.springs=np.empty((0,4));self.angles=np.empty((0,5))
        if self.size==2:
            theta=rng.uniform(0,2*np.pi,self.n)
            u=.225*np.column_stack([np.cos(theta),np.sin(theta)])
            self.pos=np.vstack([centers-u,centers+u])
            self.kinds=np.concatenate([np.zeros(self.n,dtype=np.int64),np.ones(self.n,dtype=np.int64)])
            self.contact=np.array([[.70,.28],[.28,0.]])
            self.springs=np.array([(i,self.n+i,180.,.45) for i in range(self.n)])
        else:
            self.pos=centers.copy();self.kinds=np.zeros(self.n,dtype=np.int64)
            self.contact=np.array([[.70]])
        if not config['steric']:self.contact[:]=0.

    def react(self,time,dt,neighbors):return []
    def extra_forces(self,neighbors):return np.zeros_like(self.pos)
    def observe(self,callback,time,events):callback(time,self.pos)
    def bonds(self):return dict(scaffold=[(i,self.n+i) for i in range(self.n)] if self.size==2 else [])
    def colors(self):return ['#37b9ca']*self.n+(['#e9a65c']*self.n if self.size==2 else [])
    def export(self):return {}
    def restore(self,state):
        if state:raise ValueError('No reactive state in the mixing diagnostic')


def information(a,b,bins=8):
    joint=np.bincount(bins*a+b,minlength=bins*bins).reshape(bins,bins).astype(float)
    joint/=joint.sum();expected=joint.sum(axis=1)[:,None]*joint.sum(axis=0)[None,:]
    good=joint>0
    return float(np.sum(joint[good]*np.log(joint[good]/expected[good])))


def geometric_clusters(points,radius=1.5):
    parent=np.arange(len(points))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    pairs=cKDTree(points).query_pairs(radius,output_type='ndarray')
    for i,j in pairs:parent[root(int(i))]=root(int(j))
    sizes=np.bincount([root(i) for i in range(len(points))]);sizes=sizes[sizes>0]
    return dict(radius=radius,count=len(sizes),largest=int(sizes.max()),
        mean_degree=2*len(pairs)/len(points))


class MixingObserver:
    def __init__(self,config):
        self.config=config;self.n=config['molecules'];self.size=config['beads_per_molecule']
        self.box=np.array(config['box'],dtype=float);self.frames=[];self.times=[]
        self.record_trajectory=False
        self.radii=(.3,.7,1.5)
        self.state=dict(last_time=None,initial=None,previous=None,initial_bins=None,
            initial_neighbors=None,next_record=0.,history=[],bulk_square=0.,bulk_count=0,
            bulk_time=0.,seen=np.zeros((self.n,self.n),dtype=np.uint8),
            contacts={str(r):dict(active={},pair_time=0.,episodes=0,completed=0,
                completed_duration=0.,max_completed_duration=0.) for r in self.radii})
        # Independent analysis randomness, never the simulation PRNG.
        rng=np.random.default_rng(74000+config.get('seed',0))
        self.permutations=np.array([rng.permutation(self.n) for _ in range(32)])
        draws=rng.multinomial(self.n,np.ones(8)/8,size=2048)/self.n
        self.uniform_tv_reference=dict(mean=float(np.abs(draws-1/8).sum(axis=1).mean()/2),
            p95=float(np.quantile(np.abs(draws-1/8).sum(axis=1)/2,.95)))

    def bins(self,points):
        xy=np.clip((points/self.box*[4,2]).astype(int),[0,0],[3,1])
        return 2*xy[:,0]+xy[:,1]

    def __call__(self,time,pos):
        s=self.state
        if s['last_time'] is not None and time-s['last_time']<self.config['contact_interval']-1e-8:return
        centers=(pos[:self.n]+pos[self.n:])/2 if self.size==2 else pos
        sites=pos[self.n:] if self.size==2 else pos
        tree=cKDTree(centers)
        if s['initial'] is None:
            s['initial']=centers.copy();s['previous']=centers.copy();s['initial_bins']=self.bins(centers)
            s['initial_neighbors']=tree.query(centers,k=6)[1][:,1:]
        last=s['last_time'];span=0. if last is None else time-last
        if span:
            bulk=np.all((centers>1.)&(centers<self.box-1.)&(s['previous']>1.)&(s['previous']<self.box-1.),axis=1)
            square=np.sum((centers-s['previous'])**2,axis=1)
            s['bulk_square']+=float(square[bulk].sum());s['bulk_count']+=int(bulk.sum())
            s['bulk_time']+=span*int(bulk.sum())
        pairs=cKDTree(sites).query_pairs(max(self.radii),output_type='ndarray')
        distance=np.sum((sites[pairs[:,0]]-sites[pairs[:,1]])**2,axis=1)
        for bit,radius in enumerate(self.radii):
            c=s['contacts'][str(radius)];active=c['active']
            c['pair_time']+=len(active)*span
            current={int(i)*self.n+int(j) for i,j in pairs[distance<=radius*radius]}
            for key in set(active)-current:
                duration=time-active.pop(key);c['completed']+=1;c['completed_duration']+=duration
                c['max_completed_duration']=max(c['max_completed_duration'],duration)
            for key in current-set(active):active[key]=float(time);c['episodes']+=1
            if current:
                ids=np.array(list(current),dtype=int)
                s['seen'][ids//self.n,ids%self.n]|=1<<bit
        s['previous']=centers.copy();s['last_time']=float(time)
        if not self.times:self.times=[float(time)]
        if time<s['next_record']-1e-8:return
        bins=self.bins(centers);counts=np.bincount(bins,minlength=8)
        mi=information(s['initial_bins'],bins)
        null=np.array([information(s['initial_bins'],bins[p]) for p in self.permutations])
        probabilities=np.bincount(s['initial_bins'],minlength=8)/self.n
        p=probabilities[probabilities>0];entropy=-float(np.sum(p*np.log(p)))
        nearest=tree.query(centers,k=6)[1][:,1:]
        retention=float(np.mean([len(set(a)&set(b))/5 for a,b in zip(s['initial_neighbors'],nearest)]))
        chance=5/(self.n-1)
        initial_mode=float(np.cos(np.pi*s['initial'][:,0]/self.box[0]).mean())
        contacts={}
        for bit,radius in enumerate(self.radii):
            seen=(s['seen']&(1<<bit))!=0;unique=seen.sum(axis=0)+seen.sum(axis=1)
            c=s['contacts'][str(radius)]
            contacts[str(radius)]=dict(current_pairs=len(c['active']),unique_pairs=int(seen.sum()),
                mean_distinct_partners=float(unique.mean()),p10_distinct_partners=float(np.quantile(unique,.1)),
                fraction_with_no_encounter=float(np.mean(unique==0)),episodes=c['episodes'],
                pair_time=c['pair_time'],completed_episodes=c['completed'],
                mean_completed_duration=c['completed_duration']/c['completed'] if c['completed'] else None,
                longest_completed_duration=c['max_completed_duration'],
                right_censored_episodes=len(c['active']))
        row=dict(time=float(time),right_fraction=float(np.mean(centers[:,0]>=self.box[0]/2)),
            spatial_grid_counts=counts.tolist(),spatial_tv=float(np.abs(counts/self.n-1/8).sum()/2),
            cosine_mode=float(np.cos(np.pi*centers[:,0]/self.box[0]).mean()),initial_cosine_mode=initial_mode,
            mean_square_displacement=float(np.sum((centers-s['initial'])**2,axis=1).mean()),
            short_lag_bulk_D=s['bulk_square']/(4*s['bulk_time']) if s['bulk_time'] else None,
            initial_neighbor_retention=retention,neighbor_chance=chance,
            neighbor_retention_excess=(retention-chance)/(1-chance),
            position_mutual_information=mi,permutation_mi_mean=float(null.mean()),
            permutation_mi_sd=float(null.std()),corrected_normalized_mi=max(0.,mi-float(null.mean()))/entropy if entropy else 0.,
            geometric_clusters=geometric_clusters(centers),contacts=contacts,
            outside_soft_box_fraction=float(np.mean(np.any((centers<0)|(centers>self.box),axis=1))))
        s['history'].append(row);s['next_record']=(int((time+1e-8)/self.config['record_interval'])+1)*self.config['record_interval']

    def summary(self):
        D=.25*self.config['temperature']/self.size
        history=self.state['history']
        thresholds=dict(occupation=lambda r:abs(r['right_fraction']-.5)<=.1 and r['spatial_tv']<=self.uniform_tv_reference['p95'],
            neighbor_replacement=lambda r:r['neighbor_retention_excess']<=.1,
            positional_memory=lambda r:r['corrected_normalized_mi']<=.1)
        first={}
        for name,condition in thresholds.items():
            hit=next((r['time'] for r in history if condition(r)),None)
            first[name]=dict(time=hit if hit is not None else self.state['last_time'],event=hit is not None)
        return dict(history=history,first_passages=first,uniform_tv_reference=self.uniform_tv_reference,
            isolated_center_D_prediction=D,
            reflecting_first_mode_tau_prediction=self.box[0]**2/(np.pi**2*D) if D else None,
            molecule_count=self.n,bead_count=self.n*self.size,
            contact_sampling_interval=self.config['contact_interval'],
            scope='No chemical reactions, affinities or transient bonds. Fixed monomers/dimers under the existing Brownian integrator and soft walls. Geometric encounters do not imply reactive eligibility.',
            limitations='Contacts sampled, sub-sample encounters may be missed; episode durations are discretized and active episodes right-censored. Grid/MI finite-sample references are descriptive, not independent significance tests. First threshold passages are not a proof of sustained equilibrium. Ideal reflecting theory approximates soft walls and ignores steric forces.')
