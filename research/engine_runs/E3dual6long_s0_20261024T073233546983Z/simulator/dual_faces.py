"""Two local faces of one G dimer; no aggregate identity or global mode."""
import numpy as np
from numba import njit
from .reference import degree,normals,local_port_free


@njit(cache=True,nogil=True)
def reflected_force(pos,pairs,n,stiffness=80.):
    force=np.zeros_like(pos);energy=0.
    for i,j in pairs:
        d=(2*pos[j]-pos[n+j])-(2*pos[i]-pos[n+i])
        f=stiffness*d
        force[i]+=2*f;force[n+i]-=f
        force[j]-=2*f;force[n+j]+=f
        energy+=.5*stiffness*np.dot(d,d)
    return force,energy


def react(c,time,dt,neighbors):
    cfg,rng=c.config,c.rng;n=c.n;interval=5*dt
    deg=degree(n,c.edges);nrm=normals(c.pos,c.rungs)
    release=c.cycle=='cycle' and time%c.period>=c.period-c.release_time
    source_edges=sorted(c.edges);events=[]
    # Each face has its own local saturation state. Both are active concurrently.
    for back,pairing in ((True,c.copy_pairing),(False,c.pairing)):
        for i,j in enumerate(pairing):
            if j<=i:continue
            rate=.003
            if c.gate and deg[i]==0 and deg[j]==0:rate=5.
            if release:rate=12.
            if c.cycle=='local' and deg[i]>0 and deg[j]>0:rate=cfg['local_off_rate']
            if rng.random() < -np.expm1(-rate*interval):pairing[i]=pairing[j]=-1
        sites=2*c.pos[:n]-c.pos[n:2*n] if back else c.pos[n:2*n]
        candidates=neighbors.pairs(sites,.3,'recognition_back' if back else 'recognition_front').copy()
        rng.shuffle(candidates)
        for i,j in candidates:
            if release or c.bits[i]!=c.bits[j] or pairing[i]>=0 or pairing[j]>=0:continue
            if np.dot(nrm[i],nrm[j])>-.5:continue
            if back:
                if c.families[i]!=0 or c.families[j]!=0:continue
            else:
                if c.families[i]==c.families[j]:continue
                g,f=(i,j) if c.families[i]==0 else (j,i)
                if deg[g]==0 or deg[f]!=0:continue
                if c.food is not None and c.food.site_bound[f]>=0:continue
            if cfg['monomer_only_capture'] and not ((deg[i]>0)!=(deg[j]>0)):continue
            rate=35. if not c.gate or deg[i] or deg[j] else .1
            if rng.random() < -np.expm1(-rate*interval):pairing[i]=j;pairing[j]=i
        for i,j in source_edges:
            if c.families[i]!=0 or c.families[j]!=0:continue
            a,b=int(pairing[i]),int(pairing[j])
            if a<0 or b<0 or a==b:continue
            pair=tuple(sorted((a,b)))
            if pair in c.edges or not cfg['ligation']:continue
            if c.families[a]!=c.families[b]:continue
            d=c.pos[b]-c.pos[a];distance=np.linalg.norm(d)
            if not .72<distance<1.28 or np.dot(nrm[a],nrm[b])<.5:continue
            if abs(np.dot(nrm[a],d))>.5*distance or abs(np.dot(nrm[b],d))>.5*distance:continue
            if not local_port_free(a,b,c.pos,c.edges,c.capacities[a]) or not local_port_free(b,a,c.pos,c.edges,c.capacities[b]):continue
            if rng.random() < -np.expm1(-cfg['ligation_rate']*interval):
                c.edges.add(pair);events.append(dict(source=(i,j),formed=pair,face='back' if back else 'front'))
    return events
