"""T9E: one local endpoint candidate, two initial preparations, gated MD2 transfer."""
import argparse,copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.config import resolve
from simulator.coupled_bath import genetics_config

MD2=ROOT/'research/campaign_recipes/MD2_20261030T115427443420Z/manifest.json'


def baseline(seed):
    tasks=json.loads(MD2.read_text(encoding='utf-8'))['tasks']
    return copy.deepcopy(next(t['scenario'] for t in tasks if t['label']==f'MD2_bath_new_s{seed}'))


def small(seed,variant,preparation):
    base=baseline(seed);g=genetics_config(base['chemistry'])
    if preparation not in ('expression','tool'):raise ValueError(preparation)
    groups=([dict(family=1,sequence=b,backbone=False) for b in '001011'] if preparation=='expression'
        else [dict(family=1,sequence='001',backbone=True)]+
             [dict(family=1,sequence=b,backbone=False) for b in '011'])
    g.update(free_units=24,function_units=24,box=[8.,6.],initial_assemblies=groups)
    if variant=='end':g['gf_end_capture']=True
    elif variant!='old':raise ValueError(variant)
    return resolve(dict(schema_version=1,model='copy',seed=seed,duration=1200.,
        name=f'T9E_{preparation}_{variant}_s{seed}',branch='T9E',chemistry=g,
        engine=copy.deepcopy(base['engine']),mechanics=copy.deepcopy(base['mechanics'])))


def transfer(seed,fine=False):
    cfg=baseline(seed);cfg['chemistry']['genetics']['gf_end_capture']=True
    cfg.update(name=f'T9E_bath_s{seed}'+('_fine' if fine else ''),branch='T9E')
    if fine:
        for key in ('reaction_every','sample_every'):cfg['engine'][key]*=2
        cfg['engine']['dt']/=2
    return resolve(cfg)


def plans():
    common=dict(workers=2,checkpoint_seconds=30.,kinetic_window=50.,
        record_trajectory=False,genetic_audit=True)
    a=dict(common,name='T9E local endpoint expression and complete-tool interference',
        comparison_policy='One opt-in local GF endpoint gate; G/G, rates, forces and Langevin MD2 unchanged. '
            'Two initial preparations have identical atom/symbol counts but different F connectivity. '
            'Small concentrated box, not an integrated cell;12 tasks and no parameter sweep.',
        tasks=[dict(scenario=small(seed,variant,prep)) for prep in ('expression','tool')
               for seed in range(3) for variant in ('old','end')])
    b=dict(common,name='T9E selected conditional transfer to MD2 bath',
        comparison_policy='Run only after prospective T9E small-bath gate. Three current MD2 seeds, '
            'one selected fine seed0 preserving reaction/observation cadence. Old MD2 results reused. '
            'Selected follow-up, not independent validation or convergence certificate.',
        tasks=[dict(scenario=transfer(seed)) for seed in range(3)]+[dict(scenario=transfer(0,True))])
    return a,b


if __name__=='__main__':
    a,b=plans()
    for name,value in (('expression_endpoints',a),('expression_transfer',b)):
        path=ROOT/f'campaigns/{name}.json';path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(path)
