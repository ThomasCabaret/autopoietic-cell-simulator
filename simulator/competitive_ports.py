"""Local competitive port law, optional in the shared simulation engine.

Normalize each attractive port pair by competition at both endpoints:
  p_e = -u_e/A, S_v=sum incident p_e, D_e=1+S_i+S_j-2p_e
  E=sum u_e/D_e, A=epsilon*(1-9*exp(-8)).
For one isolated pair D=1: exact historical potential and force. Each port's
sum p_e/D_e <=1 since D_e>=S_i. No global matching, aggregate or new constant.
The force derivative includes the competition terms, not just pair reweighting.
"""
import numpy as np
from numba import njit
from .docking import port_geometry, project_port_force


@njit(cache=True,nogil=True,inline='always')
def _port_score(x,cutoff):
    return (np.exp(-x)-cutoff*(9-x))/(1-9*cutoff)


@njit(cache=True,nogil=True)
def _free_scores(head,tail,pairs,free,width,partners):
    cutoff=np.exp(-8.)
    ids=np.empty((2*len(pairs),4),dtype=np.int64);scores=np.empty(2*len(pairs));count=0
    for k in range(len(pairs)):
        i,j=pairs[k]
        if partners is not None and (partners[i,0]==j or partners[i,1]==j):continue
        for a in range(2):
            b=1-a
            if not free[i,a] or not free[j,b]:continue
            hx=head[j,b,0]-head[i,a,0];hy=head[j,b,1]-head[i,a,1]
            tx=tail[j,b,0]-tail[i,a,0];ty=tail[j,b,1]-tail[i,a,1]
            q=(hx*hx+hy*hy)+(tx*tx+ty*ty);x=q/(2*width*width)
            if x>=8.:continue
            p=_port_score(x,cutoff)
            ids[count,0]=i;ids[count,1]=j;ids[count,2]=a;ids[count,3]=b
            scores[count]=p;count+=1
    return ids[:count],scores[:count]


@njit(cache=True,nogil=True)
def competitive_terms(pos,pairs,free,long,short,epsilon,width,partners=None):
    n=len(pos)//2;head,tail,_,_=port_geometry(pos,n,long,short)
    amplitude=epsilon*(1-9*np.exp(-8.))
    ids,scores=_free_scores(head,tail,pairs,free,width,partners);count=len(ids)
    total=np.zeros((n,2))
    for k in range(count):
        i,j,a,b=ids[k];p=scores[k];total[i,a]+=p;total[j,b]+=p
    denom=np.empty(count);derivative_sum=np.zeros((n,2));load=np.zeros((n,2));energy=0.
    for k in range(count):
        i,j,a,b=ids[k];p=scores[k];d=1+total[i,a]+total[j,b]-2*p;denom[k]=d
        energy-=amplitude*p/d;load[i,a]+=p/d;load[j,b]+=p/d
        derivative_sum[i,a]+=p/(d*d);derivative_sum[j,b]+=p/(d*d)
    multiplier=np.empty(count)
    for k in range(count):
        i,j,a,b=ids[k];p=scores[k];d=denom[k]
        multiplier[k]=1/d-derivative_sum[i,a]-derivative_sum[j,b]+2*p/(d*d)
    return ids,multiplier,load,energy


@njit(cache=True,nogil=True)
def _project_forces(pos,geometry,ids,multiplier,long,short,epsilon,width):
    head,tail,tangent,lengths=geometry
    n=len(head);force=np.zeros_like(pos);cutoff=np.exp(-8.)
    for k in range(len(ids)):
        i,j,a,b=ids[k];hx=head[j,b,0]-head[i,a,0];hy=head[j,b,1]-head[i,a,1]
        tx=tail[j,b,0]-tail[i,a,0];ty=tail[j,b,1]-tail[i,a,1]
        x=(hx*hx+hy*hy+tx*tx+ty*ty)/(2*width*width)
        scale=epsilon/(width*width)*(np.exp(-x)-cutoff)*multiplier[k]
        for unit,face,sign in ((i,a,1.),(j,b,-1.)):
            fx,fy,gx,gy=sign*scale*hx,sign*scale*hy,sign*scale*tx,sign*scale*ty
            project_port_force(force,unit,n+unit,face,fx,fy,gx,gy,
                               tangent[unit],lengths[unit],long,short)
    return force


@njit(cache=True,nogil=True)
def competitive_force(pos,pairs,free,long,short,epsilon,width,partners=None):
    ids,multiplier,_,energy=competitive_terms(pos,pairs,free,long,short,epsilon,width,partners)
    geometry=port_geometry(pos,len(pos)//2,long,short)
    return _project_forces(pos,geometry,ids,multiplier,long,short,epsilon,width),energy


@njit(cache=True,nogil=True)
def _products(n,ids,scores):
    products=np.ones((n,2));zeros=np.zeros((n,2),dtype=np.int64)
    for k in range(len(ids)):
        i,j,a,b=ids[k];factor=1-scores[k]
        if factor==0.:
            zeros[i,a]+=1;zeros[j,b]+=1
        else:
            products[i,a]*=factor;products[j,b]*=factor
    return products,zeros


@njit(cache=True,nogil=True,inline='always')
def _without_factor(product,zeros,factor):
    if factor==0.:
        return product if zeros==1 else 0.
    return product/factor if zeros==0 else 0.


@njit(cache=True,nogil=True)
def _saturated_energy(products,zeros,epsilon):
    energy=0.
    for i in range(len(products)):
        for a in range(2):
            energy+=1-(products[i,a] if zeros[i,a]==0 else 0.)
    return -.5*epsilon*(1-9*np.exp(-8.))*energy


@njit(cache=True,nogil=True)
def saturated_force(pos,pairs,free,long,short,epsilon,width,partners=None):
    """Per-face energy: -A/2 times one minus the product of (1-p)."""
    n=len(pos)//2;geometry=port_geometry(pos,n,long,short)
    ids,scores=_free_scores(geometry[0],geometry[1],pairs,free,width,partners)
    products,zeros=_products(n,ids,scores)
    weights=np.empty(len(ids))
    for k in range(len(ids)):
        i,j,a,b=ids[k];factor=1-scores[k]
        weights[k]=.5*(_without_factor(products[i,a],zeros[i,a],factor)+
                      _without_factor(products[j,b],zeros[j,b],factor))
    return (_project_forces(pos,geometry,ids,weights,long,short,epsilon,width),
            _saturated_energy(products,zeros,epsilon))


@njit(cache=True,nogil=True)
def local_free_delta(pos,pairs,old_free,new_free,old_partners,new_partners,changed,long,short,epsilon,width,
                     saturated=False):
    """Exact free-port delta in a bounded geometric patch.

    Competitive energies extend through two hops and read the third.
    Per-face energies change through one hop and read the second.
    """
    n=len(pos)//2;keep=np.zeros(n,dtype=np.bool_)
    for i in changed:keep[i]=True
    for _ in range(2 if saturated else 3):
        previous=keep.copy()
        for i,j in pairs:
            if previous[i] or previous[j]:keep[i]=keep[j]=True
    units=np.flatnonzero(keep);m=len(units);lookup=np.full(n,-1,dtype=np.int64)
    for k in range(m):lookup[units[k]]=k
    local=np.empty((2*m,2));before=np.empty((m,2),dtype=np.int64);after=np.empty((m,2),dtype=np.int64)
    for k in range(m):
        i=units[k];local[k]=pos[i];local[m+k]=pos[n+i]
        for face in range(2):
            a=old_partners[i,face];b=new_partners[i,face]
            before[k,face]=lookup[a] if a>=0 else -1;after[k,face]=lookup[b] if b>=0 else -1
    selected=np.empty_like(pairs);count=0
    for i,j in pairs:
        if keep[i] and keep[j]:selected[count,0]=lookup[i];selected[count,1]=lookup[j];count+=1
    selected=selected[:count]
    if saturated:
        head,tail,_,_=port_geometry(local,m,long,short)
        ids,scores=_free_scores(head,tail,selected,old_free[units],width,before)
        products,zeros=_products(m,ids,scores)
        e0=_saturated_energy(products,zeros,epsilon)
        ids,scores=_free_scores(head,tail,selected,new_free[units],width,after)
        products,zeros=_products(m,ids,scores)
        return _saturated_energy(products,zeros,epsilon)-e0
    e0=competitive_terms(local,selected,old_free[units],long,short,epsilon,width,before)[3]
    e1=competitive_terms(local,selected,new_free[units],long,short,epsilon,width,after)[3]
    return e1-e0


def partners(n,links):
    result=np.full((n,2),-1,dtype=np.int64)
    for i,j,a,b in links:result[i,a]=j;result[j,b]=i
    return result


def birth_port_base(c,neighbors):
    """Prepared lipid geometry shared until the next accepted birth."""
    from .docking import free_faces
    heads,ids,links=c.lipids.layout();n=len(heads);cfg=c.config
    packed=c.pos[ids]
    before=np.vstack((free_faces(n,links),np.array([[False,False]])));after=before.copy();after[n]=True
    bound=partners(n+1,links)
    reach=1.+4*cfg['dock_width']
    existing=neighbors.pairs(packed[:n],reach,'HT:competitive_lipid_heads')
    saturated=None
    if cfg['free_port_potential']=='saturated':
        head,tail,_,_=port_geometry(packed,n,1.,cfg['short_length'])
        ids,scores=_free_scores(head,tail,existing,before[:n],cfg['dock_width'],bound[:n])
        products,zeros=_products(n,ids,scores)
        saturated=(head,tail,np.where(zeros==0,products,0.))
    return packed,before,after,bound,existing,reach,saturated


@njit(cache=True,nogil=True)
def _saturated_birth(pose,near,head,tail,products,free,short,width,epsilon):
    new_head,new_tail,_,_=port_geometry(pose,1,1.,short)
    new_product=np.ones(2);delta=0.;cutoff=np.exp(-8.)
    for i in near:
        for a in range(2):
            if not free[i,a]:continue
            b=1-a
            hx=new_head[0,b,0]-head[i,a,0];hy=new_head[0,b,1]-head[i,a,1]
            tx=new_tail[0,b,0]-tail[i,a,0];ty=new_tail[0,b,1]-tail[i,a,1]
            x=((hx*hx+hy*hy)+(tx*tx+ty*ty))/(2*width*width)
            if x>=8.:continue
            p=_port_score(x,cutoff)
            delta+=products[i,a]*p;new_product[b]*=1-p
    return -.5*epsilon*(1-9*cutoff)*(delta+(1-new_product[0])+(1-new_product[1]))


def birth_port_delta(c,h,t,neighbors,base=None):
    """Adding two free ports also changes competition in existing pairs."""
    cfg=c.config
    packed,before,after,bound,existing,reach,saturated=(
        birth_port_base(c,neighbors) if base is None else base)
    n=len(packed)//2
    # The trial head changes at each proposal. Reuse the existing head pairs
    # and merge the trial edges in the same lexicographic order.
    distance2=np.sum((packed[:n]-c.pos[h])**2,axis=1)
    near=np.flatnonzero(distance2<reach**2)
    if saturated is not None:
        return float(_saturated_birth(c.pos[[h,t]],near,*saturated,before,
            cfg['short_length'],cfg['dock_width'],cfg['dock_energy']))
    pos=np.vstack((packed[:n],c.pos[h],packed[n:],c.pos[t]))
    trial=np.column_stack((near,np.full(len(near),n,dtype=np.int64)))
    pairs=np.insert(existing,np.searchsorted(existing[:,0],near,side='right'),trial,axis=0)
    return float(local_free_delta(pos,pairs,before,after,bound,bound,np.array([n],dtype=np.int64),
        1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width']))
