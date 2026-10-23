"""Research execution and provenance; no graphics imported here."""
from datetime import datetime,timezone
import json
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
        'closed_sets','translated_sets','certified_generations','functional_chain_shapes_final','ancestry_criterion')}


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
              'source_sha256':checkpoint.source_hashes(),'numpy':np.__version__,
              'elapsed_seconds':elapsed,'error':error,'completed':sim.done,
              'metrics':metrics,'expected_checks':checks}
    (path/'result.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
    if observer.frames:
        extra={'pairing':np.array(observer.pairing_frames),'recognition_types':observer.last_bits,
               'families':observer.last_families} if sim.config['model']=='copy' else {}
        np.savez_compressed(path/'trajectory.npz',positions=np.array(observer.frames),
                            times=np.array(observer.times),edges=np.array(observer.edges_frames),**extra)
    checkpoint.save(path/'checkpoint.npz',sim,observer)
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
    equal=json.dumps(obs.summary(),sort_keys=True)==json.dumps(evidence['metrics'],sort_keys=True)
    print(json.dumps({'all_metrics_reproduced':equal}))
    if not equal:
        raise AssertionError('Replay observations differ')
