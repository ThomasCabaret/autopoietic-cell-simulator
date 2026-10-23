"""Versioned NPZ + tagged JSON, including RNG, bonds, caches and observers."""
import hashlib
import json
from pathlib import Path
import numpy as np
from .engine import Simulation


def source_hashes():
    root=Path(__file__).parent
    return {'simulator/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.glob('*.py'))}


def pack(value):
    if isinstance(value,np.ndarray):
        return {'@':'array','dtype':str(value.dtype),'shape':list(value.shape),'data':value.tolist()}
    if isinstance(value,dict):
        return {'@':'dict','data':[[pack(k),pack(v)] for k,v in value.items()]}
    if isinstance(value,(set,tuple)):
        return {'@':type(value).__name__,'data':[pack(v) for v in value]}
    if isinstance(value,list):
        return [pack(v) for v in value]
    if isinstance(value,np.generic):
        return value.item()
    return value


def unpack(value):
    if isinstance(value,list):
        return [unpack(v) for v in value]
    if not isinstance(value,dict):
        return value
    kind=value['@']
    if kind=='array':
        return np.array(value['data'],dtype=value['dtype']).reshape(value['shape'])
    if kind=='dict':
        return {unpack(k):unpack(v) for k,v in value['data']}
    return (set if kind=='set' else tuple)(unpack(v) for v in value['data'])


def save(path, simulation, observer=None):
    simulation.prepare()
    c=simulation.chemistry
    metadata={'checkpoint_version':1,'config':simulation.config,'step':simulation.step_index,
              'prepared':simulation.prepared,'rng':simulation.rng.bit_generator.state,
              'chemistry':c.export(),'source_sha256':source_hashes(),
              'observer':pack(observer.__dict__) if observer is not None else None}
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    with temporary.open('wb') as stream:
        np.savez_compressed(stream,metadata=json.dumps(metadata,allow_nan=False),
                            positions=c.pos,springs=c.springs,angles=c.angles)
    temporary.replace(path)


def load(path, observer_factory=None):
    with np.load(path,allow_pickle=False) as data:
        metadata=json.loads(str(data['metadata']))
        if metadata['checkpoint_version']!=1:
            raise ValueError('Unsupported checkpoint version')
        if metadata['source_sha256']!=source_hashes():
            raise ValueError('Checkpoint code differs. Replay with its archived simulator sources.')
        sim=Simulation(metadata['config'])
        sim.step_index=metadata['step']
        sim.prepared=metadata['prepared']
        sim.rng.bit_generator.state=metadata['rng']
        sim.chemistry.pos=data['positions'].copy()
        sim.chemistry.springs=data['springs'].copy()
        sim.chemistry.angles=data['angles'].copy()
        sim.chemistry.restore(metadata['chemistry'])
    observer=None
    if observer_factory is not None:
        observer=observer_factory(sim.config)
        if metadata['observer'] is not None:
            observer.__dict__.update(unpack(metadata['observer']))
        sim.listeners.append(observer)
    return sim,observer
