"""A bounded four-bead contact: coincident head AND tail ports cooperate.

The two rows have different port spacing; no preferred aggregate angle, ring
size, chain identity or component query is used by this interaction.
"""
import numpy as np
from numba import njit


@njit(cache=True, nogil=True)
def port_geometry(pos,n,long,short):
    head=np.empty((n,2,2)); tail=np.empty((n,2,2))
    tangent=np.empty((n,2)); lengths=np.empty(n)
    for i in range(n):
        ux=pos[n+i,0]-pos[i,0]; uy=pos[n+i,1]-pos[i,1]
        r=max(np.sqrt(ux*ux+uy*uy),1e-8)
        tx,ty=-uy/r,ux/r
        tangent[i,0]=tx; tangent[i,1]=ty; lengths[i]=r
        for face in range(2):
            s=2*face-1
            head[i,face,0]=pos[i,0]+s*long/2*tx
            head[i,face,1]=pos[i,1]+s*long/2*ty
            tail[i,face,0]=pos[n+i,0]+s*short/2*tx
            tail[i,face,1]=pos[n+i,1]+s*short/2*ty
    return head,tail,tangent,lengths


@njit(cache=True, nogil=True)
def docking_force(pos,pairs,free,long,short,epsilon,width,partners=None):
    n=len(pos)//2
    head,tail,tangent,lengths=port_geometry(pos,n,long,short)
    force=np.zeros_like(pos); energy=0.
    cutoff=np.exp(-8.)
    for q in range(len(pairs)):
        i,j=pairs[q,0],pairs[q,1]
        if partners is not None and (partners[i,0]==j or partners[i,1]==j): continue
        for a in range(2):
            b=1-a
            if not free[i,a] or not free[j,b]: continue
            hx=head[j,b,0]-head[i,a,0]; hy=head[j,b,1]-head[i,a,1]
            tx=tail[j,b,0]-tail[i,a,0]; ty=tail[j,b,1]-tail[i,a,1]
            x=(hx*hx+hy*hy+tx*tx+ty*ty)/(2*width*width)
            if x>=8.: continue
            e=np.exp(-x)
            energy-=epsilon*(e-cutoff*(9.-x))
            scale=epsilon/(width*width)*(e-cutoff)
            fhx,fhy,ftx,fty=scale*hx,scale*hy,scale*tx,scale*ty
            for unit,face,sign in ((i,a,1.),(j,b,-1.)):
                fx,fy,gx,gy=sign*fhx,sign*fhy,sign*ftx,sign*fty
                s=2*face-1
                # t = R normalize(T-H); distribute its exact Jacobian to H/T.
                vx=s*(long/2*fy+short/2*gy)
                vy=-s*(long/2*fx+short/2*gx)
                nx,ny=tangent[unit,1],-tangent[unit,0]
                dot=vx*nx+vy*ny
                cx=(vx-dot*nx)/lengths[unit]
                cy=(vy-dot*ny)/lengths[unit]
                force[unit,0]+=fx-cx; force[unit,1]+=fy-cy
                force[n+unit,0]+=gx+cx; force[n+unit,1]+=gy+cy
    return force,energy


def free_faces(n,links):
    free=np.ones((n,2),dtype=np.bool_)
    for i,j,a,b in links:
        free[i,a]=free[j,b]=False
    return free


def update_faces(pos,links,config,rng,neighbors,interval):
    n=len(pos)//2
    long,short=1.,config['short_length']
    head,tail,_,_=port_geometry(pos,n,long,short)
    kept=[]; broken=0
    for i,j,a,b in sorted(links):
        stretch=max(abs(np.linalg.norm(pos[j]-pos[i])-long),
                    abs(np.linalg.norm(pos[n+j]-pos[n+i])-short))
        if stretch>config['break_extension'] or rng.random() < -np.expm1(-config['bond_off_rate']*interval):
            broken+=1
        else: kept.append((i,j,a,b))
    free=free_faces(n,kept)
    existing={tuple(sorted((i,j))) for i,j,_,_ in kept}
    candidates=neighbors.pairs(pos[:n],long+4*config['dock_width'],'face_capture').copy()
    rng.shuffle(candidates)
    if config['bonding']:
        for i,j in candidates:
            i,j=int(i),int(j)
            if (i,j) in existing: continue
            for a in rng.permutation(2):
                a=int(a); b=1-a
                if not free[i,a] or not free[j,b]: continue
                q=np.sum((head[j,b]-head[i,a])**2)+np.sum((tail[j,b]-tail[i,a])**2)
                if q<config['dock_capture']**2 and rng.random() < -np.expm1(-config['dock_rate']*interval):
                    kept.append((i,j,a,b)); existing.add((i,j))
                    free[i,a]=free[j,b]=False
                    break
    return sorted(kept),broken
