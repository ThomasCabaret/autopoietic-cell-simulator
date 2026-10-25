"""Research execution and provenance; no graphics imported here."""
from datetime import datetime,timezone
import json
import hashlib
from pathlib import Path
import shutil
import time
import numpy as np
from .config import observer_config
from .engine import Simulation
from .observations import CopyObserver,VesicleObserver
from . import checkpoint
from .registry import MODELS


def make_observer(config,record=True):
    c=observer_config(config)
    obj=MODELS[config['model']][2](c)
    obj.record_trajectory=record
    return obj


def compact(metrics):
    return {k:v for k,v in metrics.items() if k not in ('history','events','complete_sets','detached_sets',
        'closed_sets','translated_sets','certified_generations','functional_chain_shapes_final','ancestry_criterion','food_events',
        'assembly_state','assembly_incorporation_times')}


def create_output(config,parent='outputs'):
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in config['name'])
    path=Path(parent)/f'{safe}_s{config["seed"]}_{stamp}'
    path.mkdir(parents=True,exist_ok=False)
    for name in checkpoint.source_hashes():
        target=path/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(Path(__file__).parent/name.split('/')[-1],target)
    (path/'scenario.json').write_text(json.dumps(config,indent=2,ensure_ascii=False),encoding='utf-8')
    (path/'replay.py').write_text('from pathlib import Path\nfrom simulator.runner import replay\nreplay(Path(__file__).parent)\n',encoding='utf-8')
    return path


def save_result(path,sim,observer,elapsed,error=None):
    # Hash the frozen snapshot, not possibly edited development files at run end.
    archived={p.relative_to(path).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((path/'simulator').glob('*.py'))}
    if not archived:
        raise ValueError('Missing archived simulator sources for this result')
    metrics=observer.summary() if observer.times else {}
    checks={}
    for key,criterion in sim.config.get('expected',{}).items():
        actual=metrics.get(key)
        if isinstance(criterion,(int,float)):
            criterion={'min':criterion}
        checks[key]=(actual is not None and all(
            actual>=limit if op=='min' else actual<=limit if op=='max' else actual==limit
            for op,limit in criterion.items()))
    evidence={'format_version':2,'scenario':sim.config,
              'config':{**observer_config(sim.config),'branch':sim.config.get('branch','W0'),
                        'duration':sim.config['duration'],'dt':sim.dt},
              'source_sha256':archived,'numpy':np.__version__,
              'elapsed_seconds':elapsed,'error':error,'completed':sim.done,
              'metrics':metrics,'expected_checks':checks}
    (path/'result.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
    if observer.frames:
        extra={'pairing':np.array(observer.pairing_frames),'recognition_types':observer.last_bits,
               'families':observer.last_families} if sim.config['model']=='copy' else {}
        if getattr(observer,'food_edges_frames',[]):
            extra.update(food_edges=np.array(observer.food_edges_frames),food_binding=np.array(observer.food_binding_frames))
        if getattr(observer,'copy_pairing_frames',[]):extra['copy_pairing']=np.array(observer.copy_pairing_frames)
        if getattr(observer,'rungs_frames',[]):
            extra.update(rungs=np.array(observer.rungs_frames),unit_bits=np.array(observer.unit_bits_frames),
                         atom_bits=np.array(observer.assembly_state['atom_bits']))
        if getattr(observer,'precursor_binding_frames',[]):extra['precursor_binding']=np.array(observer.precursor_binding_frames)
        np.savez_compressed(path/'trajectory.npz',positions=np.array(observer.frames),
                            times=np.array(observer.times),edges=np.array(observer.edges_frames),**extra)
    checkpoint.save(path/'checkpoint.npz',sim,observer,source_manifest=archived)
    return evidence


def run(config,parent='outputs',record=True,resume=None,progress=None):
    if resume:
        sim,obs=checkpoint.load(resume,make_observer)
    else:
        sim=Simulation(config)
        obs=make_observer(sim.config,record)
        sim.listeners.append(obs)
    path=create_output(sim.config,parent)
    start=time.perf_counter()
    error=None
    try:
        while not sim.done:
            sim.advance(250)
            if progress:
                progress(sim)
    except (RuntimeError,FloatingPointError) as exc:
        error=str(exc)
    evidence=save_result(path,sim,obs,time.perf_counter()-start,error)
    print(json.dumps({'run':str(path.resolve()),'error':error,'elapsed':evidence['elapsed_seconds'],
                      'completed':sim.done,'expected_checks':evidence['expected_checks'],
                      **compact(evidence['metrics'])},ensure_ascii=False),flush=True)
    return evidence,path


def replay(path):
    path=Path(path)
    evidence=json.loads((path/'result.json').read_text(encoding='utf-8'))
    for name,expected in evidence['source_sha256'].items():
        import hashlib
        if hashlib.sha256((path/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('Archived source hash mismatch: '+name)
    if checkpoint.source_hashes()!=evidence['source_sha256']:
        raise ValueError('Run the archived replay.py to use its exact engine revision')
    sim=Simulation(evidence['scenario'])
    obs=make_observer(sim.config,record=False)
    sim.listeners.append(obs)
    while not sim.done:
        sim.advance(1000)
    # JSON converts integer atom-ID keys to strings. Compare normalized values,
    # not serialization order (numeric 2,10 differs from string "10","2").
    equal=json.loads(json.dumps(obs.summary()))==evidence['metrics']
    print(json.dumps({'all_metrics_reproduced':equal}))
    if not equal:
        raise AssertionError('Replay observations differ')
