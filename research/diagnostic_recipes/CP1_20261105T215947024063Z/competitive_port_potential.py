"""CP1 static prototype, NOT installed in the simulation dynamics.

Normalize each attractive port pair by competition at both endpoints:
  p_e = -u_e/A, S_v=sum incident p_e, D_e=1+S_i+S_j-2p_e
  E=sum u_e/D_e, A=epsilon*(1-9*exp(-8)).
For one isolated pair D=1: exact historical potential and force. Each port's
sum p_e/D_e <=1 since D_e>=S_i. No global matching, aggregate or new constant.
The force derivative includes the competition terms, not just pair reweighting.
"""
import numpy as np
from numba import njit
from simulator.docking import port_geometry


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
            q=np.sum((head[j,b]-head[i,a])**2)+np.sum((tail[j,b]-tail[i,a])**2);x=q/(2*width*width)
            if x>=8.:continue
            p=(np.exp(-x)-cutoff*(9-x))/(1-9*cutoff)
            ids[count]=np.array([i,j,a,b]);scores[count]=p;count+=1;total[i,a]+=p;total[j,b]+=p
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
        i,j,a,b=ids[k];hx,hy=head[j,b]-head[i,a];tx,ty=tail[j,b]-tail[i,a]
        x=(hx*hx+hy*hy+tx*tx+ty*ty)/(2*width*width)
        scale=epsilon/(width*width)*(np.exp(-x)-cutoff)*multiplier[k]
        for unit,face,sign in ((i,a,1.),(j,b,-1.)):
            fx,fy,gx,gy=sign*scale*hx,sign*scale*hy,sign*scale*tx,sign*scale*ty;s=2*face-1
            vx=s*(long/2*fy+short/2*gy);vy=-s*(long/2*fx+short/2*gx)
            nx,ny=tangent[unit,1],-tangent[unit,0];dot=vx*nx+vy*ny
            cx,cy=(vx-dot*nx)/lengths[unit],(vy-dot*ny)/lengths[unit]
            force[unit,0]+=fx-cx;force[unit,1]+=fy-cy;force[n+unit,0]+=gx+cx;force[n+unit,1]+=gy+cy
    return force,energy
