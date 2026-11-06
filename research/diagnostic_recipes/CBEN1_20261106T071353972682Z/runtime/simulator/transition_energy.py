"""Exact finite-neighborhood mechanical delta for a single new H--T bond.

Only changed cores, released capture sites, one axial spring and newly exposed
ports contribute. No total-world energy, component, sequence, target count or
observer is read. The search may scan arrays, as other local kernels do; all
contributions have the same finite cutoffs as their force law.
"""
import math
import numpy as np
from .docking import docking_force,free_faces


def formation_energy(c,h,t,neighbors):
    cfg=c.config;pos=c.pos;cap=c.capture;changed={h,t}
    pairs=neighbors.pairs(pos,float(c.contact.max()),'HT:delta_core')
    pairs=pairs[np.isin(pairs[:,0],[h,t])|np.isin(pairs[:,1],[h,t])]
    core=0.
    for a,b in pairs:
        ka,kb=int(c.kinds[a]),int(c.kinds[b]);newa=3 if a in changed else ka;newb=3 if b in changed else kb
        d=float(np.linalg.norm(pos[a]-pos[b]))
        core+=40*(max(c.contact[newa,newb]-d,0.)**2-max(c.contact[ka,kb]-d,0.)**2)
    axial=90*(float(np.linalg.norm(pos[h]-pos[t]))-.65)**2
    released={int(cap.atom_bound[a]) for a in changed if cap.atom_bound[a]>=0}
    springs=-sum(.5*cap.stiffness*float(np.sum((pos[c.rungs[s,1]]-pos[cap.site_bound[s]])**2)) for s in released)
    affected=cap.affected_sites(c,released) if hasattr(cap,'affected_sites') else released
    touched=list(changed|{int(c.rungs[s,1]) for s in affected if c.rungs[s,1]>=0})
    pairs=neighbors.pairs(pos,3*cfg['food_ligand_width'],'HT:delta_capture')
    pairs=pairs[np.isin(pairs[:,0],touched)|np.isin(pairs[:,1],touched)]
    attraction=0.
    for a,b in pairs:
        for site,atom in ((int(a),int(b)),(int(b),int(a))):
            s=int(cap.owners[site])
            if s<0 or c.pairing[s]>=0:continue
            category=int(cap.categories[atom]);new_category=-1 if atom in changed else category
            value=-cap.activity[s]*cfg['food_ligand_energy']*math.exp(-float(np.sum((pos[atom]-pos[site])**2))/(2*cfg['food_ligand_width']**2))
            old=(category>=0 and c.bits[s]==category and cap.site_bound[s]<0 and cap.atom_bound[atom]<0)
            new=(new_category>=0 and c.bits[s]==new_category and (cap.site_bound[s]<0 or s in released) and
                 (cap.atom_bound[atom]<0 or atom in changed))
            old=old and cap.binding_allowed(c,s,atom)
            new=new and cap.binding_allowed(c,s,atom,released)
            attraction+=value*(int(new)-int(old))
    # A newly formed axial pair has two unoccupied faces. Other pairs expose
    # only their actual free local faces; existing port energies do not change.
    heads,_,links=c.lipids.layout();available=free_faces(len(heads),links);ports=0.
    if cfg.get('free_port_potential','additive')=='competitive':
        from .competitive_ports import birth_port_delta
        ports=birth_port_delta(c,h,t,neighbors)
    elif heads:
        points=np.vstack((pos[heads],pos[h]));last=len(heads)
        nearby=neighbors.pairs(points,1.+4*cfg['dock_width'],'HT:delta_ports')
        for i,j in nearby:
            if j!=last:continue
            a=heads[i];b=c.lipids.rungs[a]
            p=pos[[a,h,b,t]];free=np.vstack((available[i],[True,True]))
            ports+=docking_force(p,np.array([[0,1]],dtype=np.int64),free,1.,cfg['short_length'],
                cfg['dock_energy'],cfg['dock_width'])[1]
    return dict(core=float(core),HT_axial=axial,capture_springs=springs,
                free_capture_potential=float(attraction),ports=float(ports))


def thermal_factor(delta,temperature):
    if delta<=0:return 1.
    return math.exp(-delta/temperature) if temperature>0 else 0.
