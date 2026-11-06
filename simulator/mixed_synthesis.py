"""P/R and H/T share real saturable F sites in one continuous particle bath.

No functional aggregate is read by reactions. CopyChemistry owns genetic
bonds, LinkedLipids owns actual H/T partners, and one PrecursorCapture owns
all ligands. The adapter prevents duplicate capture springs/forces/reactions.
"""
import copy
import numpy as np
from .copy import CopyChemistry
from .precursors import PrecursorCapture,capture_stiffness
from .lipid_synthesis import LipidSynthesisChemistry,LipidSynthesisObserver,DEFAULTS as LIPID_DEFAULTS
from .linked_lipids import LinkedLipids
from .coupled_bath import ScopedNeighbors
from .observations import make_copy_observer

SHARED=('temperature','box','rung_capture_radius','rung_formation_rate','rung_catalytic_rate',
    'food_binding_radius','food_binding_rate','food_unbinding_rate','food_ligand_energy',
    'food_ligand_width','food_activation','capture_curvature')
DEFAULTS={k:v for k,v in LIPID_DEFAULTS.items() if k not in ('tool_count','tool_linked','tool_pose')}
DEFAULTS.update(genetics={},lipid_capture=True,capture_cooperativity=False,
    initial_boundary=None,bound_barrier_radius=0.,bound_barrier_stiffness=80.)


def genetics_config(config):
    from .config import resolve
    return resolve(dict(schema_version=1,model='copy',chemistry={**config['genetics'],
        **{k:config[k] for k in SHARED}}))['chemistry']


class MixedCapture(PrecursorCapture):
    def __init__(self,c):
        self.stiffness=capture_stiffness(c.config)
        self.site_bound=np.full(c.n,-1,dtype=np.int64)
        self.atom_bound=np.full(len(c.pos),-1,dtype=np.int64);self.refresh(c)

    def refresh(self,c):
        c._views();g=c.host;active=g.rungs[:,1]>=0
        self.owners=np.full(len(c.pos),-1,dtype=np.int64)
        sites=np.flatnonzero(active & (g.families==1))
        self.owners[g.rungs[sites,1]]=sites
        self.categories=np.full(len(c.pos),-1,dtype=np.int64)
        self.categories[np.flatnonzero(~active)]=0
        self.categories[g.n:c.prefix]=1
        self.categories[g.rungs[active,1]]=-1
        if c.config['lipid_capture']:self.categories[c.prefix:]=c.ligand_types[c.prefix:]
        if c.lipids.rungs:
            self.categories[list(c.lipids.rungs)]=-1;self.categories[list(c.lipids.rungs.values())]=-1
        self.activity=np.ones(c.n)
        if c.config['food_activation']:
            self.activity[:]=.1/35.
            for i,j in g.edges:self.activity[i]=self.activity[j]=1.
        if c.config['capture_cooperativity']:
            self.bond_neighbors=[[] for _ in range(c.n)]
            for i,j in c.edges:self.bond_neighbors[i].append(j);self.bond_neighbors[j].append(i)
            self.material_group=(c.ligand_types>=0).astype(np.int64)
            self.allowed_groups=np.ones((c.n,2),dtype=bool)
            for s,adjacent in enumerate(self.bond_neighbors):
                for other in adjacent:
                    atom=int(self.site_bound[other])
                    if atom>=0:
                        self.allowed_groups[s]&=((np.arange(2)==self.material_group[atom]) &
                            (c.bits[s]!=self.categories[atom]))

    def binding_allowed(self,c,site,atom,released=()):
        if not c.config['capture_cooperativity']:return True
        for neighbor in self.bond_neighbors[site]:
            other=int(self.site_bound[neighbor])
            if other<0 or neighbor in released:continue
            if self.material_group[atom]!=self.material_group[other] or self.categories[atom]==self.categories[other]:return False
        return True

    def affected_sites(self,c,released):
        if not c.config['capture_cooperativity']:return released
        return set(released)|{q for s in released for q in self.bond_neighbors[s]}

    def force_pairs(self,c,neighbors):
        pairs=super().force_pairs(c,neighbors)
        if not c.config['capture_cooperativity'] or not len(pairs):return pairs
        keep=np.zeros(len(pairs),dtype=bool)
        for a,b in ((pairs[:,0],pairs[:,1]),(pairs[:,1],pairs[:,0])):
            owners=self.owners[a]
            keep|=(owners>=0)&(self.categories[b]>=0)&self.allowed_groups[np.maximum(owners,0),self.material_group[b]]
        return pairs[keep]


class GeneticCaptureView:
    """Global IDs match the genetic prefix; host mechanics excludes this field."""
    def __init__(self,world):self.world=world
    @property
    def site_bound(self):return self.world.capture.site_bound
    @property
    def atom_bound(self):return self.world.capture.atom_bound
    def refresh(self,c):self.world.capture.refresh(self.world)
    def react(self,c,dt,neighbors):
        self.world.capture.react(self.world,dt,ScopedNeighbors(self.world.reaction_neighbors,'shared:'))
    def support(self,p,r):return self.world.capture.support(p,r)
    def release(self,atom):self.world.capture.release(atom)
    def springs(self,c):return []
    def forces(self,c,neighbors):return np.zeros_like(c.pos)
    def export(self):return self.world.capture.export()
    def restore(self,c,state):self.world.capture.restore(self.world,state)


class MixedSynthesisChemistry(LipidSynthesisChemistry):
    def __init__(self,config,rng):
        self.config,self.rng=config,rng;self.box=np.asarray(config['box'],dtype=float)
        initial=genetics_config(config);boundary=config['initial_boundary']
        packet=self.box if boundary is None else np.asarray(boundary['packet_box'],dtype=float)
        initial['box']=packet.tolist()
        self.host=CopyChemistry(initial,rng);self.host.config['box']=self.box.tolist();self.host.box=self.box
        self.prefix=len(self.host.pos)
        count=config['food_units'];food=rng.uniform([.6,.6],packet-.6,size=(2*count,2))
        self.pos=np.concatenate((self.host.pos.copy(),food));self.lipids=LinkedLipids()
        self.births=[];self.exchanges=[];self.ligand_types=np.full(len(self.pos),-1,dtype=np.int64)
        self.ligand_types[self.prefix:self.prefix+count]=0;self.ligand_types[self.prefix+count:]=1
        from .mixed_boundary import initialize
        initialize(self)
        from .lipid_synthesis import initialize_lipids
        initialize_lipids(self)
        self._views();self.capture=MixedCapture(self)
        self.host.assembly.catalyst=GeneticCaptureView(self)
        r=config['tool_lipid_contact']
        self.contact=np.array([[.7,.28,0.,r],[.28,0.,0.,r],[0.,0.,.4,.4],[r,r,.4,.4]])
        if config['formation_gate']=='metropolis':
            self.transition_stats={k:dict(proposals=0,contact_time=0.,weighted_time=0.,positive_delta=0,
                sum_positive_delta=0.,max_delta=None,min_delta=None,formed=0) for k in ('background','catalytic')}
        self.mobility=np.concatenate((np.full(self.prefix,.25),np.full(len(self.pos)-self.prefix,.4)))[:,None]
        self._mechanics()

    def _views(self):
        g=self.host;g.pos=self.pos[:self.prefix]
        self.n=g.n;self.rungs=g.rungs;self.bits=g.bits;self.edges=g.edges;self.pairing=g.pairing

    def react(self,time,dt,neighbors):
        self.reaction_neighbors=neighbors;self._views()
        # The host adapter reacts the global capture once, before P/R formation.
        events=self.host.react(time,dt,ScopedNeighbors(neighbors,'PR:'))
        self._views();self.capture.refresh(self);self._mechanics()
        before=len(self.births);self.form_lipids(time,dt*5,neighbors)
        self.observation_due=self.config['initial_boundary'] is not None and len(self.births)>before
        if self.observation_due:
            for e in self.births[before:]:e['birth_midpoint']=((self.pos[e['head']]+self.pos[e['tail']])/2).tolist()
        if self.config['capture_cooperativity']:self.capture.refresh(self)
        extra_energy=None
        if (self.config['contact_exchange_gate']=='metropolis' or self.config['contact_update_gate']=='metropolis') and self.config['bound_barrier_radius']>0:
            from .mixed_boundary import segment_energy_delta
            extra_energy=lambda old,new:segment_energy_delta(self,old,new,ScopedNeighbors(neighbors,'L:exchange:'))
        self.exchanges.extend(dict(time=float(time),**e) for e in self.lipids.react(
            self.pos,self.config,self.rng,ScopedNeighbors(neighbors,'L:'),dt*5,extra_energy))
        self._mechanics();return events

    def extra_forces(self,neighbors):
        self._views();force=self.capture.forces(self,ScopedNeighbors(neighbors,'shared:'))
        force[:self.prefix]+=self.host.extra_forces(ScopedNeighbors(neighbors,'PR:'))
        force+=self.lipids.forces(self.pos,self.config,ScopedNeighbors(neighbors,'L:'))[0]
        if self.config['bound_barrier_radius']>0:
            from .mixed_boundary import segment_forces
            force+=segment_forces(self,ScopedNeighbors(neighbors,'L:'))
        return force

    def lipid_candidates(self,neighbors):
        if not self.config['food_units']:return np.empty((0,2),dtype=np.int64)
        pairs=super().lipid_candidates(neighbors)
        types=self.ligand_types
        return pairs[((types[pairs[:,0]]==0)&(types[pairs[:,1]]==1))|
            ((types[pairs[:,0]]==1)&(types[pairs[:,1]]==0))]

    def bonds(self):
        # Host bonds already include the one global capture through the facade.
        result={k:list(v) for k,v in self.host.bonds().items()}
        for k,v in self.lipids.bonds().items():result.setdefault(k,[]).extend(v)
        return result

    def export(self):
        state=super().export()
        state.update(host_springs=self.host.springs.tolist(),host_angles=self.host.angles.tolist())
        return state

    def colors(self):
        colors=super().colors()
        n=len(self.initial_boundary_heads)
        return colors+['#148e9c']*n+['#df7947']*n

    def restore(self,state):
        self._views();self.host.springs=np.asarray(state['host_springs'],dtype=float).reshape(-1,4)
        self.host.angles=np.asarray(state['host_angles'],dtype=float).reshape(-1,5)
        self.host.restore(state['host']);self._views();self.lipids.restore(state['lipids'])
        self.capture.restore(self,state['capture']);self.births=list(state['births']);self.exchanges=list(state['exchanges'])
        if 'transition_stats' in state:self.transition_stats=copy.deepcopy(state['transition_stats'])
        self._mechanics()


class MixedSynthesisObserver(LipidSynthesisObserver):
    def __init__(self,config):
        super().__init__(config);self.genetic_state=None;self.used_lipids=set();self.invariant_failures=0
        self.boundary_state=None

    def genetic_observer(self):
        cfg={**genetics_config(self.config),'case':self.config['case'],'seed':self.config['seed']}
        obj=make_copy_observer(cfg);obj.record_trajectory=False
        if self.genetic_state is not None:obj.__dict__.update(self.genetic_state)
        return obj

    def __call__(self,time,c,events):
        occupied=[(s,int(a)) for s,a in enumerate(c.capture.site_bound) if a>=0]
        axial=[int(r) for r in c.host.rungs[:,1] if r>=0]
        heads=list(c.lipids.rungs);tails=list(c.lipids.rungs.values());count=c.config['food_units']
        faces=[(a,x) for a,b,x,y in c.lipids.links]+[(b,y) for a,b,x,y in c.lipids.links]
        valid=(len(c.pos)==c.prefix+2*count+2*len(c.initial_boundary_heads) and len(axial)==len(set(axial)) and
            all(c.prefix<=h<len(c.pos) and c.ligand_types[h]==0 for h in heads) and
            all(c.prefix<=t<len(c.pos) and c.ligand_types[t]==1 for t in tails) and len(tails)==len(set(tails)) and
            len(faces)==len(set(faces)) and all(a in c.lipids.rungs and b in c.lipids.rungs and a<b and x in (0,1) and y==1-x for a,b,x,y in c.lipids.links) and
            len(occupied)==len({a for _,a in occupied}) and
            all(c.capture.atom_bound[a]==s for s,a in occupied) and
            all(c.capture.site_bound[s]==a for a,s in enumerate(c.capture.atom_bound) if s>=0))
        self.invariant_failures+=int(not valid)
        g=self.genetic_observer();prior=g.assembly_prior_tools
        for e in c.births[len(self.births):]:
            matches=[(chain,kind) for chain,kind in prior.items() if e['catalyzed'] and set(e['sites'])<=set(chain)]
            chain,kind=matches[0] if len(matches)==1 else (None,None)
            self.births.append(dict(e,chain=list(chain) if chain else None,chain_kind=kind))
        c.host.observe(g,time,events);self.genetic_state=g.__dict__
        born={e['head']:e['time'] for e in self.births}
        for i,j,_,_ in c.lipids.links:
            self.used_lipids.update(h for h in (i,j) if born.get(h,time)<time)
        self.times.append(float(time))
        if hasattr(c,'transition_stats'):self.transition_stats=copy.deepcopy(c.transition_stats)
        occupied=[int(a) for a in c.capture.site_bound if a>=0]
        wrong=0;double=0
        for i,j in c.edges:
            a,b=int(c.capture.site_bound[i]),int(c.capture.site_bound[j])
            if a<0 or b<0:continue
            double+=1;wrong+=int((a<c.prefix)!=(b<c.prefix))
        self.history.append(dict(time=float(time),lipids=len(c.lipids.rungs),lateral_contacts=len(c.lipids.links),
            occupied_sites=len(occupied),genetic_ligands=sum(a<c.prefix for a in occupied),
            lipid_ligands=sum(a>=c.prefix for a in occupied),double_occupied_edges=double,wrong_double_edges=wrong))
        if c.initial_boundary_heads:
            from .mixed_boundary import BoundaryObserver
            observer=BoundaryObserver()
            if self.boundary_state is not None:observer.__dict__.update(self.boundary_state)
            observer.observe(time,c);self.boundary_state=observer.__dict__
        if c.lipids.exchange_stats is not None:self.exchange_gate_stats=copy.deepcopy(c.lipids.exchange_stats)
        if c.lipids.contact_stats is not None:self.contact_update_stats=copy.deepcopy(c.lipids.contact_stats)
        if getattr(self,'record_trajectory',True):self.frames.append(c.pos.copy())

    def summary(self):
        result=super().summary();g=self.genetic_observer().summary()
        births={int(e['support']):e['time'] for e in g.get('assembly_state',{}).get('events',[])}
        whole=[e for e in self.births if e['chain_kind']=='expressed' and e['chain'] and
            all(q in births and births[q]<e['time'] for q in e['chain'])]
        result.update(genetics=g,lipids_from_expressed_F=sum(e['chain_kind']=='expressed' for e in self.births),
            lipids_from_whole_food_F=len(whole),whole_food_F_active_on_lipids=len({tuple(e['chain']) for e in whole}),
            new_lipids_later_contacted=len(self.used_lipids),atom_port_invariant_failures=self.invariant_failures,
            scope='One shared capture pool P/R/H/T; actual products and conserved atom IDs. Prepared short G/F, '
                'finite stocks, no cell membrane, losses, open feed or homeostasis. H/T local energy gate optional; '
                'P/R formation retains its historical helper. Tool provenance uses prior passive observations only; may undercount.')
        if self.boundary_state is not None:
            from .mixed_boundary import BoundaryObserver
            observer=BoundaryObserver();observer.__dict__.update(self.boundary_state);result['boundary']=observer.summary()
            result['scope']='Constructed L boundary and shared P/R/H/T capture, actual products; finite stocks, no losses/open feed/homeostasis. P/R helper and external release cycle retained.'
        if hasattr(self,'exchange_gate_stats'):result['exchange_gate_stats']=self.exchange_gate_stats
        if hasattr(self,'contact_update_stats'):result['contact_update_stats']=self.contact_update_stats
        return result
