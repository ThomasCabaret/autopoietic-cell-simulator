"""E3 same-bath coexistence on C2D; baseline and reflected-face candidates."""
import argparse,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.run_batch4 import scenario as previous
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe
SEQUENCES={name:seq for seq,names in [
    ('001',['E3base3','E3dual3','E3dual3Fonly','E3dual3nogene','E3dual3bare','E3cooperative3','E3cooperative3Fonly','E3cooperative3nogene']),
    ('001011',['E3base6','E3dual6','E3dual6long','E3base6long','E3dual6extended','E3base6extended','E3dual6Gonly','E3base6Gonly','E3cooperative6','E3cooperative6Gonly'])]
    for name in names}
DUAL_CASES={'E3dual3','E3dual6','E3dual6long','E3dual6extended','E3dual3Fonly',
            'E3dual6Gonly','E3dual3nogene','E3dual3bare'}
COOPERATIVE_CASES={'E3cooperative3','E3cooperative6','E3cooperative3Fonly','E3cooperative3nogene','E3cooperative6Gonly'}

def scenario(case,seed,duration,overrides=None,sequence=None):
    if sequence is None and case not in SEQUENCES:raise ValueError('Unknown case: provide an explicit sequence')
    seq=sequence or SEQUENCES[case]
    changes=dict(sequence=seq,free_units=24,function_units=24,
                 dual_faces=case in DUAL_CASES,product_cooperativity=case in COOPERATIVE_CASES)
    if case in {'E3dual3Fonly','E3cooperative3Fonly'}:changes['free_units']=0
    if case in {'E3dual6Gonly','E3base6Gonly','E3cooperative6Gonly'}:changes.update(free_units=48,function_units=0,food_pairs=0)
    if case in {'E3dual3nogene','E3cooperative3nogene'}:changes['template']=False
    if case=='E3dual3bare':changes.update(food_ligand_energy=0.,food_binding_rate=0.)
    changes.update(overrides or {})
    cfg=previous('C2express',seed,duration,changes,case,candidate='D')
    cfg['branch']='E3'
    return cfg

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case');p.add_argument('--seed',type=int,default=0)
    p.add_argument('--duration',type=float,default=1200.);p.add_argument('--overrides',type=Path)
    p.add_argument('--sequence',choices=['001','001011'])
    a=p.parse_args();changes=json.loads(a.overrides.read_text()) if a.overrides else None
    evidence,path=run(scenario(a.case,a.seed,a.duration,changes,a.sequence),ROOT/'research/engine_runs')
    export_recipe(path)
    if evidence['error']:raise SystemExit(1)
