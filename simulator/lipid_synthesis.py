"""L1 prototype: the existing F01 co-recruiter binds real H/T, then MD2 ports act.

Separate candidate extension, not the integrated P/R/L chemistry. Prepared F
uses CopyChemistry; capture uses PrecursorCapture unchanged except ligand types.
Neither dynamics nor capture reads a complete tool, membrane or target product.
"""
import copy
import numpy as np
from .copy import CopyChemistry
from .precursors import PrecursorCapture,capture_stiffness
from .linked_lipids import LinkedLipids
from .coupled_bath import ScopedNeighbors
from .config import COPY_DEFAULTS


DEFAULTS=dict(temperature=.08,box=[12.,9.],food_units=24,tool_count=4,tool_linked=True,
    rung_capture_radius=.58,rung_formation_rate=.0001,rung_catalytic_rate=20.,
    food_binding_radius=.25,food_binding_rate=20.,food_unbinding_rate=.1,
    food_ligand_energy=2.,food_ligand_width=.6,food_activation=True,
    short_length=.98,dock_width=.3,dock_energy=4.,dock_capture=.25,dock_rate=25.,
    bond_off_rate=.02,break_extension=.35,bonding=True,
    contact_exchange_rate=.2,contact_exchange_capture=.8,terminal_exchange=True,
    formation_gate='none',tool_lipid_contact=.55,capture_curvature='legacy',tool_pose='straight',contact_exchange_gate='none',contact_update_gate='none',free_port_potential='additive',initial_lipids=[])


def initialize_lipids(c):
    """Prepared isolated H/T dimers consume the existing food stock only."""
    for i,item in enumerate(c.config['initial_lipids']):
        h,t=c.prefix+i,c.prefix+c.config['food_units']+i
        c.pos[h]=item['head'];c.pos[t]=item['tail'];c.lipids.bind(h,t)


def native_tool_pose(host,pairs):
    """Constructed-start geometry only; never called by reactions or observers."""
    touched=set()
    for i,j in sorted(pairs):
        if i in touched or j in touched:raise ValueError('Native pose initializer requires disjoint prepared site pairs')
        touched.update((i,j));d=host.pos[j]-host.pos[i];d=d/np.linalg.norm(d)
        normal=np.array([-d[1],d[0]])
        old=(host.pos[host.rungs[i,1]]-host.pos[i])+(host.pos[host.rungs[j,1]]-host.pos[j])
        if np.dot(normal,old)<0:normal=-normal
        for q,along in ((i,d),(j,-d)):
            cosine=host.config['functional_cosines'].get(str(int(host.bits[q])),0.)
            host.pos[host.rungs[q,1]]=host.pos[q]+.45*(cosine*along+np.sqrt(1-cosine*cosine)*normal)


class HTPrecursorCapture(PrecursorCapture):
    """Same local site/capture kernel; H is donor0 and T acceptor1."""
    def __init__(self,c):
        self.stiffness=capture_stiffness(c.config)
        self.site_bound=np.full(c.n,-1,dtype=np.int64)
        self.atom_bound=np.full(len(c.pos),-1,dtype=np.int64);self.refresh(c)

    def refresh(self,c):
        self.owners=np.full(len(c.pos),-1,dtype=np.int64)
        self.owners[c.rungs[:,1]]=np.arange(c.n)
        self.categories=c.ligand_types.copy()
        if c.lipids.rungs:
            self.categories[list(c.lipids.rungs)]=-1;self.categories[list(c.lipids.rungs.values())]=-1
        self.activity=np.ones(c.n)
        if c.config['food_activation']:
            self.activity[:]=.1/35.
            for i,j in c.edges:self.activity[i]=self.activity[j]=1.

    def springs(self,c):
        return [(int(c.rungs[s,1]),int(a),self.stiffness,0.) for s,a in enumerate(self.site_bound) if a>=0]


class LipidSynthesisChemistry:
    def __init__(self,config,rng):
        self.config,self.rng=config,rng;self.box=np.asarray(config['box'],dtype=float)
        self.host=None
        if config['tool_count']:
            g=dict(COPY_DEFAULTS,sequence='01',seed_family=1,free_units=0,
                function_units=2*(config['tool_count']-1),box=config['box'],temperature=config['temperature'],
                template=config['tool_linked'],backbone_angle=20.,functional_cosines={'0':.8,'1':.8},
                constructible=True,assembled_stock=True,rung_catalysis=False,
                initial_assemblies=[dict(family=1,sequence='01',backbone=config['tool_linked']) for _ in range(config['tool_count']-1)])
            self.host=CopyChemistry(g,rng)
            if config['tool_pose']=='native':native_tool_pose(self.host,[(0,1)]+[q['units'] for q in self.host.initial_groups])
            prefix=self.host.pos.copy();self.n=self.host.n;self.rungs=self.host.rungs;self.bits=self.host.bits
        else:
            prefix=np.empty((0,2));self.n=0;self.rungs=np.empty((0,2),dtype=np.int64);self.bits=np.empty(0,dtype=np.int64)
        self.prefix=len(prefix);count=config['food_units']
        # Independent localized H and T, never paired by their initial indices.
        food=rng.uniform([.6,.6],self.box-.6,size=(2*count,2))
        self.pos=np.concatenate((prefix,food));self.lipids=LinkedLipids();self.births=[];self.exchanges=[]
        self.ligand_types=np.full(len(self.pos),-1,dtype=np.int64)
        self.ligand_types[self.prefix:self.prefix+count]=0;self.ligand_types[self.prefix+count:]=1
        self.edges=set();self.pairing=np.full(self.n,-1,dtype=np.int64);self._views()
        self.capture=HTPrecursorCapture(self)
        # Same core F/F matrix, MD2 L/L .4 and bound F/L .55. Free H/T pass F.
        r=config['tool_lipid_contact']
        self.contact=np.array([[.7,.28,0.,r],[.28,0.,0.,r],[0.,0.,.4,.4],[r,r,.4,.4]])
        if config['formation_gate']=='metropolis':
            self.transition_stats={key:dict(proposals=0,contact_time=0.,weighted_time=0.,positive_delta=0,
                sum_positive_delta=0.,max_delta=None,min_delta=None,formed=0) for key in ('background','catalytic')}
        if config['initial_lipids']:
            initialize_lipids(self)
            self.capture.refresh(self)
        self.mobility=np.concatenate((np.full(self.prefix,.25),np.full(2*count,.4)))[:,None]
        self.springs=np.empty((0,4));self.angles=np.empty((0,5));self._mechanics()

    def _views(self):
        if self.host is not None:
            self.host.pos=self.pos[:self.prefix];self.edges=self.host.edges;self.pairing=self.host.pairing

    def _mechanics(self):
        h=self.host;rows=[] if h is None else h.springs.tolist()
        rows+=self.lipids.springs()+self.capture.springs(self)
        self.springs=np.asarray(rows,dtype=float).reshape(-1,4)
        self.angles=np.empty((0,5)) if h is None else h.angles.copy()
        prefix=np.empty(0,dtype=np.int64) if h is None else h.kinds
        self.kinds=np.concatenate((prefix,np.full(len(self.pos)-self.prefix,2,dtype=np.int64)))
        if self.lipids.rungs:
            self.kinds[list(self.lipids.rungs)]=3;self.kinds[list(self.lipids.rungs.values())]=3

    def react(self,time,dt,neighbors):
        self._views()
        if self.host is not None:self.host.react(time,dt,ScopedNeighbors(neighbors,'F:'))
        self._views();self.capture.react(self,dt,ScopedNeighbors(neighbors,'HT:'))
        self.form_lipids(time,dt*5,neighbors)
        exchanges=self.lipids.react(self.pos,self.config,self.rng,ScopedNeighbors(neighbors,'L:'),dt*5)
        self.exchanges.extend(dict(time=float(time),**e) for e in exchanges)
        self._mechanics();return []

    def form_lipids(self,time,interval,neighbors):
        pairs=self.lipid_candidates(neighbors).copy();self.rng.shuffle(pairs)
        fixed_pairs=None
        for a,b in pairs:
            a,b=int(a),int(b)
            if self.capture.categories[a]==1 and self.capture.categories[b]==0:a,b=b,a
            if self.capture.categories[a]!=0 or self.capture.categories[b]!=1:continue
            # Material compatibility, independent of donor/acceptor site affinity.
            # Mixed baths may also capture P/R on those same sites.
            if self.ligand_types[a]!=0 or self.ligand_types[b]!=1:continue
            sites=self.capture.support(a,b)
            catalyzed=all(q>=0 for q in sites) and tuple(sorted(sites)) in self.edges
            rate=self.config['rung_catalytic_rate'] if catalyzed else self.config['rung_formation_rate']
            factor=1.;delta=None
            if self.config['formation_gate']=='metropolis':
                from .transition_energy import formation_energy,formation_pairs,thermal_factor
                if fixed_pairs is None:
                    fixed_pairs=formation_pairs(self,neighbors)
                terms=formation_energy(self,a,b,neighbors,fixed_pairs);delta=sum(terms.values());factor=thermal_factor(delta,self.config['temperature'])
                stats=self.transition_stats['catalytic' if catalyzed else 'background']
                stats['proposals']+=1;stats['contact_time']+=interval;stats['weighted_time']+=interval*factor
                stats['positive_delta']+=int(delta>0);stats['sum_positive_delta']+=max(delta,0.)
                stats['max_delta']=delta if stats['max_delta'] is None else max(stats['max_delta'],delta)
                stats['min_delta']=delta if stats['min_delta'] is None else min(stats['min_delta'],delta)
            if self.rng.random()>=-np.expm1(-rate*factor*interval):continue
            self.lipids.bind(a,b);self.capture.categories[a]=self.capture.categories[b]=-1
            self.capture.release(a);self.capture.release(b)
            self.births.append(dict(time=float(time),head=a,tail=b,catalyzed=bool(catalyzed),sites=list(sites)))
            if delta is not None:
                stats['formed']+=1;self.births[-1].update(delta_U=delta,energy_factor=factor)

    def lipid_candidates(self,neighbors):
        return neighbors.pairs(self.pos,self.config['rung_capture_radius'],'HT:formation')

    def extra_forces(self,neighbors):
        self._views();force=self.capture.forces(self,ScopedNeighbors(neighbors,'HT:'))
        if self.host is not None:force[:self.prefix]+=self.host.extra_forces(ScopedNeighbors(neighbors,'F:'))
        force+=self.lipids.forces(self.pos,self.config,ScopedNeighbors(neighbors,'L:'))[0]
        return force

    def observe(self,callback,time,events):callback(time,self,events)

    def bonds(self):
        b=self.lipids.bonds();b['pairing']=[]
        if self.host is not None:
            for key,pairs in self.host.bonds().items():b.setdefault(key,[]).extend(pairs)
        b['pairing'] += [(int(self.rungs[s,1]),int(a)) for s,a in enumerate(self.capture.site_bound) if a>=0]
        return b

    def colors(self):
        return ([] if self.host is None else self.host.colors())+['#148e9c']*self.config['food_units']+['#df7947']*self.config['food_units']

    def export(self):
        result=dict(host=None if self.host is None else self.host.export(),capture=self.capture.export(),
            lipids=self.lipids.export(),births=self.births,exchanges=self.exchanges)
        if hasattr(self,'transition_stats'):result['transition_stats']=self.transition_stats
        return result

    def restore(self,state):
        self._views()
        if self.host is not None:
            rows=self.springs[(self.springs[:,0]<self.prefix)&(self.springs[:,1]<self.prefix)]
            self.host.springs=rows.copy();self.host.angles=self.angles.copy();self.host.restore(state['host'])
        self._views();self.lipids.restore(state['lipids']);self.capture.restore(self,state['capture'])
        self.births=list(state['births']);self.exchanges=list(state['exchanges']);self._mechanics()
        if 'transition_stats' in state:self.transition_stats=copy.deepcopy(state['transition_stats'])


class LipidSynthesisObserver:
    def __init__(self,config):
        self.config=config;self.times=[];self.frames=[];self.edges_frames=[];self.history=[];self.births=[]

    def __call__(self,time,c,events):
        self.times.append(float(time));self.births=list(c.births)
        if c.lipids.contact_stats is not None:self.contact_update_stats=copy.deepcopy(c.lipids.contact_stats)
        if hasattr(c,'transition_stats'):self.transition_stats=copy.deepcopy(c.transition_stats)
        self.history.append(dict(time=float(time),lipids=len(c.lipids.rungs),lateral_contacts=len(c.lipids.links),
            occupied_sites=int(np.count_nonzero(c.capture.site_bound>=0))))
        if getattr(self,'record_trajectory',True):self.frames.append(c.pos.copy())

    def summary(self):
        by_site={}
        for e in self.births:
            if e['catalyzed']:
                key=tuple(e['sites']);by_site[key]=by_site.get(key,0)+1
        result=dict(lipids_formed=len(self.births),catalyzed_lipids=sum(e['catalyzed'] for e in self.births),
            max_products_per_site_pair=max(by_site.values(),default=0),births=self.births,history=self.history,
            scope='Prepared existing F01 co-recruiter, H/T only. Same capture constants but extended ligand types. '
                'No P/R competition, expression, full-cell membrane or maintenance proof. Products use real conserved H/T atom IDs.')
        if hasattr(self,'transition_stats'):result['transition_stats']=self.transition_stats
        if hasattr(self,'contact_update_stats'):result['contact_update_stats']=self.contact_update_stats
        return result
