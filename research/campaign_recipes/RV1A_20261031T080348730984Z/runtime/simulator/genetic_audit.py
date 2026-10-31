"""Read-only genetic opportunity census, independent of reaction RNG/caches.

Only the observer reads this data. Counts before a reaction tick approximate
exposure; they do not reproduce its sequential unbinding/capture/ligation order.
"""
import math
import numpy as np
from .spatial import Neighborhood
from .reference import degree,normals,local_port_free


class GeneticAudit:
    def __init__(self,state=None,window=25.):
        self.window=window;self.neighbors=Neighborhood()
        self.state=state or dict(version=1,last_time=None,last_counts={},windows={},first={},
            ticks=0,net_pairs_formed=0,net_pairs_lost=0,ligations=0,assembly=0,
            catalytic_assembly=0,pair_starts={},pair_episodes=[],max_pair_span=0.)

    def scan(self,c,time):
        n=c.n;cfg=c.config;active=c.rungs[:,1]>=0
        deg=degree(n,c.edges);nrm=np.zeros((n,2));nrm[active]=normals(c.pos,c.rungs[active])
        cat=c.assembly.catalyst if c.assembly is not None else None
        counts=dict(active_G=int(np.count_nonzero(active&(c.families==0))),
            active_F=int(np.count_nonzero(active&(c.families==1))),
            free_P=int(np.count_nonzero(~active)),free_R=int(n-active.sum()),
            paired_GF=0,paired_GG=0,occupied_precursor_sites=0,recognition_near=0,
            recognition_eligible_GF=0,recognition_eligible_GG=0,
            ligation_double_paired=0,ligation_eligible_F=0,ligation_eligible_G=0,
            precursor_capture_near=0,precursor_capture_eligible=0,
            assembly_near=0,assembly_catalytic_eligible=0)
        # Prepared identities are observer-only: never supplied to reactions.
        prepared=[q for group in c.initial_groups if group['family']==1 and group['backbone']
                  for q in group['units']]
        counts['prepared_F_sites']=len(prepared)
        counts['prepared_F_paired_sites']=int(sum(c.pairing[q]>=0 for q in prepared))
        for d in range(3):
            mask=active&(c.families==1)&(deg==d)
            counts[f'unpaired_F_degree_{d}']=int(np.count_nonzero(mask&(c.pairing<0)))
            counts[f'paired_F_degree_{d}']=int(np.count_nonzero(mask&(c.pairing>=0)))
        for i,j in enumerate(c.pairing):
            if j>i:counts['paired_GF' if c.families[i]!=c.families[j] else 'paired_GG']+=1
        if cat is not None:counts['occupied_precursor_sites']=int(np.count_nonzero(cat.site_bound>=0))
        release=c.cycle=='cycle' and time%c.period>=c.period-c.release_time
        available=np.flatnonzero(active)
        nearby=available[self.neighbors.pairs(c.pos[c.rungs[active,1]],.3,'recognizers')]
        counts['recognition_near']=len(nearby)
        def reject(prefix,reason):
            key=prefix+'_blocked_'+reason;counts[key]=counts.get(key,0)+1
        for i,j in nearby:
            if c.bits[i]!=c.bits[j]:reject('recognition','symbol');continue
            if cat is not None and (cat.site_bound[i]>=0 or cat.site_bound[j]>=0):reject('recognition','precursor');continue
            if c.pairing[i]>=0 or c.pairing[j]>=0:reject('recognition','occupied');continue
            if np.dot(nrm[i],nrm[j])>-.5:reject('recognition','orientation');continue
            if release:reject('recognition','external_release_phase');continue
            if c.families[i]==1 and c.families[j]==1:reject('recognition','FF');continue
            if c.families[i]!=c.families[j]:
                g,f=(i,j) if c.families[i]==0 else (j,i)
                key=f'recognition_GF_geometric_F_degree_{deg[f]}'
                counts[key]=counts.get(key,0)+1
                if deg[g]==0 or deg[f]>(1 if cfg.get('gf_end_capture',False) else 0):reject('recognition','family_degree');continue
            end_contact=cfg.get('gf_end_capture',False) and c.families[i]!=c.families[j]
            if cfg.get('monomer_only_capture',False) and not end_contact and not ((deg[i]>0)!=(deg[j]>0)):
                reject('recognition','monomer_gate');continue
            if cfg.get('product_cooperativity',False):
                support,incoming=(i,j) if deg[i]>0 else (j,i)
                if end_contact:support,incoming=g,f
                linked=[b if a==support else a for a,b in c.edges if a==support or b==support]
                if any(c.families[c.pairing[q]]!=c.families[incoming] for q in linked if c.pairing[q]>=0):
                    reject('recognition','cooperativity');continue
            counts['recognition_eligible_GF' if c.families[i]!=c.families[j] else 'recognition_eligible_GG']+=1
            if c.families[i]!=c.families[j]:
                key=f'recognition_eligible_GF_F_degree_{deg[f]}'
                counts[key]=counts.get(key,0)+1
        for i,j in sorted(c.edges):
            if c.families[i]!=0 or c.families[j]!=0:continue
            a,b=int(c.pairing[i]),int(c.pairing[j])
            if a<0 or b<0 or a==b:continue
            counts['ligation_double_paired']+=1
            pair=tuple(sorted((a,b)))
            if pair in c.edges:reject('ligation','already_linked');continue
            if not cfg['ligation']:reject('ligation','disabled');continue
            if c.families[a]!=c.families[b]:reject('ligation','family');continue
            d=c.pos[b]-c.pos[a];distance=np.linalg.norm(d)
            if not .72<distance<1.28:reject('ligation','distance');continue
            if np.dot(nrm[a],nrm[b])<.5:reject('ligation','orientation');continue
            if abs(np.dot(nrm[a],d))>.5*distance or abs(np.dot(nrm[b],d))>.5*distance:
                reject('ligation','skew');continue
            if not local_port_free(a,b,c.pos,c.edges,c.capacities[a]) or not local_port_free(b,a,c.pos,c.edges,c.capacities[b]):
                reject('ligation','ports');continue
            counts['ligation_eligible_F' if c.families[a] else 'ligation_eligible_G']+=1
        if c.assembly is not None:
            occupied=set(int(r) for r in c.rungs[active,1])
            for p,r in self.neighbors.pairs(c.pos,cfg['rung_capture_radius'],'assembly'):
                if p>=n or r<n or active[p] or int(r) in occupied:continue
                counts['assembly_near']+=1
                if cat is not None:
                    a,b=cat.support(p,r)
                    if a>=0 and b>=0 and tuple(sorted((a,b))) in c.edges:counts['assembly_catalytic_eligible']+=1
            if cat is not None:
                # Derive classes from actual local bonds, without refresh(c).
                owners=np.full(2*n,-1,dtype=int);categories=np.full(2*n,-1,dtype=int)
                categories[np.flatnonzero(~active)]=0;categories[n:]=1
                categories[c.rungs[active,1]]=-1
                for s in np.flatnonzero(active&(c.families==1)):owners[c.rungs[s,1]]=s
                for i,j in self.neighbors.pairs(c.pos,cfg['food_binding_radius'],'precursor'):
                    for site,atom in ((i,j),(j,i)):
                        s=owners[site]
                        if s<0 or categories[atom]<0 or c.bits[s]!=categories[atom]:continue
                        counts['precursor_capture_near']+=1
                        if c.pairing[s]<0 and cat.site_bound[s]<0 and cat.atom_bound[atom]<0:
                            counts['precursor_capture_eligible']+=1
        return counts

    def integrate(self,time):
        last=self.state['last_time']
        if last is None:return
        while last<time-1e-10:
            k=int(math.floor((last+1e-9)/self.window));end=min(time,(k+1)*self.window)
            w=self.state['windows'].setdefault(str(k),dict(start=k*self.window,end=(k+1)*self.window,observed_time=0.,exposure={}))
            span=end-last;w['observed_time']+=span
            for name,count in self.state['last_counts'].items():w['exposure'][name]=w['exposure'].get(name,0.)+span*count
            last=end

    def attach(self,c):
        g=getattr(c,'genetics',c);original=g.react
        def observed(time,dt,neighbors):
            before=self.scan(g,time);self.integrate(time)
            for name,count in before.items():
                if count>0:self.state['first'].setdefault(name,float(time))
            old={(i,int(j)) for i,j in enumerate(g.pairing) if j>i}
            old_assembly=len(g.assembly.events) if g.assembly is not None else 0
            result=original(time,dt,neighbors)
            after={(i,int(j)) for i,j in enumerate(g.pairing) if j>i}
            self.state['net_pairs_formed']+=len(after-old);self.state['net_pairs_lost']+=len(old-after)
            for pair in old-after:
                key=f'{pair[0]},{pair[1]}';start=self.state['pair_starts'].pop(key,None)
                if start is not None:
                    span=time-start;self.state['max_pair_span']=max(self.state['max_pair_span'],span)
                    self.state['pair_episodes'].append(dict(start=start,end=float(time),span=span))
            for pair in after-old:self.state['pair_starts'][f'{pair[0]},{pair[1]}']=float(time)
            self.state['ligations']+=sum('source' in e and 'formed' in e for e in result)
            if g.assembly is not None:
                events=g.assembly.events[old_assembly:];self.state['assembly']+=len(events)
                self.state['catalytic_assembly']+=sum(e.get('catalyzed',False) for e in events)
            self.state.update(last_time=float(time),last_counts=before,ticks=self.state['ticks']+1)
            return result
        g.react=observed

    def summary(self,time):
        totals={};duration=0.
        for w in self.state['windows'].values():
            duration+=w['observed_time']
            for key,value in w['exposure'].items():totals[key]=totals.get(key,0.)+value
        names=('recognition_eligible_GF','recognition_eligible_GG','ligation_eligible_F',
               'ligation_eligible_G','precursor_capture_eligible','assembly_catalytic_eligible')
        first={k:dict(time=self.state['first'].get(k,time),event=k in self.state['first'],measured=True) for k in names}
        return dict(version=1,observed_time=duration,exposure=totals,first_passages=first,
            net_pairs_formed=self.state['net_pairs_formed'],net_pairs_lost=self.state['net_pairs_lost'],
            ligations=self.state['ligations'],assembled=self.state['assembly'],catalytic_assembled=self.state['catalytic_assembly'],
            max_completed_net_pair_span=self.state['max_pair_span'],
            right_censored_pairs=[dict(start=t,span=time-t) for t in self.state['pair_starts'].values()],
            scope='Pre-reaction counts, left-held between reaction ticks; motifs may change within a tick. Exclusions sequential, not independent causes. No observer feedback or exact hazard.',state=self.state)
