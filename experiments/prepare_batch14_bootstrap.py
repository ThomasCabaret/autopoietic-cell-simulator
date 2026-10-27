"""Matched prepared/unlinked F001 initial tools, same atoms and fixed J0 laws."""
import argparse,copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.run_batch13 import scenario as previous
from simulator.engine import Simulation
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe
import numpy as np


def scenario(case,seed=0,duration=1200.):
    bath=case.startswith('bath');linked=case.endswith('prepared')
    if case not in ('cold_prepared','cold_unlinked','bath_prepared','bath_unlinked'):raise ValueError(case)
    cfg=previous('bath' if bath else 'cold',seed,duration)
    cfg['name']='J1_'+case;cfg['branch']='J1'
    g=cfg['chemistry']['genetics'] if bath else cfg['chemistry']
    g['initial_assemblies']=([dict(family=1,sequence='001',backbone=linked)]+
        [dict(family=1,sequence=b,backbone=False) for b in '011'])
    return cfg


def verify_initial_pair(bath,seed):
    prefix='bath' if bath else 'cold'
    a=Simulation(scenario(prefix+'_prepared',seed,.02));b=Simulation(scenario(prefix+'_unlinked',seed,.02))
    np.testing.assert_array_equal(a.chemistry.pos,b.chemistry.pos)
    assert a.rng.bit_generator.state==b.rng.bit_generator.state
    ga=getattr(a.chemistry,'genetics',a.chemistry);gb=getattr(b.chemistry,'genetics',b.chemistry)
    np.testing.assert_array_equal(ga.bits,gb.bits);np.testing.assert_array_equal(ga.rungs,gb.rungs)
    assert ga.edges-gb.edges=={(27,28),(28,29)} and gb.edges<=ga.edges
    assert len(a.chemistry.pos)==(588 if bath else 102)
    return dict(bath=bath,seed=seed,positions_rng_atoms_identical=True,only_two_F_bonds_differ=True)


def plan():
    return dict(name='J1 constructed tool versus geometrically matched unlinked control',
        workers=2,checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,genetic_audit=True,
        comparison_policy='All J0 laws fixed at0.08, six F monomers preserved. Only two initial bonds differ in each prepared/unlinked pair; initial tool is not a translated product.',
        tasks=[dict(scenario=scenario(case,seed)) for seed in range(3)
               for case in ('cold_prepared','cold_unlinked','bath_prepared','bath_unlinked')])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['plan','verify','pilot'])
    p.add_argument('--output',type=Path);a=p.parse_args()
    if a.action=='plan':
        target=a.output or ROOT/'campaigns/constructed_tool.json';target.write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    elif a.action=='verify':print(json.dumps([verify_initial_pair(b,s) for b in (False,True) for s in range(3)]))
    else:
        for case in ('cold_prepared','cold_unlinked'):
            evidence,path=run(scenario(case,0,200.),a.output or ROOT/'research/engine_runs',record=False)
            export_recipe(path)
            if evidence['error']:raise SystemExit(1)
