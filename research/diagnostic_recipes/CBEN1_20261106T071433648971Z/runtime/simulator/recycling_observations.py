"""Passive current-state census and atom lifecycle, without irreversible lineage.

Initial material is included in current counts. Recycling is an event sequence
on real atom IDs, not evidence of expression, homeostasis or a new generation.
"""
from collections import Counter
import numpy as np
from .initial import groups
from .observations import components


class RecyclingObserver:
    def __init__(self, config):
        self.target=config['sequence']
        initial=set(range(len(self.target))) if config.get('template',True) and len(self.target)>1 else set()
        initial.update(q for g in groups(config) if g['backbone'] and len(g['units'])>1 for q in g['units'])
        n=len(self.target)+config['free_units']+config['function_units']
        self.polymer_atoms=initial | {n+q for q in initial}
        self.released_atoms=set();self.recycled_rungs=set();self.incorporated_lives=set()
        self.seen=0;self.counts=dict(backbone_break=0,rung_break=0,rung_form=0,backbone_form=0,
            catalyzed_formations=0,polymer_reassemblies=0,recycled_incorporations=0)
        self.history=[];self.times=[];self.frames=[];self.edges_frames=[];self.pairing_frames=[]
        self.rungs_frames=[];self.unit_bits_frames=[];self.precursor_binding_frames=[]
        self.assembly_state=None;self.last_bits=None;self.last_families=None
        self.recycle_mode=True;self.invariant_failures=0;self.last={}

    def __call__(self,time,pos,edges,pairing,bits,events,families=None):
        self.times.append(float(time));self.last_bits=bits.copy();self.last_families=families.copy()
        if getattr(self,'record_trajectory',True):
            self.frames.append(pos.copy());self.pairing_frames.append(pairing.copy())
            dense=np.zeros((len(bits),len(bits)),dtype=bool)
            for a,b in edges:dense[a,b]=dense[b,a]=True
            self.edges_frames.append(dense)

    def observe_assembly(self,c,time):
        for e in c.turnover.events[self.seen:]:
            kind=e['kind'];self.counts[kind]+=1
            if kind=='rung_break':
                s,r=e['support'],e['recognizer']
                self.released_atoms.update({s,r}&self.polymer_atoms)
                self.recycled_rungs.discard(s);self.incorporated_lives.discard(s)
            elif kind=='rung_form':
                s,r=e['support'],e['recognizer']
                self.recycled_rungs.discard(s);self.incorporated_lives.discard(s)
                if s in self.released_atoms and r in self.released_atoms:
                    self.counts['polymer_reassemblies']+=1;self.recycled_rungs.add(s)
                self.released_atoms.discard(s);self.released_atoms.discard(r)
                if e.get('catalyzed',False):self.counts['catalyzed_formations']+=1
            elif kind=='backbone_form':
                for q in (e['a'],e['b']):
                    # Actual recognizer at the event, not the later census.
                    self.polymer_atoms.update((q,e['recognizers'][str(q)]))
                    if q in self.recycled_rungs and q not in self.incorporated_lives:
                        self.counts['recycled_incorporations']+=1;self.incorporated_lives.add(q)
        self.seen=len(c.turnover.events)
        active=c.rungs[:,1]>=0;rs=c.rungs[active,1]
        valid=(len(c.pos)==2*c.n and len(rs)==len(set(map(int,rs))) and
            bool(np.all((rs>=c.n)&(rs<2*c.n))) and bool(np.isfinite(c.pos).all()))
        if valid:
            valid=bool(np.array_equal(c.bits[active],c.assembly.atom_bits[rs-c.n]))
        for a,b in c.edges:
            valid &= bool(active[a] and active[b] and c.families[a]==c.families[b])
        for a,b in enumerate(c.pairing):
            if b>=0:valid &= bool(b<c.n and c.pairing[b]==a and active[a] and active[b])
        cat=c.assembly.catalyst
        if cat is not None:
            for site,atom in enumerate(cat.site_bound):
                if atom>=0:
                    valid &= bool(active[site] and c.pairing[site]<0 and cat.atom_bound[atom]==site)
                    valid &= bool((atom<c.n and not active[atom]) or (atom>=c.n and atom not in rs))
            for atom,site in enumerate(cat.atom_bound):
                if site>=0:valid &= bool(cat.site_bound[site]==atom)
        if not valid:self.invariant_failures+=1
        lengths={'G':Counter(),'F':Counter()};targets={'G':0,'F':0};detached={'G':0,'F':0}
        for comp,order,cycle in components(c.n,c.edges):
            if not order or cycle or not all(active[q] for q in comp):continue
            family='G' if c.families[order[0]]==0 else 'F'
            lengths[family][str(len(order))]+=1
            seq=''.join(str(int(c.bits[q])) for q in order)
            if len(order)==len(comp) and seq in (self.target,self.target[::-1]):
                targets[family]+=1
                if all(c.pairing[q]<0 for q in comp):detached[family]+=1
        self.last=dict(time=float(time),active_rungs=int(active.sum()),free_P=int((~active).sum()),
            free_R=int(c.n-len(rs)),backbone_links=len(c.edges),target_chains=targets,
            detached_targets=detached,lengths={k:dict(v) for k,v in lengths.items()},
            atoms=len(c.pos),invariants_valid=bool(valid),**self.counts)
        self.history.append(dict(self.last))
        self.assembly_state=dict(atom_bits=c.assembly.atom_bits.tolist())
        if getattr(self,'record_trajectory',True):
            self.rungs_frames.append(c.rungs.copy());self.unit_bits_frames.append(c.bits.copy())
            if cat is not None:self.precursor_binding_frames.append(cat.site_bound.copy())

    def summary(self):
        return dict(observer='reversible_current_census_v1',final=self.last,history=self.history,
            invariant_failures=self.invariant_failures,**self.counts,
            limitations='Current counts include prepared material. No irreversible lineage, new expression or '
                'generation certificate. Recycling requires both real atoms previously released from polymer-derived '
                'material. Finite closed stock is not homeostasis; rates are kinetic helpers, not detailed balance.')
