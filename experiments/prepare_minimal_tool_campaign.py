"""MIN1: same assembler, smaller construction and its expression transfer."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from experiments.prepare_expression_campaign import baseline,MD2
from simulator.config import resolve
from simulator.coupled_bath import genetics_config


def configuration(seed,name,duration,g):
    b=baseline(seed)
    return resolve(dict(schema_version=1,model='copy',name=name,branch='MIN1',seed=seed,duration=duration,
        chemistry=g,engine=copy.deepcopy(b['engine']),mechanics=copy.deepcopy(b['mechanics'])))


def prepared(seed,variant,duration=400.):
    if variant not in ('long','short','split','no_boost'):raise ValueError(variant)
    g=genetics_config(baseline(seed)['chemistry'])
    if variant in ('short','no_boost'):
        groups=[dict(family=1,sequence='01',backbone=True),dict(family=1,sequence='0',backbone=False)]*4
    else:groups=[dict(family=1,sequence='001',backbone=variant=='long') for _ in range(4)]
    g.update(sequence='001',free_units=36,function_units=36,box=[12.,9.],template=False,initial_assemblies=groups)
    if variant=='no_boost':g['rung_catalytic_rate']=g['rung_formation_rate']
    return configuration(seed,f'MIN1_A_{variant}_s{seed}',duration,g)


def expression(seed,variant,duration=1200.):
    if variant not in ('short','long','nogene'):raise ValueError(variant)
    seq='001' if variant=='long' else '01';linked=variant!='nogene'
    g=genetics_config(baseline(seed)['chemistry'])
    g.update(sequence=seq,free_units=39-len(seq),function_units=36,box=[12.,9.],template=linked,
        initial_assemblies=[dict(family=0,sequence=seq,backbone=linked) for _ in range(3)]+
            [dict(family=1,sequence=b,backbone=False) for b in '001011'])
    return configuration(seed,f'MIN1_B_{variant}_s{seed}',duration,g)


def plans():
    common=dict(workers=2,checkpoint_seconds=30.,kinetic_window=50.,record_trajectory=False)
    a=dict(common,name='MIN1 minimum prepared assembler and local-motif controls',
        comparison_policy='BATCH_32_PLAN; no new tool/function; fixed MD2 laws except explicit no_boost ablation; equal composition in A.',
        tasks=[dict(scenario=prepared(s,v)) for s in range(3) for v in ('long','short','split','no_boost')])
    b=dict(common,name='MIN1 selected expression and product-use transfer',
        comparison_policy='Gate-selected follow-up, fixed laws, shorter gene versus001; initial inventories reported, no long-gene or integrated-cell claim.',
        tasks=[dict(scenario=expression(s,v)) for s in range(3) for v in ('short','long','nogene')])
    return a,b


if __name__=='__main__':
    for name,plan in zip(('minimal_tool_prepared','minimal_tool_expression'),plans()):
        path=ROOT/f'campaigns/{name}.json';path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8');print(path)
