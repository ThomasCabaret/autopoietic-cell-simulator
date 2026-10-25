"""C3A: construct actual dimers from persistent independent precursor beads."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.run_batch5 import scenario as previous
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe

CASES={
    'C3copy':{},
    'C3expression':dict(free_units=0,function_units=24),
    'C3mixed':dict(free_units=24,function_units=24),
    'C3noassembly':dict(rung_formation_rate=0.),
    'C3noligation':dict(ligation=False),
    'C3nogene':dict(template=False),
    'C3prepared':dict(assembled_stock=True),
}

def scenario(case,seed=0,duration=800.,overrides=None):
    if case not in CASES:raise ValueError('Unknown batch6 case')
    change=dict(constructible=True,assembled_stock=False,food_pairs=0,
                free_units=24,function_units=0,sequence='001')
    change.update(CASES[case]);change.update(overrides or {})
    cfg=previous('E3cooperative3',seed,duration,change)
    cfg.update(name=case,branch='C3A')
    return cfg

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',choices=CASES)
    p.add_argument('--seed',type=int,default=0);p.add_argument('--duration',type=float,default=800.)
    p.add_argument('--overrides',type=Path)
    a=p.parse_args();changes=json.loads(a.overrides.read_text()) if a.overrides else None
    evidence,path=run(scenario(a.case,a.seed,a.duration,changes),ROOT/'research/engine_runs')
    export_recipe(path)
    if evidence['error']:raise SystemExit(1)
