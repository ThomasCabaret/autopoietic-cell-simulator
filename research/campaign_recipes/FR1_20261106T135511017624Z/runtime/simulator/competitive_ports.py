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
from .docking import port_geometry


@njit(cache=True,nogil=True)
def competitive_terms(pos,pairs,free,long,short,epsilon,width,partners=None):
    n=len(pos)//2;head,tail,_,_=port_geometry(pos,n,long,short)
    cutoff=np.exp(-8.);amplitude=epsilon*(1-9*cutoff)
    ids=np.empty((2*len(pairs),4),dtype=np.int64);scores=np.empty(2*len(pairs));count=0
    total=np.zeros((n,2))
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
            p=(np.exp(-x)-cutoff*(9-x))/(1-9*cutoff)
            ids[count,0]=i;ids[count,1]=j;ids[count,2]=a;ids[count,3]=b
            scores[count]=p;count+=1;total[i,a]+=p;total[j,b]+=p
    ids=ids[:count];scores=scores[:count];denom=np.empty(count);derivative_sum=np.zeros((n,2));load=np.zeros((n,2));energy=0.
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
def competitive_force(pos,pairs,free,long,short,epsilon,width,partners=None):
    ids,multiplier,_,energy=competitive_terms(pos,pairs,free,long,short,epsilon,width,partners)
    n=len(pos)//2;head,tail,tangent,lengths=port_geometry(pos,n,long,short);force=np.zeros_like(pos);cutoff=np.exp(-8.)
    for k in range(len(ids)):
        i,j,a,b=ids[k];hx=head[j,b,0]-head[i,a,0];hy=head[j,b,1]-head[i,a,1]
        tx=tail[j,b,0]-tail[i,a,0];ty=tail[j,b,1]-tail[i,a,1]
        x=(hx*hx+hy*hy+tx*tx+ty*ty)/(2*width*width)
        scale=epsilon/(width*width)*(np.exp(-x)-cutoff)*multiplier[k]
        for unit,face,sign in ((i,a,1.),(j,b,-1.)):
            fx,fy,gx,gy=sign*scale*hx,sign*scale*hy,sign*scale*tx,sign*scale*ty;s=2*face-1
            vx=s*(long/2*fy+short/2*gy);vy=-s*(long/2*fx+short/2*gx)
            nx,ny=tangent[unit,1],-tangent[unit,0];dot=vx*nx+vy*ny
            cx,cy=(vx-dot*nx)/lengths[unit],(vy-dot*ny)/lengths[unit]
            force[unit,0]+=fx-cx;force[unit,1]+=fy-cy;force[n+unit,0]+=gx+cx;force[n+unit,1]+=gy+cy
    return force,energy


@njit(cache=True,nogil=True)
def local_free_delta(pos,pairs,old_free,new_free,old_partners,new_partners,changed,long,short,epsilon,width):
    """Exact competitive delta in a patch of at most3 geometric contact hops.

    Changed energies extend through2 hops; endpoint partitions need the third.
    Global pair indices are a spatial index only, no global energy is evaluated.
    """
    n=len(pos)//2;keep=np.zeros(n,dtype=np.bool_)
    for i in changed:keep[i]=True
    for _ in range(3):
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
    e0=competitive_terms(local,selected,old_free[units],long,short,epsilon,width,before)[3]
    e1=competitive_terms(local,selected,new_free[units],long,short,epsilon,width,after)[3]
    return e1-e0


def partners(n,links):
    result=np.full((n,2),-1,dtype=np.int64)
    for i,j,a,b in links:result[i,a]=j;result[j,b]=i
    return result


def birth_port_delta(c,h,t,neighbors):
    """Adding two free ports also changes competition in existing pairs."""
    from .docking import free_faces
    heads,_,links=c.lipids.layout();n=len(heads);cfg=c.config
    pos=c.pos[heads+[h]+[c.lipids.rungs[q] for q in heads]+[t]]
    before=np.vstack((free_faces(n,links),np.array([[False,False]])));after=before.copy();after[n]=True
    bound=partners(n+1,links)
    pairs=neighbors.pairs(pos[:n+1],1.+4*cfg['dock_width'],'HT:competitive_delta')
    return float(local_free_delta(pos,pairs,before,after,bound,bound,np.array([n],dtype=np.int64),
        1.,cfg['short_length'],cfg['dock_energy'],cfg['dock_width']))
