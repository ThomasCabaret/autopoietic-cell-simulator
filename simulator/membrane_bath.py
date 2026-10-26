"""Prepared large boundary and diagnostic probes using bounded local laws.

Radius, original IDs and inside/outside placements are constructor/observer
data only. Reactions reuse the V8 face contact; no insertion operation exists.
"""
import math
import numpy as np
from numba import njit
from .membrane import MembraneChemistry
from .docking import update_faces,docking_force
from .config import MEMBRANE_DEFAULTS
from .observations import components,area
from .contact_exchange import exchange_faces

DEFAULTS=dict(MEMBRANE_DEFAULTS,units=243,ring_units=219,ring_radius=34.5,
    initial='ring',box=[90.,90.],face_docking=True,short_length=.98,
    temperature=.08,dock_width=.3,bond_off_rate=.02,
    free_lipid_start='inside_annulus',retained_probes=24,permeable_probes=24,
    barrier_radius=.55,barrier_stiffness=80.,initial_jitter=.015,
    contact_exchange_rate=0.,contact_exchange_capture=.8)


@njit(cache=True,nogil=True)
def barrier_force(pos,edges,probe_ids,candidates,radius,stiffness):
    """Repulsion from one actual bond segment: endpoints + probe, three atoms."""
    force=np.zeros_like(pos);energy=0.
    for ei,pi in candidates:
        a,b=edges[ei];p=probe_ids[pi]
        dx,dy=pos[b,0]-pos[a,0],pos[b,1]-pos[a,1]
        wx,wy=pos[p,0]-pos[a,0],pos[p,1]-pos[a,1]
        t=min(1.,max(0.,(wx*dx+wy*dy)/max(dx*dx+dy*dy,1e-16)))
        qx,qy=wx-t*dx,wy-t*dy;distance=np.sqrt(qx*qx+qy*qy)
        overlap=max(radius-distance,0.)
        if overlap==0.:continue
        energy+=.5*stiffness*overlap*overlap
        scale=stiffness*overlap/max(distance,1e-10)
        fx,fy=scale*qx,scale*qy
        force[p,0]+=fx;force[p,1]+=fy
        force[a,0]-=(1-t)*fx;force[a,1]-=(1-t)*fy
        force[b,0]-=t*fx;force[b,1]-=t*fy
    return force,energy


@njit(cache=True,nogil=True)
def polygon_simple(points):
    n=len(points)
    for i in range(n):
        a=points[i];b=points[(i+1)%n]
        for j in range(i+2,n):
            if i==0 and j==n-1:continue
            c=points[j];d=points[(j+1)%n]
            x1=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
            x2=(b[0]-a[0])*(d[1]-a[1])-(b[1]-a[1])*(d[0]-a[0])
            y1=(d[0]-c[0])*(a[1]-c[1])-(d[1]-c[1])*(a[0]-c[0])
            y2=(d[0]-c[0])*(b[1]-c[1])-(d[1]-c[1])*(b[0]-c[0])
            if x1*x2<0. and y1*y2<0.:return False
    return True


@njit(cache=True,nogil=True)
def in_polygon(points,polygon):
    result=np.zeros(len(points),dtype=np.bool_)
    for k in range(len(points)):
        x,y=points[k];inside=False
        for i in range(len(polygon)):
            ax,ay=polygon[i];bx,by=polygon[(i+1)%len(polygon)]
            if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:inside=not inside
        result[k]=inside
    return result


class MembraneBathChemistry(MembraneChemistry):
    def __init__(self,config,rng):
        # Reuse all local mechanics. Discarded parent initialization is not a
        # trajectory and performs no chemical transitions.
        base=dict(config,initial='dispersed_units',fragment_size=1)
        super().__init__(base,rng);self.config=config
        n=self.n;m=config['ring_units'];R=config['ring_radius'];center=self.box/2
        theta=np.arange(m)*2*np.pi/m;radial=np.column_stack((np.cos(theta),np.sin(theta)))
        self.pos[:m]=(R+self.shaft/2)*radial+center
        self.pos[n:n+m]=(R-self.shaft/2)*radial+center
        for i in range(m,n):
            for _ in range(20000):
                mode=config['free_lipid_start']
                lo,hi=(R-4.,R-2.) if mode=='inside_annulus' else ((R+2.,R+4.) if mode=='outside_annulus' else (0.,R-2.))
                r=np.sqrt(rng.uniform(lo*lo,hi*hi));t=rng.uniform(0,2*np.pi)
                midpoint=center+r*np.array([np.cos(t),np.sin(t)])
                t=rng.uniform(0,2*np.pi);v=self.shaft/2*np.array([np.cos(t),np.sin(t)])
                h,tail=midpoint+v,midpoint-v
                previous=np.concatenate((self.pos[:i],self.pos[n:n+i]))
                if min(np.linalg.norm(previous-h,axis=1).min(),np.linalg.norm(previous-tail,axis=1).min())>.42:
                    self.pos[i]=h;self.pos[n+i]=tail;break
            else:raise RuntimeError('Free lipid initial packing jam')
        self.pos+=rng.normal(scale=config['initial_jitter'],size=self.pos.shape)
        links=[]
        for i in range(m):
            j=(i+1)%m
            links.append((i,j,0,1) if i<j else (j,i,1,0))
        self.face_links=sorted(links)
        contacts={(i,j) for i,j,a,b in links};self.edges=[contacts.copy(),contacts.copy()]
        self.broken_contacts=0;self._face_mechanics()
        counts=(config['retained_probes'],config['permeable_probes']);probes=[]
        for kind,count in enumerate(counts):
            lo,hi=(R-3.,R-1.2) if kind==0 else (R+1.2,R+3.)
            radii=np.sqrt(rng.uniform(lo*lo,hi*hi,count));angles=rng.uniform(0,2*np.pi,count)
            probes.append(center+radii[:,None]*np.column_stack((np.cos(angles),np.sin(angles))))
        self.pos=np.concatenate((self.pos,*probes))
        self.kinds=np.concatenate((np.zeros(2*n,dtype=np.int64),np.ones(counts[0],dtype=np.int64),np.full(counts[1],2,dtype=np.int64)))
        r=config['barrier_radius'];self.contact=np.array([[.4,r,0.],[r,0.,0.],[0.,0.,0.]])
        self.probe_ids=np.arange(2*n,2*n+counts[0],dtype=np.int64)
        self.exchange_events=[]

    def react(self,time,dt,neighbors):
        self.face_links,broken=update_faces(self.pos[:2*self.n],self.face_links,self.config,self.rng,neighbors,dt*5)
        if self.config['contact_exchange_rate']>0:
            self.face_links,events=exchange_faces(self.pos[:2*self.n],self.face_links,self.config,self.rng,neighbors,dt*5)
            self.exchange_events.extend(dict(time=float(time),**e) for e in events)
        self.broken_contacts+=broken
        contacts={(i,j) for i,j,a,b in self.face_links};self.edges=[contacts.copy(),contacts.copy()]
        self._face_mechanics();return []

    def extra_forces(self,neighbors):
        force=np.zeros_like(self.pos);n=self.n
        if self.config['dock_energy']:
            pairs=neighbors.pairs(self.pos[:n],self.long+4*self.config['dock_width'],'face_force')
            force[:2*n]+=docking_force(self.pos[:2*n],pairs,self.faces_free,self.long,self.short,
                self.config['dock_energy'],self.config['dock_width'],self.face_partners)[0]
        if self.config['barrier_radius']>0 and len(self.probe_ids) and self.edges[0]:
            edges=np.array(sorted(self.edges[0]),dtype=np.int64)
            midpoint=(self.pos[edges[:,0]]+self.pos[edges[:,1]])/2
            half=.5*np.linalg.norm(self.pos[edges[:,1]]-self.pos[edges[:,0]],axis=1).max()
            # Global max bounds only the spatial search; individual forces use
            # the local segment distance, never a contour or desired radius.
            points=np.concatenate((midpoint,self.pos[self.probe_ids]));ne=len(edges)
            pairs=neighbors.pairs(points,half+self.config['barrier_radius'],'probe_segments')
            pairs=pairs[(pairs[:,0]<ne)&(pairs[:,1]>=ne)].copy();pairs[:,1]-=ne
            force+=barrier_force(self.pos,edges,self.probe_ids,pairs,
                self.config['barrier_radius'],self.config['barrier_stiffness'])[0]
        return force

    def observe(self,callback,time,events):
        if self.config['contact_exchange_rate']>0:callback(time,self.pos,self.edges,self.face_links,self.exchange_events)
        else:callback(time,self.pos,self.edges,self.face_links)

    def export(self):
        state=super().export()
        if self.config['contact_exchange_rate']>0:state['exchange_events']=self.exchange_events
        return state

    def restore(self,state):
        super().restore(state);self.exchange_events=list(state.get('exchange_events',[]))

    def colors(self):
        return super().colors()+['#9a4aa0']*self.config['retained_probes']+['#d4af37']*self.config['permeable_probes']


class MembraneBathObserver:
    """All aggregate membership and inside/outside tests are analysis only."""
    def __init__(self,config):
        self.n=config['units'];self.ring=config['ring_units'];self.nr=config['retained_probes'];self.np=config['permeable_probes']
        self.frames=[];self.times=[];self.edges_frames=[];self.face_link_frames=[];self.history=[]
        self.initial_area=None;self.escaped=set();self.entered=set();self.inserted=set()
        self.last_inserted=set();self.spans={};self.max_spans={}
        self.exchange_events=None

    def __call__(self,time,pos,edges,links,exchange_events=None):
        if exchange_events is not None:self.exchange_events=list(exchange_events)
        if self.initial_area is None:self.initial_area=area(pos[:self.ring])
        candidates=[]
        for comp,order,cycle in components(self.n,edges[0]):
            if len(comp & set(range(self.ring)))<.8*self.ring or len(order)<3:continue
            p=pos[order];a=area(p)
            # A long invented chord would misclassify probes in a missing arc.
            # Open paths provide an analysis envelope only across a small gap.
            if not cycle and np.linalg.norm(p[-1]-p[0])>2.5:continue
            if a<.5*self.initial_area or not polygon_simple(p):continue
            matching=cycle and all(tuple(sorted((order[q],order[(q+1)%len(order)]))) in edges[1] for q in range(len(order)))
            candidates.append((a,order,matching))
        closed=False;valid=False;current=set();a=None;inside_ret=None
        if candidates:
            a,order,closed=max(candidates,key=lambda x:x[0]);valid=True
            mask=in_polygon(pos[2*self.n:],pos[order]);inside_ret=int(mask[:self.nr].sum())
            self.escaped.update(int(i) for i in np.flatnonzero(~mask[:self.nr]))
            self.entered.update(int(i) for i in np.flatnonzero(mask[self.nr:]))
            if closed:current={i for i in order if i>=self.ring};self.inserted.update(current)
        dt=time-self.times[-1] if self.times else 0.
        for i in current:
            self.spans[i]=self.spans.get(i,0.)+dt if i in self.last_inserted else 0.
            self.max_spans[i]=max(self.max_spans.get(i,0.),self.spans[i])
        self.last_inserted=current
        self.times.append(time)
        if getattr(self,'record_trajectory',True):
            self.frames.append(pos.copy());mat=np.full((self.n,4),-1,dtype=np.int32)
            if links:mat[:len(links)]=np.asarray(links,dtype=np.int32)
            self.face_link_frames.append(mat)
        self.history.append(dict(time=time,parent_closed=bool(closed),envelope_valid=valid,parent_area=a,
            inserted_now=sorted(current),retained_inside=inside_ret,retained_escaped=len(self.escaped),permeable_entered=len(self.entered),contacts=len(links)))

    def summary(self):
        valid=sum(x['envelope_valid'] for x in self.history)
        result=dict(parent_closed_fraction=sum(x['parent_closed'] for x in self.history)/max(len(self.history),1),
            envelope_valid_fraction=valid/max(len(self.history),1),final_parent_closed=self.history[-1]['parent_closed'],
            final_parent_area=self.history[-1]['parent_area'],initial_area=self.initial_area,
            inserted_into_closed_parent_ever=len(self.inserted),inserted_ids=sorted(self.inserted),
            persistent_inserted_10=sum(t>=10. for t in self.max_spans.values()),sampled_insertion_spans=self.max_spans,
            retained_escape_fraction=len(self.escaped)/self.nr if self.nr and valid else None,
            permeable_entry_fraction=len(self.entered)/self.np if self.np and valid else None,
            escaped_probe_ids=sorted(self.escaped),entered_probe_ids=sorted(self.entered),history=self.history,
            envelope_definition='Simple original-parent path; virtual closure only across endpoint gap<=2.5; larger fragmented envelopes are unknown, never physical walls',
            persistence_definition='Consecutive sampled closed-parent membership for10 time units; unresolved openings between samples possible')
        if self.exchange_events is not None:result.update(contact_exchanges=len(self.exchange_events),exchange_events=self.exchange_events)
        return result
