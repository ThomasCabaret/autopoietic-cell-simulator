"""Fixed chemistry at scaled constructed inventory; no new molecular function."""
import argparse,copy,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from simulator.engine import Simulation


def scenario(scale,membrane,seed=0,no_boost=False,duration=1200.):
    if scale not in (1,8,16):raise ValueError(scale)
    ref=json.loads((ROOT/'research/campaign_recipes/J1_20261027T144451586423Z/manifest.json').read_text(encoding='utf-8'))
    raw=copy.deepcopy(next(t['scenario'] for t in ref['tasks'] if t['scenario']['name']=='J1_bath_prepared' and t['scenario']['seed']==seed))
    raw.update(name=f'J3_k{scale}_'+('bath' if membrane else 'open')+('_noBoost' if no_boost else ''),branch='J3',duration=duration)
    c=raw['chemistry'];c.update(include_membrane=membrane,packet_offset=[0.,0.],world_box=None)
    g=c['genetics'];g.update(free_units=27*scale-3,function_units=24*scale,box=[8*math.sqrt(scale),6*math.sqrt(scale)])
    g['initial_assemblies']=([dict(family=0,sequence='001',backbone=True) for _ in range(scale-1)]+
        [group for _ in range(scale) for group in ([dict(family=1,sequence='001',backbone=True)]+
                                               [dict(family=1,sequence=b,backbone=False) for b in '011'])])
    if no_boost:g['rung_catalytic_rate']=g['rung_formation_rate']
    return raw


def verify():
    rows=[]
    for scale in (1,8,16):
        for seed in range(3):
            a=Simulation(scenario(scale,True,seed,duration=.02));b=Simulation(scenario(scale,False,seed,duration=.02))
            ga=a.chemistry.genetics;gb=b.chemistry.genetics
            np.testing.assert_array_equal(ga.pos,gb.pos)
            assert a.rng.bit_generator.state==b.rng.bit_generator.state and ga.export()==gb.export()
            assert len(ga.pos)==102*scale and len(a.chemistry.pos)==486+102*scale
            active=ga.rungs[:,1]>=0
            assert active.sum()==9*scale and np.count_nonzero(~active)==42*scale
            assert np.bincount(ga.assembly.atom_bits,minlength=2).tolist()==[26*scale,25*scale]
            center=a.chemistry.box/2
            assert np.linalg.norm(ga.pos-center,axis=1).max()<34.5-1.
            if scale==16:
                control=Simulation(scenario(scale,True,seed,no_boost=True,duration=.02))
                np.testing.assert_array_equal(a.chemistry.pos,control.chemistry.pos)
                assert a.rng.bit_generator.state==control.rng.bit_generator.state
                assert a.chemistry.export()==control.chemistry.export()
            rows.append(dict(scale=scale,seed=seed,beads=486+102*scale,matched_initial_packet_and_rng=True))
    return rows


def plan():
    tasks=[dict(scenario=scenario(k,m,s)) for k in (1,8,16) for s in range(3) for m in (False,True)]
    tasks += [dict(scenario=scenario(16,True,s,no_boost=True)) for s in range(3)]
    return dict(name='J3 scaled constructed inventory with matched no-L and no-boost controls',workers=2,
        checkpoint_seconds=60,kinetic_window=25,record_trajectory=False,genetic_audit=True,
        comparison_policy='Same J0 chemistry, identical short genes replicated in the initial state, scale1/8/16. Matched PR/RNG with/without L. No-boost16 is a declared rate-ablation candidate. Centered packets; no inner wall, source or feedback.',tasks=tasks)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['plan','verify','pilot'])
    p.add_argument('--output',type=Path);a=p.parse_args()
    if a.action=='verify':print(json.dumps(verify()))
    elif a.action=='plan':(ROOT/'campaigns/density_transfer.json').write_text(json.dumps(plan(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    else:
        from simulator.runner import run
        from scripts.reconstruct_experiment import export_recipe
        evidence,path=run(scenario(16,True,0,duration=2.),a.output or ROOT/'research/engine_runs',record=False)
        export_recipe(path)
        if evidence['error']:raise SystemExit(1)
