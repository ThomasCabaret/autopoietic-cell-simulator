"""C2 integration on actual composite F units; frozen candidate per run."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe

CANDIDATE=dict(alphabet='01',free_units=0,function_units=0,food_pairs=8,
    activation=True,release='cycle',period=200.,release_time=15.,backbone_angle=20.,
    box=[8.,6.],monomer_only_capture=True,temperature=.6,
    functional_bend_cosines={'0':.6,'1':-.5},functional_bend_strength=100.,
    food_ligand_energy=2.,food_ligand_width=.6,food_binding_radius=.25,
    food_binding_rate=20.,food_unbinding_rate=.1,food_reaction_radius=.25,food_reaction_rate=.2)
CASES={
    'C2prepared':dict(sequence='001',seed_family=1),
    'C2shuffled':dict(sequence='010',seed_family=1),
    'C2loose':dict(sequence='001',seed_family=1,template=False),
    'C2bare':dict(sequence='001',seed_family=1,food_ligand_energy=0.,food_binding_rate=0.),
    'C2express':dict(sequence='001',seed_family=0,function_units=24),
    'C2nogene':dict(sequence='001',seed_family=0,function_units=24,template=False),
    'C2copyref':dict(sequence='001011',seed_family=0,free_units=48,food_pairs=0),
    'C2expressionref':dict(sequence='001011',seed_family=0,function_units=48,food_pairs=0),
}
CANDIDATES={
    'A':{},
    'B':dict(functional_cosines={'0':.8,'1':.8}),
    'C':dict(functional_cosines={'0':.8,'1':.8},functional_bend_cosines={}),
    'D':dict(functional_cosines={'0':.8,'1':.8},functional_bend_cosines={},food_activation=True),
}

def scenario(case,seed,duration,overrides=None,name=None,candidate='C'):
    return resolve(dict(schema_version=1,model='copy',name=name or case+candidate,branch='C2',seed=seed,
        duration=duration,chemistry={**CANDIDATE,**CANDIDATES[candidate],**CASES[case],**(overrides or {})},
        engine=dict(dt=.005,sample_every=100)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',choices=CASES)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--duration',type=float,default=200.)
    p.add_argument('--overrides',type=Path);p.add_argument('--name')
    p.add_argument('--candidate',choices=CANDIDATES,default='C')
    a=p.parse_args(); overrides=json.loads(a.overrides.read_text()) if a.overrides else None
    evidence,path=run(scenario(a.case,a.seed,a.duration,overrides,a.name,a.candidate),ROOT/'research/engine_runs')
    export_recipe(path)
    if evidence['error']: raise SystemExit(1)
