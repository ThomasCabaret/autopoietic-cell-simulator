"""RV1: frozen turnover ablations, then conditional MD2 transfer."""
import argparse,copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_expression_campaign import baseline,MD2
from simulator.config import resolve
from simulator.coupled_bath import genetics_config


def rates(variant):
    if variant not in ('zero','backbone','full','protected'):raise ValueError(variant)
    return dict(backbone_g=0. if variant=='zero' else .00005,
        backbone_f=0. if variant=='zero' else .001,
        rung_g=.001 if variant in ('full','protected') else 0.,
        rung_f=.01 if variant in ('full','protected') else 0.,
        protection=.05 if variant=='protected' else 1.)


def small(seed,variant,duration=1200.):
    base=baseline(seed);g=genetics_config(base['chemistry'])
    g.update(sequence='001',free_units=36,function_units=36,box=[12.,9.],
        initial_assemblies=[dict(family=0,sequence='001',backbone=True) for _ in range(3)]+
            [dict(family=1,sequence='001',backbone=True) for _ in range(4)]+
            [dict(family=1,sequence=b,backbone=False) for b in '001011'],bond_turnover=rates(variant))
    return resolve(dict(schema_version=1,model='copy',seed=seed,duration=duration,
        name=f'RV1_{variant}_s{seed}',branch='RV1',chemistry=g,
        engine=copy.deepcopy(base['engine']),mechanics=copy.deepcopy(base['mechanics'])))


def transfer(seed,fine=False):
    cfg=baseline(seed);cfg['chemistry']['genetics']['bond_turnover']=rates('protected')
    cfg.update(name=f'RV1_bath_s{seed}'+('_fine' if fine else ''),branch='RV1')
    if fine:
        cfg['engine']['dt']/=2
        for k in ('reaction_every','sample_every'):cfg['engine'][k]*=2
    return resolve(cfg)


def plans():
    common=dict(workers=2,checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False,genetic_audit=False)
    a=dict(common,name='RV1 local material recycling and bond-loss ablations',
        comparison_policy='BATCH_31_PLAN prospective gate;12 trials, fixed laws per variant, finite stock; no homeostasis claim.',
        tasks=[dict(scenario=small(seed,variant)) for seed in range(3) for variant in ('zero','backbone','full','protected')])
    b=dict(common,name='RV1 selected MD2 transfer',comparison_policy='Gate-selected transfer, not independent validation; no auto adoption.',
        tasks=[dict(scenario=transfer(s)) for s in range(3)]+[dict(scenario=transfer(0,True))])
    return a,b


if __name__=='__main__':
    for name,plan in zip(('recycling_local','recycling_transfer'),plans()):
        p=ROOT/f'campaigns/{name}.json';p.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8');print(p)
