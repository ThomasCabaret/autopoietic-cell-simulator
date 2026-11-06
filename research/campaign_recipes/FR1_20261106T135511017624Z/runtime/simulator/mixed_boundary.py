"""Constructed-start geometry, local segment forces, and passive diagnostics.

segment_forces and segment_energy_delta read actual axial P/R bonds and
individual L contact segments. Ring IDs/contours are never available to them.
"""
import numpy as np
from .membrane_bath import barrier_force,in_polygon,polygon_simple
from .observations import components,area


def initialize(c):
    cfg=c.config['initial_boundary'];c.initial_boundary_heads=[]
    if cfg is None:return
    packet=np.asarray(cfg['packet_box']);offset=c.box/2-packet/2+cfg['packet_offset']
    c.pos+=offset
    n=cfg['units']
    if n==0:return  # Explicit no-L control; packet placement is still identical.
    theta=np.arange(n)*2*np.pi/n
    radial=np.column_stack((np.cos(theta),np.sin(theta)))
    start=len(c.pos);radius=cfg['radius']
    c.pos=np.concatenate((c.pos,c.box/2+(radius+.325)*radial,c.box/2+(radius-.325)*radial))
    c.ligand_types=np.concatenate((c.ligand_types,np.zeros(n,dtype=np.int64),np.ones(n,dtype=np.int64)))
    c.initial_boundary_heads=list(range(start,start+n))
    for h in c.initial_boundary_heads:c.lipids.bind(h,h+n)
    for i in range(n):
        a,b=start+i,start+(i+1)%n
        c.lipids.links.append((a,b,0,1) if a<b else (b,a,1,0))
    c.lipids.links.sort()
    if np.any(c.pos<0) or np.any(c.pos>c.box):raise ValueError('Initial mixed packet/boundary leaves the world')


def segment_forces(c,neighbors):
    radius=c.config['bound_barrier_radius'];out=np.zeros_like(c.pos)
    if radius<=0 or not c.lipids.links:return out
    ids=c.host.rungs[c.host.rungs[:,1]>=0].reshape(-1)
    if not len(ids):return out
    edges=np.asarray([(a,b) for a,b,_,_ in c.lipids.links],dtype=np.int64)
    midpoint=(c.pos[edges[:,0]]+c.pos[edges[:,1]])/2
    half=.5*np.linalg.norm(c.pos[edges[:,1]]-c.pos[edges[:,0]],axis=1).max()
    ne=len(edges);points=np.concatenate((midpoint,c.pos[ids]))
    pairs=neighbors.pairs(points,half+radius,'bound_segments')
    pairs=pairs[(pairs[:,0]<ne)&(pairs[:,1]>=ne)].copy();pairs[:,1]-=ne
    return barrier_force(c.pos,edges,ids,pairs,radius,c.config['bound_barrier_stiffness'])[0]


def segment_energy_delta(c,old,new,neighbors):
    """Only changed bond segments against actually bound P/R atoms."""
    radius=c.config['bound_barrier_radius']
    if radius<=0:return 0.
    ids=c.host.rungs[c.host.rungs[:,1]>=0].reshape(-1)
    if not len(ids):return 0.
    def energy(edge,key):
        if edge is None:return 0.
        edges=np.asarray([edge],dtype=np.int64)
        midpoint=(c.pos[edge[0]]+c.pos[edge[1]])/2
        half=.5*np.linalg.norm(c.pos[edge[0]]-c.pos[edge[1]])
        points=np.vstack((midpoint,c.pos[ids]))
        pairs=neighbors.pairs(points,half+radius,key)
        pairs=pairs[(pairs[:,0]==0)&(pairs[:,1]>0)].copy();pairs[:,1]-=1
        return barrier_force(c.pos,edges,ids,pairs,radius,c.config['bound_barrier_stiffness'])[1]
    return float(energy(new,'segment_delta_new')-energy(old,'segment_delta_old'))


class BoundaryObserver:
    """Labels and contours exist here only; state is checkpoint-serializable."""
    def __init__(self):
        self.history=[];self.ever_inserted=set();self.ever_inserted_born_inside=set()
        self.residence={};self.birth_inside={};self.last_inside={};self.last_bound={}
        self.crossings={'free':0,'bound':0,'state_changed':0}

    def observe(self,time,c):
        original=set(c.initial_boundary_heads);heads=sorted(c.lipids.rungs);lookup={h:i for i,h in enumerate(heads)}
        edges={(lookup[a],lookup[b]) for a,b,_,_ in c.lipids.links};choices=[]
        initial_area=np.pi*(c.config['initial_boundary']['radius']+.325)**2
        for comp,order,cycle in components(len(heads),edges):
            real={heads[q] for q in comp}
            if not cycle or len(order)!=len(comp) or len(real&original)<.8*len(original):continue
            points=c.pos[[heads[q] for q in order]]
            value=area(points)
            if value<.5*initial_area or not polygon_simple(points):continue
            choices.append((value,real,points))
        envelope=max(choices,key=lambda q:q[0]) if choices else None
        # Birth midpoints are stored at the actual reaction time. Geometry at
        # this sample is only an enclosing witness, not an exact birth-time contour.
        for e in c.births:
            h=e['head']
            if h in self.birth_inside:continue
            contemporaneous=abs(e['time']-time)<1e-9
            self.birth_inside[h]=(bool(in_polygon(np.asarray([e['birth_midpoint']]),envelope[2])[0])
                if envelope is not None and contemporaneous else None)
        inserted=set() if envelope is None else envelope[1]-original
        inserted_inside={h for h in inserted if self.birth_inside.get(h) is True}
        span=time-self.history[-1]['time'] if self.history else 0.
        # Sampled residence: credit intervals with two matching endpoint
        # witnesses. This does not exclude an unobserved interruption inside.
        previous=set(self.history[-1]['inserted_heads']) if self.history else set()
        for h in previous&inserted:self.residence[h]=self.residence.get(h,0.)+span
        self.ever_inserted|=inserted;self.ever_inserted_born_inside|=inserted_inside
        bound=np.zeros(c.prefix,dtype=bool);bound[c.host.rungs[c.host.rungs[:,1]>=0].reshape(-1)]=True
        if envelope is not None:
            inside=in_polygon(c.pos[:c.prefix],envelope[2])
            for atom,value in enumerate(inside):
                if atom in self.last_inside and self.last_inside[atom]!=bool(value):
                    label=('bound' if bound[atom] else 'free') if self.last_bound[atom]==bool(bound[atom]) else 'state_changed'
                    self.crossings[label]+=1
            self.last_inside={i:bool(x) for i,x in enumerate(inside)}
            self.last_bound={i:bool(x) for i,x in enumerate(bound)}
        else:self.last_inside={};self.last_bound={}
        # Contact witness independent of a contour: actual edge to a prepared L.
        contacted={h for a,b,_,_ in c.lipids.links for h,other in ((a,b),(b,a)) if h not in original and other in original}
        from scipy.spatial import cKDTree
        newborn=sorted(set(heads)-original)
        distances=cKDTree(c.pos[sorted(original)]).query(c.pos[newborn])[0] if newborn else []
        self.history.append(dict(time=float(time),valid=envelope is not None,area=None if envelope is None else envelope[0],
            contour_size=0 if envelope is None else len(envelope[1]),inserted_heads=sorted(inserted),
            inserted_born_inside=sorted(inserted_inside),new_heads_touching_prepared=sorted(contacted),
            new_head_distance_to_prepared={h:float(d) for h,d in zip(newborn,distances)}))

    def summary(self):
        return dict(history=self.history,ever_inserted=sorted(self.ever_inserted),
            ever_inserted_born_inside=sorted(self.ever_inserted_born_inside),residence=self.residence,
            birth_inside=self.birth_inside,sampled_crossings=self.crossings,
            scope='Passive closed/simple contour with >=80% original heads. Birth-inside only when '
                'birth and valid contour are observed at the same time; other births unknown. '
                'Sampled residence/crossings, not continuous sealing, flux, maintenance or renewal.')


def scan_contacts(c,neighbors):
    """Passive pre-reaction face census, original/new labels only here."""
    from .docking import free_faces,port_geometry
    heads,ids,links=c.lipids.layout();n=len(heads);pos=c.pos[ids]
    original=np.isin(heads,c.initial_boundary_heads)
    pairs=neighbors.pairs(pos[:n],1.+4*c.config['dock_width'],'mixed_kinetic_contacts')
    pairs=pairs[original[pairs[:,0]]!=original[pairs[:,1]]].copy()
    if not len(pairs):return dict(encounter_pairs=0,capture_faces=0,exchange_faces=0,gated_exchange_faces=0,units=[])
    swap=~original[pairs[:,0]];pairs[swap]=pairs[swap,::-1];i,k=pairs.T
    free=free_faces(n,links);head,tail,_,_=port_geometry(pos,n,1.,c.config['short_length'])
    partners=np.full((n,2),-1,dtype=np.int64);face=np.zeros((n,2),dtype=np.int64)
    for x,y,a,b in links:partners[x,a]=y;partners[y,b]=x;face[x,a]=b;face[y,b]=a
    unlinked=np.array([y not in partners[x] for x,y in pairs])
    strain=np.maximum(abs(np.linalg.norm(pos[k]-pos[i],axis=1)-1.),
        abs(np.linalg.norm(pos[n+k]-pos[n+i],axis=1)-c.config['short_length']))<=c.config['break_extension']
    capture=exchange=gated=0
    for a in (0,1):
        b=1-a;q=np.sum((head[k,b]-head[i,a])**2,axis=1)+np.sum((tail[k,b]-tail[i,a])**2,axis=1)
        capture+=int(np.count_nonzero(unlinked&free[i,a]&free[k,b]&(q<c.config['dock_capture']**2)))
        eligible=unlinked&~free[i,a]&free[k,b]&strain&(q<c.config['contact_exchange_capture']**2)
        exchange+=int(np.count_nonzero(eligible))
        j=np.maximum(partners[i,a],0);other=1-face[i,a]
        gated+=int(np.count_nonzero(eligible&(free[j,other]|free[k,1-b])))
    return dict(encounter_pairs=len(pairs),capture_faces=capture,exchange_faces=exchange,
        gated_exchange_faces=gated,units=[heads[q] for q in np.unique(k)])
