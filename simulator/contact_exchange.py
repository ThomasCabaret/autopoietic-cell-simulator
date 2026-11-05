"""Activated associative displacement on bounded local face contacts.

One occupied face switches partner to a geometrically nearby free face. One
bond disappears and one appears; no closure/insertion or component query occurs.
The displaced partner stays where mechanics put it. Both directions/sides use
the same rule. The default is an explicit nonthermal helper; the optional local
energy gate does not establish global detailed balance for the full chemistry.
"""
import numpy as np
from .docking import port_geometry,free_faces


def exchange_faces(pos,links,config,rng,neighbors,interval,extra_energy=None,stats=None):
    rate=config.get('contact_exchange_rate',0.)
    if rate<=0:return links,[]
    if config.get('contact_exchange_gate','none')=='metropolis' and config.get('bound_barrier_radius',0.)>0 and extra_energy is None:
        raise ValueError('Energy-gated exchange requires the bound-segment energy callback')
    n=len(pos)//2;long=1.;short=config['short_length']
    head,tail,_,_=port_geometry(pos,n,long,short)
    partners=np.full((n,2),-1,dtype=np.int64);partner_faces=np.full((n,2),-1,dtype=np.int64)
    by_pair={}
    for i,j,a,b in links:
        partners[i,a]=j;partners[j,b]=i;partner_faces[i,a]=b;partner_faces[j,b]=a
        by_pair[tuple(sorted((i,j)))]=(i,j,a,b)
    pairs=neighbors.pairs(pos[:n],long+4*config['dock_width'],'exchange_faces').copy();rng.shuffle(pairs)
    probability=-np.expm1(-rate*interval);touched=set();events=[]
    for x,y in pairs:
        for i,k in ((int(x),int(y)),(int(y),int(x))):
            if tuple(sorted((i,k))) in by_pair:continue
            for a in rng.permutation(2):
                a=int(a);b=1-a;j=int(partners[i,a])
                if j<0 or partners[k,b]>=0 or (i,a) in touched or (k,b) in touched:continue
                old_face=int(partner_faces[i,a])
                if (j,old_face) in touched:continue
                # Symmetric under swapping displaced/incoming partners. Read
                # only their other local port occupancy, never a chain identity.
                if config.get('terminal_exchange',False) and partners[j,1-old_face]>=0 and partners[k,1-b]>=0:continue
                dh=np.linalg.norm(pos[k]-pos[i]);dt=np.linalg.norm(pos[n+k]-pos[n+i])
                if max(abs(dh-long),abs(dt-short))>config['break_extension']:continue
                q=float(np.sum((head[k,b]-head[i,a])**2)+np.sum((tail[k,b]-tail[i,a])**2))
                if q>=config['contact_exchange_capture']**2 or rng.random()>=probability:continue
                removed=by_pair[tuple(sorted((i,j)))]
                formed=(i,k,a,b) if i<k else (k,i,b,a)
                delta=None;factor=1.
                if config.get('contact_exchange_gate','none')=='metropolis':
                    from .exchange_energy import port_delta
                    from .transition_energy import thermal_factor
                    delta=port_delta(pos,list(by_pair.values()),removed,formed,config,neighbors)
                    if extra_energy is not None:delta+=float(extra_energy(removed,formed))
                    factor=thermal_factor(delta,config['temperature'])
                    if stats is not None:
                        stats['proposals']+=1;stats['sum_factor']+=factor;stats['positive_delta']+=int(delta>0)
                        stats['sum_positive_delta']+=max(delta,0.)
                        stats['max_delta']=delta if stats['max_delta'] is None else max(stats['max_delta'],delta)
                        stats['min_delta']=delta if stats['min_delta'] is None else min(stats['min_delta'],delta)
                    if factor<1. and (factor<=0. or rng.random()>=factor):
                        if stats is not None:stats['rejected']+=1
                        continue
                    if stats is not None:stats['accepted']+=1
                by_pair.pop(tuple(sorted((i,j))))
                by_pair[tuple(sorted((i,k)))]=formed
                partners[j,old_face]=-1;partner_faces[j,old_face]=-1
                partners[i,a]=k;partner_faces[i,a]=b;partners[k,b]=i;partner_faces[k,b]=a
                touched.update(((i,a),(k,b),(j,old_face)))
                event=dict(removed=list(removed),formed=list(formed),port_mismatch=q)
                if delta is not None:event.update(delta_U=float(delta),energy_factor=factor)
                events.append(event)
                break
    return sorted(by_pair.values()),events
