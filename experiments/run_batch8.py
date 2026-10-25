"""Frozen C3B1 catalytic-precursor transfer candidate and explicit controls."""
import argparse,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.run_batch6 import scenario as previous
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe

CASES={
    'C3Bprepared':{},
    'C3Bunlinked':{'initial_assemblies':[dict(family=1,sequence='001',backbone=False)]},
    'C3Bbare':dict(food_ligand_energy=0.,food_binding_rate=0.),
    'C3Bnone':dict(initial_assemblies=[]),
    'C3BunlinkedNoLigation':dict(ligation=False,initial_assemblies=[dict(family=1,sequence='001',backbone=False)]),
    'C3BnoBoost':dict(rung_catalytic_rate=.0001),
    'C3Bexpress':dict(function_units=24,initial_assemblies=[dict(family=1,sequence=b,backbone=False) for b in '001011']),
    'C3Bnogene':dict(template=False,function_units=24,initial_assemblies=[dict(family=1,sequence=b,backbone=False) for b in '001011'])
}


def scenario(case,seed=0,duration=800.,overrides=None):
    if case not in CASES:raise ValueError('Unknown batch8 case')
    change=dict(free_units=24,function_units=3,rung_catalysis=True,rung_formation_rate=.0001,
        initial_assemblies=[dict(family=1,sequence='001',backbone=True)])
    change.update(CASES[case]);change.update(overrides or {})
    cfg=previous('C3copy',seed,duration,change);cfg.update(name=case,branch='C3B1')
    return cfg


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',choices=CASES)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--duration',type=float,default=800.)
    p.add_argument('--overrides',type=Path)
    a=p.parse_args();changes=json.loads(a.overrides.read_text()) if a.overrides else None
    r,path=run(scenario(a.case,a.seed,a.duration,changes),ROOT/'research/engine_runs');export_recipe(path)
    if r['error']:raise SystemExit(1)
