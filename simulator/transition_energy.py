"""Exact finite-neighborhood mechanical delta for a single new H--T bond.

Only changed cores, released capture sites, one axial spring and newly exposed
ports contribute. No total-world energy, component, sequence, target count or
observer is read. The search may scan arrays, as other local kernels do; all
contributions have the same finite cutoffs as their force law.
"""
import math
import numpy as np
from numba import njit
from .docking import docking_force,free_faces


@njit(cache=True)
def _index_pairs(pairs, count):
    offsets = np.zeros(count+1, dtype=np.int64)
    for a, b in pairs:
        offsets[a+1] += 1
        offsets[b+1] += 1
    offsets = np.cumsum(offsets)
    cursor = offsets[:-1].copy()
    rows = np.empty(2*len(pairs), dtype=np.int64)
    for row, (a, b) in enumerate(pairs):
        rows[cursor[a]] = row
        rows[cursor[b]] = row
        cursor[a] += 1
        cursor[b] += 1
    return offsets, rows, pairs


def formation_pairs(c, neighbors):
    """Index fixed geometric candidates once per tick, preserving pair order."""
    count = len(c.pos)
    core, capture = (_index_pairs(neighbors.pairs(c.pos, radius, key), count) for radius, key in (
        (float(c.contact.max()), 'HT:delta_core'),
        (3*c.config['food_ligand_width'], 'HT:delta_capture')))
    ports = None
    if c.config.get('free_port_potential', 'additive') == 'competitive':
        from .competitive_ports import birth_port_base
        ports = birth_port_base(c, neighbors)
    return core, capture, ports


def _incident(index, ids):
    offsets, rows, pairs = index
    selected = np.unique(np.concatenate([rows[offsets[i]:offsets[i+1]] for i in ids]))
    return pairs[selected]


def formation_energy(c,h,t,neighbors,fixed_pairs=None):
    cfg=c.config;pos=c.pos;cap=c.capture;changed={h,t}
    core_pairs,capture_pairs,port_base=formation_pairs(c,neighbors) if fixed_pairs is None else fixed_pairs
    pairs=_incident(core_pairs,changed)
    core=0.
    for a,b in pairs:
        ka,kb=int(c.kinds[a]),int(c.kinds[b]);newa=3 if a in changed else ka;newb=3 if b in changed else kb
        before,after=c.contact[ka,kb],c.contact[newa,newb]
        if before!=after:
            d=float(np.linalg.norm(pos[a]-pos[b]))
            core+=40*(max(after-d,0.)**2-max(before-d,0.)**2)
    axial=90*(float(np.linalg.norm(pos[h]-pos[t]))-.65)**2
    released={int(cap.atom_bound[a]) for a in changed if cap.atom_bound[a]>=0}
    springs=-sum(.5*cap.stiffness*float(np.sum((pos[c.rungs[s,1]]-pos[cap.site_bound[s]])**2)) for s in released)
    affected=cap.affected_sites(c,released) if hasattr(cap,'affected_sites') else released
    touched=changed|{int(c.rungs[s,1]) for s in affected if c.rungs[s,1]>=0}
    pairs=_incident(capture_pairs,touched)
    attraction=0.
    for a,b in pairs:
        for site,atom in ((int(a),int(b)),(int(b),int(a))):
            s=int(cap.owners[site])
            if s<0 or c.pairing[s]>=0:continue
            category=int(cap.categories[atom]);new_category=-1 if atom in changed else category
            old=(category>=0 and c.bits[s]==category and cap.site_bound[s]<0 and cap.atom_bound[atom]<0)
            new=(new_category>=0 and c.bits[s]==new_category and (cap.site_bound[s]<0 or s in released) and
                 (cap.atom_bound[atom]<0 or atom in changed))
            old=old and cap.binding_allowed(c,s,atom)
            new=new and cap.binding_allowed(c,s,atom,released)
            if old!=new:
                value=-cap.activity[s]*cfg['food_ligand_energy']*math.exp(-float(np.sum((pos[atom]-pos[site])**2))/(2*cfg['food_ligand_width']**2))
                attraction+=value*(int(new)-int(old))
    # A newly formed axial pair has two unoccupied faces. Other pairs expose
    # only their actual free local faces. Competitive partitions of existing
    # pairs must also change; the additive branch has no such reweighting.
    ports=0.
    if cfg.get('free_port_potential','additive')=='competitive':
        from .competitive_ports import birth_port_delta
        ports=birth_port_delta(c,h,t,neighbors,port_base)
    elif c.lipids.rungs:
        heads,_,links=c.lipids.layout();available=free_faces(len(heads),links)
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
