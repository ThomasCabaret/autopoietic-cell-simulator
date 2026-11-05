"""Finite-neighborhood potential difference for one lateral-contact replacement.

Only three L have changed occupancy; their spatial neighbors retain the same
cutoffs as the force law. No aggregate, contour or biological label is read.
"""
import numpy as np
from .docking import free_faces,docking_force,bound_port_force


def port_delta(pos,links,removed,formed,config,neighbors):
    n=len(pos)//2;changed=(set(removed[:2]) if removed is not None else set())|(set(formed[:2]) if formed is not None else set())
    new=[e for e in links if removed is None or tuple(e)!=tuple(removed)]
    if formed is not None:new.append(tuple(formed))
    pairs=neighbors.pairs(pos[:n],1.+4*config['dock_width'],'exchange_delta')
    keep=np.isin(pairs[:,0],list(changed))|np.isin(pairs[:,1],list(changed));pairs=pairs[keep]
    def free_energy(edges):
        partners=np.full((n,2),-1,dtype=np.int64)
        for i,j,a,b in edges:partners[i,a]=j;partners[j,b]=i
        return docking_force(pos,pairs,free_faces(n,edges),1.,config['short_length'],
            config['dock_energy'],config['dock_width'],partners)[1]
    def bound_energy(edge):
        if edge is None:return 0.
        return bound_port_force(pos,np.asarray([edge],dtype=np.int64),1.,config['short_length'],
            config['dock_energy'],config['dock_width'])[1]
    return float(free_energy(new)-free_energy(links)+bound_energy(formed)-bound_energy(removed))
