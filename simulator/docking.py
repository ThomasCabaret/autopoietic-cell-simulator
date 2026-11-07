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


@njit(cache=True, nogil=True, inline='always')
def project_port_force(force, unit, tail, face, fx, fy, gx, gy, tangent, length, long, short):
    """Apply the Jacobian of the port geometry to one pair of endpoint forces."""
    s=2*face-1
    vx=s*(long/2*fy+short/2*gy);vy=-s*(long/2*fx+short/2*gx)
    nx,ny=tangent[1],-tangent[0]
    dot=vx*nx+vy*ny
    cx,cy=(vx-dot*nx)/length,(vy-dot*ny)/length
    force[unit,0]+=fx-cx;force[unit,1]+=fy-cy
    force[tail,0]+=gx+cx;force[tail,1]+=gy+cy


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
                project_port_force(force,unit,n+unit,face,fx,fy,gx,gy,
                                   tangent[unit],lengths[unit],long,short)
    return force,energy


def free_faces(n,links):
    free=np.ones((n,2),dtype=np.bool_)
    for i,j,a,b in links:
        free[i,a]=free[j,b]=False
    return free


@njit(cache=True,nogil=True)
def bound_port_force(pos,links,long,short,epsilon,width):
    """Harmonic continuation of the existing free-port potential at q=0.

    Explicit bonded four-bead motifs only; no component or contour read.
    Replaces row springs/angles in the opt-in candidate, never adds to them.
    """
    n=len(pos)//2
    head,tail,tangent,lengths=port_geometry(pos,n,long,short)
    force=np.zeros_like(pos);energy=0.
    stiffness=epsilon*(1-np.exp(-8.))/(width*width)
    offset=-epsilon*(1-9*np.exp(-8.))
    for k in range(len(links)):
        i,j,a,b=links[k]
        hx,hy=head[j,b,0]-head[i,a,0],head[j,b,1]-head[i,a,1]
        tx,ty=tail[j,b,0]-tail[i,a,0],tail[j,b,1]-tail[i,a,1]
        energy+=offset+.5*stiffness*(hx*hx+hy*hy+tx*tx+ty*ty)
        for unit,face,sign in ((i,a,1.),(j,b,-1.)):
            fx,fy=sign*stiffness*hx,sign*stiffness*hy
            gx,gy=sign*stiffness*tx,sign*stiffness*ty
            project_port_force(force,unit,n+unit,face,fx,fy,gx,gy,
                               tangent[unit],lengths[unit],long,short)
    return force,energy


def update_faces(pos,links,config,rng,neighbors,interval,extra_energy=None,stats=None):
    n=len(pos)//2
    long,short=1.,config['short_length']
    head,tail,_,_=port_geometry(pos,n,long,short)
    gated=config.get('contact_update_gate','none')=='metropolis'
    if gated and config.get('bound_barrier_radius',0.)>0 and extra_energy is None:
        raise ValueError('Energy-gated contacts require the bound-segment energy callback')
    def accept(current,removed,formed,kind):
        from .exchange_energy import port_delta
        from .transition_energy import thermal_factor
        delta=port_delta(pos,current,removed,formed,config,neighbors)
        if extra_energy is not None:delta+=float(extra_energy(removed,formed))
        factor=thermal_factor(delta,config['temperature'])
        accepted=not (factor<1. and (factor<=0. or rng.random()>=factor))
        if stats is not None:
            s=stats[kind];s['proposals']+=1;s['accepted']+=int(accepted);s['rejected']+=int(not accepted)
            s['positive_delta']+=int(delta>0);s['sum_factor']+=factor;s['sum_accepted_delta']+=delta if accepted else 0.
            s['max_delta']=delta if s['max_delta'] is None else max(s['max_delta'],delta)
            s['min_delta']=delta if s['min_delta'] is None else min(s['min_delta'],delta)
        return accepted
    kept=[]; broken=0;current=list(links) if gated else None
    for i,j,a,b in sorted(links):
        stretch=max(abs(np.linalg.norm(pos[j]-pos[i])-long),
                    abs(np.linalg.norm(pos[n+j]-pos[n+i])-short))
        proposed=stretch>config['break_extension'] or rng.random() < -np.expm1(-config['bond_off_rate']*interval)
        if proposed and (not gated or accept(current,(i,j,a,b),None,'breaking')):
            broken+=1
            if gated:current.remove((i,j,a,b))
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
                    if gated and not accept(kept,None,(i,j,a,b),'formation'):continue
                    kept.append((i,j,a,b)); existing.add((i,j))
                    free[i,a]=free[j,b]=False
                    break
    return sorted(kept),broken
