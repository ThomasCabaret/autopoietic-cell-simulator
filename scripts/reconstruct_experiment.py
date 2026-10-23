"""Rebuild ignored experiment data from a tracked recipe and exact archived code."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]


def export_recipe(folder):
    folder=Path(folder)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    hashes=result['source_sha256']
    if isinstance(hashes,str): hashes={'audit_causal_network.py':hashes}
    for name,digest in hashes.items():
        if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Source checksum differs: '+name)
    kind='causal_audit' if result.get('kind')=='formal_design_audit_not_molecular_simulation' else (
        'shared_engine' if result.get('format_version')==2 else 'local_dynamics')
    recipe={'recipe_version':1,'run_id':folder.name,'kind':kind,'source_sha256':hashes,
            'environment':{'python':'3.12','numpy':result.get('numpy','not applicable')},
            'initialization_incident':bool(result.get('error'))}
    if kind=='shared_engine': recipe['scenario']=result['scenario']
    elif kind=='local_dynamics': recipe['config']=result['config']
    else: recipe['entrypoint']='audit_causal_network.main'
    (folder/'recipe.json').write_text(json.dumps(recipe,indent=2,ensure_ascii=False),encoding='utf-8')
    return folder/'recipe.json'


def reconstruct(folder,output=None):
    folder=Path(folder).resolve()
    recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
    if recipe.get('initialization_incident'):
        raise ValueError('This recipe records an initialization incident, not a physical trajectory.')
    output=Path(output).resolve() if output else ROOT/'outputs/reconstructed'/folder.name
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Choose an empty output directory: '+str(output))
    output.mkdir(parents=True,exist_ok=True)
    for name,digest in recipe['source_sha256'].items():
        source=(folder/name).resolve()
        if not source.is_relative_to(folder):
            raise ValueError('Source path leaves the recipe folder')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
            raise ValueError('Source checksum differs: '+name)
        target=output/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
    for name in ('config.json','scenario.json','replay.py','recipe.json'):
        if (folder/name).exists(): shutil.copyfile(folder/name,output/name)
    subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(output)],check=True)
    return output


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def worker(folder):
    # A child process prevents current and historical simulator imports mixing.
    sys.path.insert(0,str(folder))
    recipe=json.loads((folder/'recipe.json').read_text(encoding='utf-8'))
    if recipe['kind']=='shared_engine':
        from simulator.engine import Simulation
        from simulator.runner import make_observer,save_result
        sim=Simulation(recipe['scenario'])
        observer=make_observer(sim.config)
        sim.listeners.append(observer)
        start=time.perf_counter()
        while not sim.done: sim.advance(1000)
        save_result(folder,sim,observer,time.perf_counter()-start)
    elif recipe['kind']=='local_dynamics':
        import numpy as np
        dynamics=load_module('local_dynamics',folder/'local_dynamics.py')
        analysis=load_module('archived_analysis',folder/'run_local_research.py')
        config=recipe['config']
        observer=analysis.CopyObserver(config) if config['mode']=='copy' else analysis.VesicleObserver(config)
        start=time.perf_counter()
        (dynamics.copying if config['mode']=='copy' else dynamics.vesicle)(config,config['seed'],observer)
        result={'config':config,'source_sha256':recipe['source_sha256'],'numpy':np.__version__,
                'elapsed_seconds':time.perf_counter()-start,'error':None,'metrics':observer.summary()}
        (folder/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        extra={}
        if config['mode']=='copy':
            extra['recognition_types']=observer.last_bits
            extra['families']=getattr(observer,'last_families',np.zeros(len(observer.last_bits),dtype=int))
            if getattr(observer,'pairing_frames',[]): extra['pairing']=np.array(observer.pairing_frames)
        np.savez_compressed(folder/'trajectory.npz',positions=np.array(observer.frames),
                            times=np.array(observer.times),edges=np.array(observer.edges_frames),**extra)
    else:
        audit=load_module('archived_audit',folder/'audit_causal_network.py')
        audit.ROOT=folder
        audit.main()


def archived_demo(folder):
    original=Path(folder).resolve()
    if (original/'trajectory.npz').exists() and (original/'result.json').exists():
        target=original
    else:
        target=ROOT/'outputs/reconstructed'/original.name
        if not (target/'trajectory.npz').exists() or not (target/'result.json').exists():
            print('Reconstruction de la trajectoire depuis la recette ; premier lancement plus long.',flush=True)
            reconstruct(original,target)
    from simulator.viewer import replay_view
    replay_view(target)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('recipe_folder',type=Path,nargs='?')
    p.add_argument('--output',type=Path)
    p.add_argument('--export-recipe',action='store_true',help='Extract inputs and code hashes from a local result')
    p.add_argument('--worker',type=Path,help=argparse.SUPPRESS)
    args=p.parse_args()
    if args.worker:
        worker(args.worker.resolve())
    elif args.recipe_folder and args.export_recipe:
        print('Recipe: '+str(export_recipe(args.recipe_folder)),flush=True)
    elif args.recipe_folder:
        print('Generated data: '+str(reconstruct(args.recipe_folder,args.output)),flush=True)
    else: p.error('provide an experiment recipe folder')


if __name__=='__main__': main()
