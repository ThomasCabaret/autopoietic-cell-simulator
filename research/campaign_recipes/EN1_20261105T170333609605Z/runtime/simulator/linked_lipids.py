"""MD2 ports on actual H--T bonds, with no prescribed tail or aggregate lookup."""
import copy
import numpy as np
from .docking import free_faces,docking_force,bound_port_force,update_faces
from .contact_exchange import exchange_faces


class LinkedLipids:
    def __init__(self):
        self.rungs={};self.links=[];self.broken_contacts=0;self.exchange_stats=None

    def bind(self,head,tail):
        head,tail=int(head),int(tail)
        occupied=set(self.rungs)|set(self.rungs.values())
        if head==tail or head in occupied or tail in occupied:raise ValueError('Axial ports already occupied or identical')
        self.rungs[head]=tail

    def layout(self):
        heads=sorted(self.rungs);lookup={h:i for i,h in enumerate(heads)}
        ids=np.asarray(heads+[self.rungs[h] for h in heads],dtype=np.int64)
        links=[(lookup[i],lookup[j],a,b) for i,j,a,b in self.links]
        return heads,ids,links

    def forces(self,pos,config,neighbors):
        heads,ids,links=self.layout();out=np.zeros_like(pos)
        if not heads:return out,0.
        packed=pos[ids];n=len(heads);partners=np.full((n,2),-1,dtype=np.int64)
        for i,j,a,b in links:partners[i,a]=j;partners[j,b]=i
        pairs=neighbors.pairs(packed[:n],1.+4*config['dock_width'],'face_force')
        force,energy=docking_force(packed,pairs,free_faces(n,links),1.,config['short_length'],
            config['dock_energy'],config['dock_width'],partners)
        bound,value=bound_port_force(packed,np.asarray(links,dtype=np.int64).reshape(-1,4),1.,
            config['short_length'],config['dock_energy'],config['dock_width'])
        # Every real atom appears once: exact gather/scatter, no movement/relabeling.
        out[ids]=force+bound
        return out,float(energy+value)

    def react(self,pos,config,rng,neighbors,interval,extra_energy=None):
        heads,ids,links=self.layout()
        if not heads:return []
        links,broken=update_faces(pos[ids],links,config,rng,neighbors,interval)
        if config.get('contact_exchange_gate','none')=='metropolis':
            if self.exchange_stats is None:
                self.exchange_stats=dict(proposals=0,accepted=0,rejected=0,positive_delta=0,sum_positive_delta=0.,sum_factor=0.,min_delta=None,max_delta=None)
            callback=None if extra_energy is None else lambda old,new:extra_energy((heads[old[0]],heads[old[1]]),(heads[new[0]],heads[new[1]]))
            links,events=exchange_faces(pos[ids],links,config,rng,neighbors,interval,callback,self.exchange_stats)
        else:links,events=exchange_faces(pos[ids],links,config,rng,neighbors,interval)
        self.links=[(heads[i],heads[j],a,b) for i,j,a,b in links];self.broken_contacts+=broken
        return [dict(removed=[heads[e['removed'][0]],heads[e['removed'][1]],*e['removed'][2:]],
            formed=[heads[e['formed'][0]],heads[e['formed'][1]],*e['formed'][2:]],port_mismatch=e['port_mismatch'],
            **{k:e[k] for k in ('delta_U','energy_factor') if k in e}) for e in events]

    def springs(self):return [(h,t,180.,.65) for h,t in sorted(self.rungs.items())]

    def bonds(self):
        return dict(scaffold=[list(q) for q in sorted(self.rungs.items())],backbone=
            [(i,j) for i,j,_,_ in self.links]+[(self.rungs[i],self.rungs[j]) for i,j,_,_ in self.links])

    def export(self):
        result=dict(rungs=sorted(self.rungs.items()),links=self.links,broken_contacts=self.broken_contacts)
        if self.exchange_stats is not None:result['exchange_stats']=copy.deepcopy(self.exchange_stats)
        return result

    def restore(self,state):
        self.rungs={};self.links=[]
        for h,t in state['rungs']:self.bind(h,t)
        occupied=set()
        for i,j,a,b in state['links']:
            if i>=j or i not in self.rungs or j not in self.rungs or a not in (0,1) or b!=1-a or (i,a) in occupied or (j,b) in occupied:
                raise ValueError('Invalid local face occupancy')
            occupied.update(((i,a),(j,b)));self.links.append((i,j,a,b))
        self.broken_contacts=int(state['broken_contacts'])
        self.exchange_stats=copy.deepcopy(state.get('exchange_stats'))
