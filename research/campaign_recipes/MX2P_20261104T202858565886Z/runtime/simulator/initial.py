"""Explicit prepared material; this module is never consulted by reactions."""
import numpy as np


def groups(config):
    length=len(config['sequence']);starts=[length,length+config['free_units']]
    limits=[starts[1],starts[1]+config['function_units']];result=[]
    if not isinstance(config.get('initial_assemblies',[]),list):raise ValueError('initial_assemblies must be a list')
    for item in config.get('initial_assemblies',[]):
        if not isinstance(item,dict) or set(item)-{'family','sequence','backbone'}:
            raise ValueError('Invalid initial assembly')
        f=item.get('family');seq=item.get('sequence')
        if f not in (0,1) or not isinstance(seq,str) or not seq or set(seq)-set('012'):
            raise ValueError('Invalid initial assembly family or sequence')
        if not isinstance(item.get('backbone',True),bool):raise ValueError('Initial backbone must be boolean')
        start=starts[f];end=start+len(seq)
        if end>limits[f]:raise ValueError('Initial assemblies exceed the configured monomer stock')
        result.append(dict(family=f,sequence=seq,backbone=item.get('backbone',True),units=tuple(range(start,end))))
        starts[f]=end
    return result


def place(group,pos,n,box,rng,separation):
    ids=np.array(group['units']);start=int(ids[0]);length=len(ids)
    line=np.column_stack((np.arange(length)-(length-1)/2,np.zeros(length)))
    for _ in range(20000):
        angle=rng.uniform(0,2*np.pi);rot=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        p=line@rot.T+rng.uniform([.6,.6],box-.6)
        r=p+np.array([0.,.45])@rot.T
        if np.any(p<.3) or np.any(p>box-.3) or np.any(r<.1) or np.any(r>box-.1):continue
        if np.min(np.linalg.norm(p[:,None]-pos[None,:start],axis=2))<=separation:continue
        pos[ids]=p;pos[n+ids]=r;return
    raise RuntimeError('Initial assembly packing jam: enlarge box or reduce stock')
