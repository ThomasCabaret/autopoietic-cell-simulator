"""Generate source-frozen common-bath experiments and thermal controls."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.run_batch8 import scenario as genetic_scenario
from simulator.runner import run
from scripts.reconstruct_experiment import export_recipe


def scenario(case,seed=0,duration=400.):
    gene=genetic_scenario('C3Bexpress',seed,duration)['chemistry'].copy()
    if case in ('native','cold'):
        gene['temperature']=.6 if case=='native' else .08
        return dict(schema_version=1,model='copy',name='J0_'+case,branch='J0T',seed=seed,duration=duration,
                    engine=dict(dt=.002,sample_every=250),chemistry=gene)
    if case not in ('bath','no_boundary'):raise ValueError(case)
    gene.pop('temperature',None)
    chemistry=dict(genetics=gene,membrane=dict(contact_exchange_rate=.2,terminal_exchange=True),
                   include_membrane=case=='bath',packet_offset=[27.5,0.])
    return dict(schema_version=1,model='coupled_bath',name='J0_'+case,branch='J0',seed=seed,duration=duration,
                engine=dict(dt=.002,sample_every=250),chemistry=chemistry)


def plan(duration=400.):
    return dict(name='J0 common physical bath and native thermal controls',workers=2,
        checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,
        comparison_policy='J0 bath/no_boundary same laws, L presence initial only. Native/cold are explicit thermal controls, not the same candidate. No membrane synthesis claimed.',
        tasks=[dict(scenario=scenario(case,seed,duration)) for seed in range(3)
               for case in ('native','cold','no_boundary','bath')])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('case',choices=['native','cold','no_boundary','bath','plan'])
    p.add_argument('--seed',type=int,default=0);p.add_argument('--duration',type=float,default=400.)
    p.add_argument('--output',type=Path);a=p.parse_args()
    if a.case=='plan':
        target=a.output or ROOT/'campaigns/common_bath.json';target.write_text(json.dumps(plan(a.duration),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    else:
        result,path=run(scenario(a.case,a.seed,a.duration),a.output or ROOT/'research/engine_runs',record=False)
        export_recipe(path)
        if result['error']:raise SystemExit(1)
